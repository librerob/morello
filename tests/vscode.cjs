// Run in a disposable VS Code Extension Development Host under xvfb-run.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const modules = process.env.MORELLO_NODE_MODULES;
const dependency = name => require(path.join(modules, name));

async function syntax(theme, palette, appRoot) {
  const textmate = dependency('vscode-textmate');
  const oniguruma = dependency('vscode-oniguruma');
  const wasm = fs.readFileSync(path.join(modules, 'vscode-oniguruma/release/onig.wasm'));
  await oniguruma.loadWASM(wasm.buffer.slice(wasm.byteOffset, wasm.byteOffset + wasm.byteLength));
  for (const [extension, language, example] of [
    ['lua', 'lua', 'library.lua'], ['python', 'python', 'document.py'],
    ['typescript-basics', 'typescript', 'library.ts'],
  ]) {
    const directory = path.join(appRoot, 'extensions', extension);
    const contribution = JSON.parse(fs.readFileSync(path.join(directory, 'package.json'), 'utf8'));
    const grammarEntry = contribution.contributes.grammars.find(item => item.language === language);
    const registry = new textmate.Registry({
      theme: { settings: [{ settings: { foreground: palette.fg, background: palette.bg } }, ...theme.tokenColors] },
      onigLib: Promise.resolve({ createOnigScanner: patterns => new oniguruma.OnigScanner(patterns),
        createOnigString: value => new oniguruma.OnigString(value) }),
      loadGrammar: async scope => {
        const entry = contribution.contributes.grammars.find(item => item.scopeName === scope);
        if (!entry) return null;
        const filename = path.join(directory, entry.path);
        return textmate.parseRawGrammar(fs.readFileSync(filename, 'utf8'), filename);
      },
    });
    const grammar = await registry.loadGrammar(grammarEntry.scopeName);
    assert(grammar, `Missing ${language} grammar`);
    let stack = textmate.INITIAL;
    const seen = new Set();
    const allowed = new Set(Object.values(palette));
    for (const line of fs.readFileSync(path.join(root, 'examples', example), 'utf8').split(/\r?\n/)) {
      const result = grammar.tokenizeLine2(line, stack);
      stack = result.ruleStack;
      const colors = registry.getColorMap();
      for (let index = 1; index < result.tokens.length; index += 2) {
        const color = colors[(result.tokens[index] >>> 15) & 0x1ff].toUpperCase();
        assert(allowed.has(color), `${language}: off-palette token ${color}`);
        seen.add(color);
      }
    }
    for (const role of ['keyword', 'string', 'func', 'comment']) {
      assert(seen.has(palette[role]), `${language} did not resolve ${role}`);
    }
    registry.dispose();
  }
}

async function webviewColors(vscode, keys) {
  const panel = vscode.window.createWebviewPanel('morello-test', 'Morello colors', vscode.ViewColumn.One,
    { enableScripts: true });
  try {
    return await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('Theme CSS probe timed out')), 15000);
      const subscription = panel.webview.onDidReceiveMessage(colors => {
        clearTimeout(timer);
        subscription.dispose();
        resolve(colors);
      });
      panel.webview.html = `<!doctype html><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'nonce-morello-test'">
        <script nonce="morello-test">
        const vscode = acquireVsCodeApi();
        const style = getComputedStyle(document.documentElement);
        vscode.postMessage(Object.fromEntries(${JSON.stringify(keys)}.map(key =>
          [key, style.getPropertyValue('--vscode-' + key.replaceAll('.', '-')).trim()])));
        </script>`;
    });
  } finally {
    panel.dispose();
  }
}

exports.run = async function () {
  const vscode = require('vscode');
  assert(vscode.extensions.getExtension('librerob.morello-theme'), 'Theme extension did not register');
  for (const variant of ['dark', 'light', 'dark']) {
    const suffix = variant === 'light' ? '-light' : '';
    const data = JSON.parse(fs.readFileSync(path.join(root, `palette${suffix}.json`), 'utf8'));
    const theme = JSON.parse(fs.readFileSync(path.join(root, `ports/vscode/themes/morello${suffix}-color-theme.json`), 'utf8'));
    await vscode.workspace.getConfiguration('workbench').update('colorTheme', data.name, vscode.ConfigurationTarget.Global);
    const expectedKind = variant === 'dark' ? vscode.ColorThemeKind.Dark : vscode.ColorThemeKind.Light;
    const deadline = Date.now() + 10000;
    while (vscode.window.activeColorTheme.kind !== expectedKind && Date.now() < deadline) {
      await new Promise(resolve => setTimeout(resolve, 50));
    }
    assert.equal(vscode.window.activeColorTheme.kind, expectedKind, 'Wrong active theme variant');
    const pairs = { 'editor.background': 'bg', 'editor.foreground': 'fg', 'sideBar.background': 'panel',
      'editorInlayHint.foreground': 'comment', 'editorInlayHint.typeForeground': 'comment',
      'editorInlayHint.parameterForeground': 'comment', 'editorCodeLens.foreground': 'comment',
      'editorSuggestWidget.background': 'float', 'editorSuggestWidget.foreground': 'fg' };
    const actual = await webviewColors(vscode, Object.keys(pairs));
    const rgb = color => color.match(/^#[0-9a-f]{6}$/i) ? color.toUpperCase() :
      '#' + color.match(/[\d.]+/g).slice(0, 3).map(channel => Number(channel).toString(16).padStart(2, '0')).join('').toUpperCase();
    for (const [key, role] of Object.entries(pairs)) {
      assert(actual[key], `Unregistered VS Code color ${key}`);
      assert.equal(rgb(actual[key]), data.colors[role], `${variant} ${key} default color leaked`);
    }
    await syntax(theme, data.colors, vscode.env.appRoot);
    const document = await vscode.workspace.openTextDocument(path.join(root, 'examples/library.ts'));
    const editor = await vscode.window.showTextDocument(document);
    editor.selection = new vscode.Selection(0, 0, 0, 12);
    await vscode.commands.executeCommand('editor.action.selectHighlights');
    console.log(`VS Code ${variant}: active theme, resolved UI colors and Lua/Python/TypeScript grammars passed`);
  }
};

if (require.main === module) {
  dependency('@vscode/test-electron').runTests({
    version: process.env.MORELLO_VSCODE_VERSION || 'stable',
    cachePath: path.join(process.env.RUNNER_TEMP, 'morello-vscode'),
    extensionDevelopmentPath: path.join(root, 'ports/vscode'), extensionTestsPath: __filename,
    launchArgs: ['--disable-gpu', '--skip-welcome', '--skip-release-notes'],
    extensionTestsEnv: { MORELLO_NODE_MODULES: modules },
  }).catch(error => { console.error(error); process.exitCode = 1; });
}

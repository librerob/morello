"""Regenerate extra terminal ports and VS Code themes from both palettes."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')


def write_json(path, value):
    write(path, json.dumps(value, indent=2))


def generate(variant):
    suffix = '-light' if variant == 'light' else ''
    data = json.loads((ROOT / f'palette{suffix}.json').read_text(encoding='utf-8'))
    p, ansi = data['colors'], data['ansi']
    ghostty = [f'# {data["name"]}', f'background = {p["bg"]}', f'foreground = {p["fg"]}',
               f'cursor-color = {p["cursor"]}', f'cursor-text = {p["bg"]}',
               f'selection-background = {p["selection"]}', f'selection-foreground = {p["fg"]}']
    ghostty += [f'palette = {index}={color}' for index, color in enumerate(ansi)]
    write(f'ports/ghostty/{data["name"]}', '\n'.join(ghostty))

    slots = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white',
             'brightBlack', 'brightRed', 'brightGreen', 'brightYellow', 'brightBlue',
             'brightPurple', 'brightCyan', 'brightWhite']
    windows = {'name': data['name'], 'background': p['bg'], 'foreground': p['fg'],
               'cursorColor': p['cursor'], 'selectionBackground': p['selection']}
    windows.update(zip(slots, ansi))
    write_json(f'ports/windows-terminal/{data["name"]}.json', windows)

    xfce = {
        'Name': data['name'], 'ColorForeground': p['fg'], 'ColorBackground': p['bg'],
        'ColorCursor': p['cursor'], 'ColorCursorForeground': p['bg'], 'ColorCursorUseDefault': 'FALSE',
        'ColorSelection': p['fg'], 'ColorSelectionBackground': p['selection'],
        'ColorSelectionUseDefault': 'FALSE', 'ColorPalette': ';'.join(ansi),
        'ColorBoldUseDefault': 'TRUE', 'ColorBoldIsBright': 'FALSE',
        'ColorUseTheme': 'FALSE', 'ColorBackgroundVary': 'FALSE', 'TabActivityColor': p['focus'],
    }
    write(f'ports/xfce-terminal/{data["name"]}.theme',
          '[Scheme]\n' + '\n'.join(f'{key}={value}' for key, value in xfce.items()))

    def rgb(color):
        return ','.join(str(int(color[i:i+2], 16)) for i in (1, 3, 5))

    konsole = ['[General]', f'Description={data["name"]}', 'Opacity=1',
               'Blur=false', 'ColorRandomization=false', 'Wallpaper=', '']
    entries = {'Foreground': p['fg'], 'ForegroundIntense': p['bright'],
               'ForegroundFaint': p['muted'], 'Background': p['bg'],
               'BackgroundIntense': p['bg'], 'BackgroundFaint': p['bg']}
    for index in range(8):
        entries[f'Color{index}'] = ansi[index]
        entries[f'Color{index}Intense'] = ansi[index + 8]
        entries[f'Color{index}Faint'] = ansi[index]
    for name, color in entries.items():
        konsole += [f'[{name}]', f'Color={rgb(color)}', '']
    write(f'ports/konsole/{data["name"]}.colorscheme', '\n'.join(konsole))

    # Older foot versions use [colors]. The default inverse cursor matches ours.
    foot = [f'foreground={p["fg"][1:]}', f'background={p["bg"][1:]}',
            f'selection-foreground={p["fg"][1:]}', f'selection-background={p["selection"][1:]}']
    foot += [f'{"regular" if i < 8 else "bright"}{i % 8}={color[1:]}' for i, color in enumerate(ansi)]
    write(f'ports/foot/morello{suffix}-legacy.ini',
          '# For foot before 1.26. Colors only.\n[colors]\n' + '\n'.join(foot))
    foot += [f'cursor={p["bg"][1:]} {p["cursor"][1:]}', f'urls={p["string"][1:]}']
    foot_sections[variant] = f'[colors-{variant}]\n' + '\n'.join(foot)

    roles = {
        'foreground': 'fg', 'descriptionForeground': 'muted', 'errorForeground': 'error',
        'focusBorder': 'focus', 'textLink.foreground': 'func', 'textLink.activeForeground': 'bright',
        'editor.background': 'bg', 'editor.foreground': 'fg',
        'editorCursor.foreground': 'cursor', 'editor.lineHighlightBackground': 'line',
        'editor.selectionBackground': 'selection', 'editor.selectionForeground': 'fg',
        'editor.inactiveSelectionBackground': 'selection',
        'editorLineNumber.foreground': 'subdued', 'editorLineNumber.activeForeground': 'focus',
        'editorIndentGuide.background1': 'border', 'editorIndentGuide.activeBackground1': 'comment',
        'editorWhitespace.foreground': 'subdued', 'editorRuler.foreground': 'border',
        'editor.findMatchBackground': 'search_current_bg', 'editor.findMatchForeground': 'search_current_fg',
        'editor.findMatchHighlightForeground': 'fg',
        'editorError.foreground': 'error', 'editorWarning.foreground': 'warning',
        'editorInfo.foreground': 'info', 'editorHint.foreground': 'hint',
        'editorGutter.addedBackground': 'focus', 'editorGutter.modifiedBackground': 'info',
        'editorGutter.deletedBackground': 'error', 'editorBracketMatch.border': 'focus',
        'editorBracketMatch.background': 'line', 'editorGroupHeader.tabsBackground': 'panel',
        'tab.activeBackground': 'bg', 'tab.activeForeground': 'fg', 'tab.activeBorderTop': 'func',
        'tab.inactiveBackground': 'panel', 'tab.inactiveForeground': 'muted', 'tab.border': 'panel',
        'sideBar.background': 'panel', 'sideBar.foreground': 'fg', 'sideBar.border': 'border',
        'sideBarTitle.foreground': 'muted', 'sideBarSectionHeader.background': 'panel',
        'activityBar.background': 'panel', 'activityBar.foreground': 'func',
        'activityBar.inactiveForeground': 'comment', 'activityBarBadge.background': 'func',
        'activityBarBadge.foreground': 'bg', 'statusBar.background': 'panel', 'statusBar.foreground': 'muted',
        'statusBar.debuggingBackground': 'keyword', 'statusBar.debuggingForeground': 'bg',
        'statusBar.noFolderBackground': 'panel', 'titleBar.activeBackground': 'panel',
        'titleBar.activeForeground': 'fg', 'titleBar.inactiveBackground': 'panel',
        'titleBar.inactiveForeground': 'muted', 'panel.background': 'panel', 'panel.border': 'border',
        'panelTitle.activeForeground': 'fg', 'panelTitle.inactiveForeground': 'muted',
        'input.background': 'float', 'input.foreground': 'fg', 'input.border': 'border',
        'input.placeholderForeground': 'comment', 'inputOption.activeBorder': 'focus',
        'dropdown.background': 'float', 'dropdown.foreground': 'fg', 'dropdown.border': 'border',
        'button.background': 'func', 'button.foreground': 'bg', 'button.hoverBackground': 'bright',
        'badge.background': 'func', 'badge.foreground': 'bg',
        'list.activeSelectionBackground': 'selection', 'list.activeSelectionForeground': 'fg',
        'list.inactiveSelectionBackground': 'line', 'list.inactiveSelectionForeground': 'fg',
        'list.hoverBackground': 'line', 'list.highlightForeground': 'func',
        'quickInput.background': 'float', 'quickInput.foreground': 'fg',
        'editorWidget.background': 'float', 'editorWidget.foreground': 'fg', 'editorWidget.border': 'border',
        'editorSuggestWidget.background': 'float', 'editorSuggestWidget.foreground': 'fg',
        'editorSuggestWidget.selectedBackground': 'selection', 'editorSuggestWidget.highlightForeground': 'func',
        'editorHoverWidget.background': 'float', 'editorHoverWidget.foreground': 'fg',
        'editorHoverWidget.border': 'border', 'notifications.background': 'float',
        'notifications.foreground': 'fg', 'notificationCenterHeader.background': 'panel',
        'terminal.background': 'bg', 'terminal.foreground': 'fg',
        'terminalCursor.foreground': 'cursor', 'terminal.selectionBackground': 'selection',
        'gitDecoration.addedResourceForeground': 'focus', 'gitDecoration.modifiedResourceForeground': 'info',
        'gitDecoration.deletedResourceForeground': 'error', 'gitDecoration.ignoredResourceForeground': 'comment',
    }
    workbench = {key: p[role] for key, role in roles.items()}
    workbench['editor.findMatchHighlightBackground'] = p['search_bg'] + '26'
    ansi_names = ['Black','Red','Green','Yellow','Blue','Magenta','Cyan','White']
    for index, color in enumerate(ansi):
        workbench['terminal.ansi' + ('Bright' if index > 7 else '') + ansi_names[index % 8]] = color

    scopes = {
        'comment': ['comment', 'punctuation.definition.comment'],
        'keyword': ['keyword', 'storage.type', 'storage.modifier'],
        'func': ['entity.name.function', 'support.function', 'meta.function-call', 'entity.name.function.member'],
        'string': ['string', 'markup.inline.raw'],
        'constant': ['constant', 'variable.other.constant', 'support.constant'],
        'type': ['entity.name.type', 'entity.name.class', 'entity.other.inherited-class', 'support.type', 'support.class'],
        'variable': ['variable', 'meta.object-literal.key', 'support.variable'],
        'operator': ['keyword.operator'],
        'punctuation': ['punctuation.separator', 'punctuation.terminator', 'punctuation.section'],
    }
    token_colors = [{'scope': scope, 'settings': {'foreground': p[role]}} for role, scope in scopes.items()]
    token_colors += [
        {'scope': ['entity.name.tag'], 'settings': {'foreground': p['keyword']}},
        {'scope': ['entity.other.attribute-name'], 'settings': {'foreground': p['func']}},
        {'scope': ['markup.heading'], 'settings': {'foreground': p['func'], 'fontStyle': 'bold'}},
        {'scope': ['markup.italic'], 'settings': {'fontStyle': 'italic'}},
        {'scope': ['markup.bold'], 'settings': {'fontStyle': 'bold'}},
        {'scope': ['markup.inserted'], 'settings': {'foreground': p['focus']}},
        {'scope': ['markup.deleted'], 'settings': {'foreground': p['error']}},
    ]
    semantic_roles = {'variable':'variable', 'parameter':'variable', 'property':'variable',
        'function':'func', 'method':'func', 'class':'type', 'interface':'type', 'struct':'type',
        'enum':'type', 'type':'type', 'typeParameter':'type', 'namespace':'type',
        'enumMember':'constant', 'variable.readonly':'constant', 'keyword':'keyword',
        'comment':'comment', 'string':'string', 'number':'constant', 'operator':'operator'}
    theme = {'name':data['name'], 'type':variant, 'semanticHighlighting':True,
             'colors':workbench, 'tokenColors':token_colors,
             'semanticTokenColors':{key:p[role] for key,role in semantic_roles.items()}}
    write_json(f'ports/vscode/themes/morello{suffix}-color-theme.json',theme)


foot_sections = {}
for variant in ('dark', 'light'):
    generate(variant)
write('ports/foot/morello.ini', '# Morello for foot 1.26+. Both variants; colors only.\n'
      + '\n\n'.join(foot_sections.values()))
data = json.loads((ROOT / 'palette.json').read_text(encoding='utf-8'))
write_json('ports/vscode/package.json', {
    'name':'morello-theme', 'displayName':'Morello', 'description':'Cherry ink and blush paper. Dark and light colors for editors and terminals.',
    'version':data['version'], 'publisher':'librerob', 'engines':{'vscode':'^1.85.0'},
    'categories':['Themes'], 'license':'MIT',
    'repository':{'type':'git','url':'https://github.com/librerob/morello'},
    'contributes':{'themes':[
        {'label':'Morello','uiTheme':'vs-dark','path':'./themes/morello-color-theme.json'},
        {'label':'Morello Light','uiTheme':'vs','path':'./themes/morello-light-color-theme.json'},
    ]},
})
print('Regenerated dark and light extra terminal ports and VS Code themes')

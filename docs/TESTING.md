# Testing

Both palettes are checked by [Verify palette](../.github/workflows/verify.yml) and [Application regression tests](../.github/workflows/battle-test.yml). Tests use disposable settings directories and do not change existing application profiles.

| Target | Coverage |
| --- | --- |
| Palettes | 348 specified contrast pairs, strict HEX values, ANSI order and agreement across ports. Structural colors and utility ANSI slots are documented exceptions. |
| Generators | Two complete regeneration passes from a different working directory; committed files must remain byte-for-byte identical. |
| Neovim | 0.10.0, 0.10.4 and current stable: repeated dark/light switching, reloads, resolved UI colors, syntax tokens, diagnostics, diff states and completion-match contrast. |
| Neovim plugins | Real lualine mode highlights and Telescope pickers. On current Neovim, Oil and Neo-tree windows, Snacks pickers, and highlight mappings with Which-key, Gitsigns, nvim-cmp and blink.cmp loaded. Blink uses its stable v1 branch and Lua matcher. |
| Vim | Native loading, variant switches, shared syntax/UI groups, comment styles and terminal ANSI colors on Ubuntu 22.04 and the current Ubuntu runner. |
| Kitty | Native configuration parser, including cursor, selection, tabs and marks; foreground, background and 16 ANSI colors queried from a running terminal. |
| Alacritty | Native startup with each TOML file, foreground/background and all 16 ANSI colors queried from the running terminal. |
| Xfce Terminal | Scheme properties applied through an isolated terminalrc; foreground/background and all 16 ANSI colors queried from the running terminal. This does not automate the Preferences preset chooser. |
| Konsole | Native scheme loading, foreground/background queries, and exact pixel checks of all 16 rendered ANSI background swatches. OSC 4 queries alone are unsuitable here: Konsole's query fallback uses its built-in table instead of the profile palette. |
| foot | Legacy files checked with Ubuntu's native parser; both modern color sections checked with the current Arch package. |
| Ghostty | Both files checked by the official macOS binary's native configuration validator. |
| Windows Terminal | Both scheme objects validated against Microsoft's official JSON schema, including unknown-property rejection. |
| VS Code | 1.85.2 and current stable in a real Extension Development Host: variant switching, resolved theme CSS colors, and TextMate tokenization using bundled Lua, Python and TypeScript grammars. |
| Base16 | Both current and legacy YAML files parsed, slots checked and role mapping compared with the palettes. |
| bat | Native cache rebuilding, theme discovery, and actual truecolor syntax output for all three example languages. |
| colorls | Native dark/light listings using temporary configuration; ANSI directory colors and readable metadata checked. Requires the matching terminal preset. |
| Emacs and Doom | Native face resolution, Python Font Lock, selections, diffs, inlay hints, terminal colors and repeated variant switches on both Ubuntu runners. Doom uses the framework revision pinned in the workflow. |
| Repository assets | Local documentation links, SVG parsing, all eight preview images, and rejection of blank black or solid-color captures. The capture shell script is checked with ShellCheck. |

The terminal swatches are retained as CI artifacts. The screenshot workflow separately captures real Neovim windows in Kitty and validates each frame before publishing it.

## Limits

These checks cover the supplied files and exercised application states. They do not establish whole-application WCAG conformance or test every plugin configuration, major mode, language server or display. Windows Terminal has schema coverage rather than a rendered Windows GUI test; Ghostty and foot have native parser coverage rather than window rendering tests. Emacs checks run headlessly. TextMate grammar tests do not launch language servers or test their semantic token streams.

External software changes over time. The workflows record the installed package versions; current-stable jobs deliberately catch compatibility changes. Different font rendering, opacity, dim attributes, accessibility settings and user overrides can change the final appearance.

References: [VS Code theme colors](https://code.visualstudio.com/api/references/theme-color), [Windows Terminal schema](https://github.com/microsoft/terminal/blob/main/doc/cascadia/profiles.schema.json), [Konsole's color query implementation](https://github.com/KDE/konsole/blob/master/src/Vt102Emulation.cpp), and [Ghostty's validator](https://github.com/ghostty-org/ghostty/blob/main/src/cli/validate_config.zig).

# Morello

A dark cherry colorscheme. Celadon functions, apricot keywords, and pale citrine strings.

![Morello in Neovim](assets/neovim-lua.png)

## Install

### Neovim

Neovim 0.10+ and a truecolor terminal. With lazy.nvim:

```lua
{
  "librerob/morello",
  lazy = false,
  priority = 1000,
  config = function()
    vim.cmd.colorscheme("morello")
  end,
}
```

For a manual install, copy `colors/morello.lua` and `lua/` into the corresponding directories in `vim.fn.stdpath("config")`.

The only optional setting is comment italics, set before loading:

```lua
require("morello").setup({ italic_comments = true })
```

Includes standard syntax, Treesitter, LSP semantic tokens, diagnostics, diffs, and terminal colors. There are highlight mappings for Telescope, Neo-tree, Oil, Gitsigns, Which-key, blink.cmp, nvim-cmp, and Snacks. Their plugins and language parsers are installed separately. For lualine, set `options.theme = "morello"` in your lualine setup.

### Terminals

| App | File | Setup |
| --- | --- | --- |
| Alacritty | [alacritty.toml](ports/alacritty/alacritty.toml) | Copy beside your config and add its path to your existing `[general]` import array. |
| Kitty | [kitty.conf](ports/kitty/kitty.conf) | Copy to `themes/morello.conf`, then add `include themes/morello.conf` after other color settings. |
| Ghostty | [Morello](ports/ghostty/Morello) | Copy to `~/.config/ghostty/themes/Morello`, then set `theme = Morello`. |
| Windows Terminal | [Morello.json](ports/windows-terminal/Morello.json) | Add the object to `schemes` in Settings JSON, then choose Morello in your profile's Appearance settings. |

These files set colors only. Editor syntax highlighting needs its editor theme too.

### VS Code

The [VS Code port](ports/vscode) includes workbench colors, TextMate scopes, semantic tokens, and the same terminal palette. It is not published on the Marketplace. To try it locally, copy that directory into `~/.vscode/extensions/librerob.morello-theme-0.1.1`, reload VS Code, then choose **Morello** from **Preferences: Color Theme**.

## Previews

### Python

![Python in Neovim](assets/neovim-python.png)

### Search, diagnostics, and a floating panel

![Search and floating documentation in Neovim](assets/neovim-ui.png)

These are captures of Neovim running in Kitty with JetBrains Mono, the included Kitty port, and a minimal built-in winbar and statusline. The UI view uses illustrative Error and Warning diagnostics with text labels. Lua uses the bundled Treesitter parser; Python uses the built-in syntax definitions. The examples and capture script are included. No image filters or transparency are used.

## Colors

![Morello palette](assets/palette.svg)

The base is a dark red-violet, with a darker matching panel color. Apricot marks control flow, celadon marks functions, and citrine marks strings. Types use a quieter blue-grey; ordinary variables remain off-white. Neutral punctuation sits above the mauve comments. Raspberry errors are distinct from the apricot keywords; error signs and error messages also use bold text.

Body text contrast is **12.36:1**. Core syntax, punctuation, and comments pass **4.5:1** on the background, panel, cursor line, and floating surface. The report contains 136 tested pairs, including selections, search, and diff states. Inactive line numbers, borders, and ANSI black are deliberate exceptions. Transparency, dim attributes, and other plugins may change contrast.

[Full palette](docs/PALETTE.md) · [Measured contrast](docs/contrast-report.json) · [Design notes](docs/DESIGN.md)

## Development

`palette.json` is the source for every port. With Python 3.11+:

```sh
python scripts/sync_ports.py
python scripts/sync_extras.py
python scripts/verify.py
python scripts/verify_extras.py
nvim --headless -u NONE -l tests/headless.lua
```

To refresh the screenshots on Linux, install Kitty, Xvfb, xdotool, ImageMagick, JetBrains Mono, Python 3, and Neovim, then run:

```sh
xvfb-run -a bash scripts/capture.sh
```

`NVIM_BIN` can override Neovim on `PATH`. On a headless machine without a GPU, add `LIBGL_ALWAYS_SOFTWARE=1` before `xvfb-run`. The palette module can be used independently: `require("morello.palette")` returns the colors without changing editor settings. ANSI entries use indices 0–15.

## License

[MIT](LICENSE).

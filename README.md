# Morello

Cherry ink at night, blush paper by day. A dark and light colorscheme for editors and terminals.

**Dark** · celadon functions, apricot keywords, and pale citrine strings.

![Morello Dark in Neovim](assets/neovim-lua.png)

**Light** · jade functions, terracotta keywords, and olive citrine strings.

![Morello Light in Neovim](assets/neovim-light-lua.png)

## Install

### Neovim

Neovim 0.10+ and a truecolor terminal. With lazy.nvim:

```lua
{
  "librerob/morello",
  lazy = false,
  priority = 1000,
  config = function()
    vim.o.background = "dark" -- "light" for blush paper
    vim.cmd.colorscheme("morello")
  end,
}
```

For a manual install, copy `colors/morello.lua` and `lua/` into the corresponding directories in `vim.fn.stdpath("config")`.

Morello follows Neovim's `background` setting. Change it with `:set background=light` or `:set background=dark`; the colorscheme reloads automatically.

Comment italics are optional, set before loading:

```lua
require("morello").setup({ italic_comments = true })
```

Includes standard syntax, Treesitter, LSP semantic tokens, diagnostics, diffs, and terminal colors. There are highlight mappings for Telescope, Neo-tree, Oil, Gitsigns, Which-key, blink.cmp, nvim-cmp, and Snacks. Their plugins and language parsers are installed separately. For lualine, set `options.theme = "morello"` in your lualine setup.

### Terminals

| App | Dark | Light | Setup |
| --- | --- | --- | --- |
| Alacritty | [alacritty.toml](ports/alacritty/alacritty.toml) | [alacritty-light.toml](ports/alacritty/alacritty-light.toml) | Import your chosen file through the existing `[general]` import array. |
| Kitty | [kitty.conf](ports/kitty/kitty.conf) | [kitty-light.conf](ports/kitty/kitty-light.conf) | Include your chosen file after other color settings. |
| Ghostty | [Morello](ports/ghostty/Morello) | [Morello Light](ports/ghostty/Morello%20Light) | Copy to `~/.config/ghostty/themes/`, then set `theme = Morello` or `theme = Morello Light`. |
| Windows Terminal | [Morello.json](ports/windows-terminal/Morello.json) | [Morello Light.json](ports/windows-terminal/Morello%20Light.json) | Add either object to `schemes`, then choose it in your profile's Appearance settings. |

These files set colors only. Editor syntax highlighting needs its editor theme too.

### VS Code

The [VS Code port](ports/vscode) includes both variants, workbench colors, TextMate scopes, semantic tokens, and matching terminal palettes. It is not published on the Marketplace. To try it locally, copy that directory into `~/.vscode/extensions/librerob.morello-theme-0.2.0`, reload VS Code, then choose **Morello** or **Morello Light** from **Preferences: Color Theme**.

## Previews

### Python

![Python in Neovim](assets/neovim-python.png)

![Python in Morello Light](assets/neovim-light-python.png)

### TypeScript

![TypeScript in Morello Light](assets/neovim-light-typescript.png)

### Search, diagnostics, and a floating panel

![Search and floating documentation in Neovim](assets/neovim-ui.png)

![Search and diagnostics in Morello Light](assets/neovim-light-ui.png)

These are captures of Neovim running in Kitty with JetBrains Mono, the matching Kitty port, and a minimal built-in winbar and statusline. The UI views use illustrative Error and Warning diagnostics with text labels. Lua uses the bundled Treesitter parser; Python and TypeScript use the built-in syntax definitions. The examples and capture script are included. Captures are checked for a rendered theme background, text, and syntax colors before replacing the published previews. No image filters or transparency are used.

## Colors

![Morello palette](assets/palette.svg)

![Morello Light palette](assets/palette-light.svg)

The base is a dark red-violet, with a darker matching panel color. Apricot marks control flow, celadon marks functions, and citrine marks strings. Types use a quieter blue-grey; ordinary variables remain off-white. Neutral punctuation sits above the mauve comments. Raspberry errors are distinct from the apricot keywords; error signs and error messages also use bold text.

The light variant uses a quiet blush ground with deep cherry text. Terracotta, jade, and olive citrine preserve the warm keywords, cool functions, and yellow-green strings of the dark variant at readable light-theme values.

Body text contrast is **12.36:1** in dark and **13.29:1** in light. Core syntax, punctuation, and comments pass **4.5:1** on the background, panel, cursor line, and floating surface in both variants. The light variant also tests every core text color on selection and diff backgrounds. The reports cover **348 pairs** in total, including search and UI states. Inactive line numbers, passive borders, and utility ANSI slots are deliberate exceptions: dark uses ANSI 0 as a dark surface; light keeps ANSI 7 and 15 as pale backgrounds. Transparency, dim attributes, and other plugins may change contrast.

[Dark palette](docs/PALETTE.md) · [Light palette](docs/PALETTE-LIGHT.md) · [Dark contrast](docs/contrast-report.json) · [Light contrast](docs/contrast-report-light.json) · [Design notes](docs/DESIGN.md)

## Development

`palette.json` and `palette-light.json` are the sources for every port. With Python 3.11+:

```sh
python scripts/sync_ports.py
python scripts/sync_extras.py
python scripts/verify.py
python scripts/verify_extras.py
nvim --headless -u NONE -l tests/headless.lua
```

To refresh both sets of screenshots on Linux, install Kitty, Xvfb, xdotool, ImageMagick, JetBrains Mono, Python 3 with Pillow, and Neovim, then run:

```sh
xvfb-run -a bash scripts/capture.sh
```

`NVIM_BIN` can override Neovim on `PATH`. On a headless machine without a GPU, add `LIBGL_ALWAYS_SOFTWARE=1` before `xvfb-run`. `require("morello").get_palette()` returns the active palette. For a fixed variant without changing editor settings, use `require("morello.palette")` or `require("morello.palette-light")`. ANSI entries use indices 0–15.

## License

[MIT](LICENSE).

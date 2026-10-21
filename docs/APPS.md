# More apps

Each port has a dark and light variant generated from the same palettes as Neovim and the terminals.

## Base16

Use [morello.yaml](../ports/base16/morello.yaml) or [morello-light.yaml](../ports/base16/morello-light.yaml) with a builder that accepts Tinted Theming's Base16 scheme format. For older builders that expect top-level `base00`–`base0F` keys, use the matching file in [legacy/](../ports/base16/legacy).

The mapping keeps cherry ink or blush paper at `base00`, readable mauve comments at `base03`, ordinary text at `base05`, strings at `base0B`, functions at `base0D`, and keywords at `base0E`. `base06` and `base07` share the brightest foreground. A builder's application template decides how these slots are used; this is a semantic Base16 scheme, rather than a copy of the terminal's ANSI slot order.

The files are not yet included in the upstream Tinted scheme collection. Add them as local schemes through your chosen builder.

## bat

From a checkout of this repository:

```sh
mkdir -p "$(bat --config-dir)/themes"
cp ports/bat/*.tmTheme "$(bat --config-dir)/themes/"
bat cache --build
bat --theme="Morello" examples/document.py
bat --theme="Morello Light" examples/document.py
```

Use `BAT_THEME=Morello` or `BAT_THEME="Morello Light"` to choose a default, or put `--theme="Morello"` in bat's config file. Some distributions name the command `batcat`; substitute it in the commands above. Rebuild the cache after updating the files. See [bat's custom-theme instructions](https://github.com/sharkdp/bat#adding-new-themes).

## colorls

Copy the two color files into colorls's config directory:

```sh
mkdir -p ~/.config/colorls
cp ports/colorls/dark_colors.yaml ports/colorls/light_colors.yaml ~/.config/colorls/
colorls --dark
colorls --light
```

Back up existing color files before replacing them. Directories and executable files use celadon or jade; file sizes, permissions, and Git status use the supporting accents. Age labels and other metadata remain readable. Tree guides use the lower-contrast border color. The terminal's own background comes from its terminal theme. See [colorls's configuration guide](https://github.com/athityakumar/colorls#custom-configurations).

## Emacs

Emacs 27.1+ with a GUI or truecolor terminal. Copy both files in [ports/emacs](../ports/emacs) to a directory such as `~/.emacs.d/themes/`, then add:

```elisp
(add-to-list 'custom-theme-load-path "~/.emacs.d/themes/")
(load-theme 'morello t)
```

For light, use `(load-theme 'morello-light t)`. Disable the previous theme when switching, so settings from unrelated themes do not remain layered:

```elisp
(mapc #'disable-theme custom-enabled-themes)
(load-theme 'morello-light t)
```

The standalone themes require no theme framework. They include core Font Lock, newer syntax faces, Org, diffs, Magit, completion, inlay hints, and ANSI/vterm colors. Mappings for optional packages take effect when those packages are installed. Comments and inlay hints stay upright. Text rendering and token classification depend on the display and major mode.

## Doom Emacs

The separate [Doom themes](../ports/doom-emacs) use the `doom-themes` framework's palette API and base integrations. Copy both files into your Doom configuration's `themes/` directory, such as `~/.config/doom/themes/` or `~/.doom.d/themes/`. In `config.el`:

```elisp
(add-to-list 'custom-theme-load-path (expand-file-name "themes/" doom-user-dir))
(setq doom-theme 'doom-morello)
```

For light, set `doom-theme` to `doom-morello-light`. Restart Doom or load the selected theme. The Doom variants share the standalone theme's core faces and add the named colors expected by `doom-color` and Doom integrations. `doom-themes` is the only theme-library dependency; it is normally supplied by Doom's theme module. Exact RGB colors require a GUI or truecolor terminal.

## Validation

The workflow checks both variants through Ruby's YAML parser, bat's native cache and renderer, colorls 1.5.0, and Emacs. Doom tests load the actual `doom-themes` framework at a pinned upstream revision. The Emacs checks cover core faces, readable inlay hints, selections, diffs, ANSI colors, repeated variant switching, and Python Font Lock. The ports have not been visually tested across every application, terminal, major mode, or plugin.

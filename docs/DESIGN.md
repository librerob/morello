# Design notes

The central relationship is cherry ink against celadon and apricot. The background carries the identity. It stays red-violet through raised surfaces, while sidebars and status lines use a darker shade of the same ground.

The three primary accents have separate jobs. Apricot marks keywords and control flow. Celadon marks functions and the active UI. Citrine marks strings. Blue-grey types and rose constants provide secondary distinctions. Plain variables remain off-white; punctuation uses a more neutral grey above the comment lightness, while staying below the body text. Both are tested as readable text.

The off-white is slightly pink rather than yellow or blue. That makes a large paragraph feel related to the cherry surface without tinting it as strongly as the accent colors. Comments use a muted mauve with a minimum 4.5:1 contrast on all four reading surfaces. Error text shifts toward raspberry to separate it from apricot keywords. Error signs are bold, while diagnostic underlines and severity labels supply cues beyond color.

The main accents do not have identical lightness: functions and strings sit a little above the apricot keywords. This gives declarations and values some prominence without turning keywords into decoration. Diff backgrounds and selected text have their own tested pairs. Search uses a strong fill only while searching.

Three candidate directions were compared on the same Python sample: cherry ink, ink violet, and rosewood. Violet felt too close to existing night palettes; rosewood felt too close to established earth tones. Cherry ink gave the clearest separate identity. These are subjective design judgments.

## Research

The following primary sources were reviewed on 20 October 2026. This is a focused comparison, not an exhaustive search of every theme or a claim that any hue belongs to one project.

| Project | What it already covers | Implication for this design |
| --- | --- | --- |
| [Dracula](https://spec.draculatheme.com/) | A grey-violet ground with strong pink, purple, green, and yellow accents. | A vivid rainbow on a familiar dark base would offer little distinction. |
| [Nord](https://www.nordtheme.com/docs/colors-and-palettes/) | A coherent blue-grey base and cool Frost accents. | A blue-grey foundation would compete directly with an established identity. |
| [Gruvbox](https://github.com/morhetz/gruvbox) | Warm retro colors, configurable contrast, and broad language support. | Warmth by itself is not a new proposition. |
| [Rosé Pine](https://rosepinetheme.com/palette/) | Violet surfaces with rose, foam, iris, and gold accents. | A dusty lavender foundation would be an especially close comparison. |
| [Catppuccin](https://github.com/catppuccin/catppuccin) | Four pastel palettes and an extensive port ecosystem. | A large set of gentle colors and attractive swatches is not sufficient differentiation. |
| [Everforest](https://github.com/sainnhe/everforest) | Green and earth tones with several contrast levels. | Botanical warmth is already well served. |
| [Kanagawa](https://github.com/rebelot/kanagawa.nvim) | Painting-inspired muted color and layered dark surfaces. | A material story needs to result in a distinct working screen. |
| [Mélange](https://github.com/savq/melange-nvim) | Warm control flow, cool data, and a broad set of ports. | Warm/cool syntax semantics alone are not original. |
| [Vague](https://github.com/vague-theme/vague.nvim) | Near-neutral dark surfaces with muted pastel syntax. | The background needs enough hue to remain identifiable. |
| [Poimandres](https://github.com/olivercederborg/poimandres.nvim) | A cool, restrained accent family on a deep dark foundation. | Reduced color count alone is not a unique concept. |
| [Oxocarbon](https://github.com/nyoom-engineering/oxocarbon.nvim) | Industrial greys and luminous colors drawn from IBM's palette. | The base and accents need a different visual relationship. |
| [Rosebones](https://github.com/zenbones-theme/zenbones.nvim/blob/main/lua/rosebones/palette.lua) | A contrast-oriented Rosé Pine interpretation on a violet ground. | A related rose name cannot be treated as evidence of an unused palette. |

Focused searches for Morello as a terminal or editor colorscheme did not surface an exact match. Search indexing is incomplete; this does not establish exclusive naming rights or worldwide uniqueness.

## Adoption hypothesis

Morello has a plausible reason to be tried: its dark cherry background is recognizable in an ordinary code screenshot, its main syntax relationships are easy to describe, and its color specification is shared across two editors and four terminals. The comment contrast and UI state checks give people a reason to keep using it after the first screenshot.

None of that predicts that it will exceed Dracula, Gruvbox, Nord, or Rosé Pine. Existing themes have years of maintenance, ports, community participation, and visibility. The next useful evidence would be preference comparisons with names hidden and actual use over several days. No user study or retention data has been collected for this palette.

A distinctly red background will also be a reason for some people to decline it. That tradeoff is intentional: reducing the color until it looks neutral would weaken the identity being tested.

"""Run inside Kitty's Python environment: kitty +runpy '...run_path...'."""
from pathlib import Path
import json
from kitty.config import load_config

root = Path(__file__).resolve().parents[1]
for suffix in ('', '-light'):
    data = json.loads((root / f'palette{suffix}.json').read_text())
    errors = []
    options = load_config(str(root / f'ports/kitty/kitty{suffix}.conf'), accumulate_bad_lines=errors)
    assert not errors, errors
    for name, role in {
        'foreground': 'fg', 'background': 'bg', 'cursor': 'cursor', 'cursor_text_color': 'bg',
        'selection_foreground': 'fg', 'selection_background': 'selection',
        'active_tab_foreground': 'bg', 'active_tab_background': 'func',
        'inactive_tab_foreground': 'muted', 'inactive_tab_background': 'line',
        'mark1_background': 'func', 'mark2_background': 'keyword', 'mark3_background': 'constant',
    }.items():
        assert int(getattr(options, name)) == int(data['colors'][role][1:], 16), name
    for index, color in enumerate(data['ansi']):
        assert int(getattr(options, f'color{index}')) == int(color[1:], 16)
print('Kitty native parser: both variants, tab/cursor/selection/mark colors and ANSI passed')

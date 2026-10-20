"""Verify contrast, TOML parsing, and color agreement across all three ports.

Run with Python 3.11+: python scripts/verify.py
No packages or network access required. This is not a terminal runtime test.
"""
from pathlib import Path
import json
import math
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]
def luminance(hex_color):
    rgb = [int(hex_color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return sum(c * w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(fg, bg):
    low, high = sorted((luminance(fg), luminance(bg)))
    return (high + 0.05) / (low + 0.05)


def oklch(hex_color):
    rgb = [int(hex_color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b) ** (1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b) ** (1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b) ** (1/3)
    lightness = 0.2104542553*l + 0.7936177850*m - 0.0040720468*s
    a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s
    b = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s
    return {'L': round(lightness, 4), 'C': round(math.hypot(a, b), 4),
            'h': round(math.degrees(math.atan2(b, a)) % 360, 2)}


def verify(variant):
    suffix = '-light' if variant == 'light' else ''
    data = json.loads((ROOT / f'palette{suffix}.json').read_text(encoding='utf-8'))
    p, ansi = data['colors'], data['ansi']
    checks = []


    def check(label, foreground, background, threshold=4.5):
        ratio = contrast(foreground, background)
        checks.append({'pair': label, 'foreground': foreground, 'background': background,
                       'ratio': round(ratio, 4), 'threshold': threshold, 'pass': ratio >= threshold})
        assert ratio >= threshold, f'{label}: {ratio:.4f} < {threshold}'


    assert len(ansi) == 16
    for c in list(p.values()) + ansi:
        assert re.fullmatch(r'#[0-9A-F]{6}', c), f'Invalid sRGB HEX: {c}'

    core = ['fg', 'muted', 'bright', 'keyword', 'string', 'func', 'variable',
            'constant', 'comment', 'type', 'operator', 'punctuation', 'error', 'warning', 'info', 'hint']
    for role in core:
        surfaces = ['bg', 'panel', 'line', 'float']
        if variant == 'light':
            surfaces += ['selection', 'diff_add', 'diff_change', 'diff_delete', 'diff_text']
        for surface in surfaces:
            check(f'{role} on {surface}', p[role], p[surface])
    for i, color in enumerate(ansi):
        if i not in data.get('ansi_utility_indices', [0]):
            for surface in ['bg', 'panel', 'line', 'float']:
                check(f'ANSI {i} on {surface}', color, p[surface])

    for label, fg, bg in [
        ('selected text', 'fg', 'selection'), ('search match', 'search_fg', 'search_bg'),
        ('current match', 'search_current_fg', 'search_current_bg'), ('cursor cell', 'bg', 'cursor'),
        ('selected completion/tab', 'bg', 'func'), ('substitute', 'bg', 'constant'),
        ('current line number', 'focus', 'line'),
        ('diff added', 'fg', 'diff_add'), ('diff changed', 'fg', 'diff_change'),
        ('diff deleted', 'error', 'diff_delete'), ('diff changed word', 'fg', 'diff_text'),
    ]:
        check(label, p[fg], p[bg])
    check('active focus border', p['focus'], p['bg'], 3.0)

    colors = tomllib.loads((ROOT/f'ports/alacritty/alacritty{suffix}.toml').read_text(encoding='utf-8'))['colors']
    keys = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    assert [colors[section][key] for section in ['normal', 'bright'] for key in keys] == ansi
    assert colors['primary']['background'] == p['bg']
    assert colors['primary']['foreground'] == p['fg']
    assert colors['selection'] == {'text': p['fg'], 'background': p['selection']}
    assert colors['search']['matches'] == {'foreground': p['search_fg'], 'background': p['search_bg']}
    assert colors['search']['focused_match'] == {'foreground': p['search_current_fg'], 'background': p['search_current_bg']}
    assert colors['cursor'] == {'text': p['bg'], 'cursor': p['cursor']}

    kitty = {}
    for line in (ROOT/f'ports/kitty/kitty{suffix}.conf').read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            key, value = line.split()
            assert key not in kitty, f'Duplicate Kitty setting: {key}'
            kitty[key] = value
    assert [kitty[f'color{i}'] for i in range(16)] == ansi
    for key, token in {'background':'bg', 'foreground':'fg', 'cursor':'cursor',
                       'cursor_text_color':'bg', 'selection_foreground':'fg',
                       'selection_background':'selection', 'active_border_color':'focus',
                       'inactive_border_color':'border', 'active_tab_background':'func',
                       'active_tab_foreground':'bg'}.items():
        assert kitty[key] == p[token], f'Kitty drift: {key}'

    lua = (ROOT/f'lua/morello/palette{suffix}.lua').read_text(encoding='utf-8')
    lua_colors = dict(re.findall(r'^  ([a-z_]+) = "(#[0-9A-F]{6})",$', lua, re.M))
    lua_ansi = {int(i): value for i, value in re.findall(r'\[(\d+)\] = "(#[0-9A-F]{6})"', lua)}
    assert lua_colors == p, 'Lua palette differs from palette.json'
    assert [lua_ansi[i] for i in range(16)] == ansi, 'Lua ANSI differs from palette.json'

    decorative = [{'role':key, 'hex':p[key], 'ratio_on_bg':round(contrast(p[key],p['bg']),4),
                   'purpose':'Decorative only; not covered by the core-text AA claim'}
                  for key in ['subdued','border']]
    report = {
        'method':'WCAG 2.x sRGB relative luminance; no rounded ratios used for pass/fail',
        'scope':'Specified foreground/background pairs on opaque surfaces only; not whole-application conformance',
        'text_threshold':4.5, 'checks_passed':len(checks), 'checks':checks,
        'decorative_exceptions':decorative,
        'ansi_exceptions':[{'index':i, 'hex':ansi[i], 'ratio_on_bg':round(contrast(ansi[i],p['bg']),4),
                          'purpose':'Utility slot; unsuitable for text on the default background'}
                          for i in data.get('ansi_utility_indices', [0])],
        'oklch':{role:oklch(value) for role,value in p.items()},
        'ports':{'toml_parse':'passed', 'ansi_16_agreement':'passed', 'lua_palette_agreement':'passed',
                 'native_runtime':'Run tests/headless.lua in Neovim; terminal apps must be checked separately'},
    }
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/f'docs/contrast-report{suffix}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'{variant}: {len(checks)} contrast checks passed; TOML parsed; ANSI and palette agree across all ports.')
    print(f'Core default text: {contrast(p["fg"],p["bg"]):.2f}:1; comments on float: {contrast(p["comment"],p["float"]):.2f}:1.')


for variant in ('dark', 'light'):
    verify(variant)

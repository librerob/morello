"""Reject blank or incomplete terminal captures before publishing them.

Requires Pillow. Run: python scripts/check_capture.py image.png dark|light
"""
from collections import Counter
from pathlib import Path
import json
import sys

from PIL import Image


def validate(path, variant):
    root = Path(__file__).resolve().parents[1]
    suffix = '-light' if variant == 'light' else ''
    palette = json.loads((root / f'palette{suffix}.json').read_text())['colors']
    with Image.open(path) as source:
        image = source.convert('RGB')
    assert image.width >= 600 and image.height >= 350, 'Capture is too small'
    counts = Counter({color: count for count, color in image.getcolors(image.width * image.height)})
    def pixels(role):
        color = tuple(bytes.fromhex(palette[role][1:]))
        return counts[color]
    assert len(counts) >= 64, 'Capture is blank or has no rendered text'
    assert pixels('bg') >= image.width * image.height * 0.2, 'Theme background is missing'
    assert pixels('fg') >= 100, 'Editor text is missing'
    assert sum(pixels(role) for role in ('keyword', 'string', 'func')) >= 50, 'Syntax colors are missing'


if __name__ == '__main__':
    assert len(sys.argv) == 3 and sys.argv[2] in ('dark', 'light')
    validate(Path(sys.argv[1]), sys.argv[2])

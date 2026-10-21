"""Regression checks for the guard that prevents publishing blank screenshots."""
from pathlib import Path
import importlib.util
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_capture', ROOT / 'scripts/check_capture.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

for variant in ('dark', 'light'):
    suffix = '-light' if variant == 'light' else ''
    for view in ('lua', 'python', 'typescript', 'ui'):
        path = ROOT / f'assets/neovim{suffix}-{view}.png'
        assert path.is_file(), f'Missing preview: {path}'
        guard.validate(path, variant)
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'blank.png'
    for color in ('#000000', '#2B1B23', '#F8F0F3'):
        Image.new('RGB', (800, 500), color).save(path)
        try:
            guard.validate(path, 'dark')
        except AssertionError:
            pass
        else:
            raise AssertionError(f'Accepted blank screenshot {color}')
print('All eight published previews passed; blank black and theme-colored frames were rejected')

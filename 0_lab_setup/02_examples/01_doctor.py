"""Read-only диагностика видимой среды: ничего не устанавливает и не меняет.

Запуск из корня: uv run python 0_lab_setup/02_examples/01_doctor.py
"""
import importlib.util
import os
import platform
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
print('Python:', platform.python_version())
print('OS:', platform.platform())
print('Logical CPUs:', os.cpu_count())

# Объём RAM: всего и сколько сейчас можно занять без вытеснения программ.
meminfo = Path('/proc/meminfo')
if meminfo.exists():
    for line in meminfo.read_text().splitlines():
        if line.startswith(('MemTotal:', 'MemAvailable:')):
            print(line)

free_gib = shutil.disk_usage(ROOT).free / 2**30
print('Disk available GiB:', round(free_gib, 1))

# Файлы-устройства видеокарты в Linux; в контейнере их может не быть.
dri = Path('/dev/dri')
print('GPU nodes:', [str(p) for p in dri.glob('*')] if dri.exists()
      else 'not visible')

for name in ('numpy', 'sklearn', 'torch', 'transformers', 'peft'):
    found = importlib.util.find_spec(name)
    print(name + ':', 'installed' if found
          else 'not installed in this Python')

if importlib.util.find_spec('torch'):
    import torch
    print('PyTorch:', torch.__version__)
    print('XPU available:', torch.xpu.is_available())
    print('CUDA available:', torch.cuda.is_available())
print('No GPU required for CPU course profile.')

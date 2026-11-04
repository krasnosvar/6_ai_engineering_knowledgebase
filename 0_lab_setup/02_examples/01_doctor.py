"""Read-only диагностика видимой среды. Запуск из корня: uv run python 0_lab_setup/02_examples/01_doctor.py."""
import importlib.util
import os
import platform
import shutil
from pathlib import Path

print('Python:', platform.python_version())
print('OS:', platform.platform())
print('Logical CPUs:', os.cpu_count())
if Path('/proc/meminfo').exists():
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith(('MemTotal:', 'MemAvailable:')):
            print(line)
print('Disk available GiB:', round(shutil.disk_usage(Path(__file__).resolve().parents[2]).free/2**30, 1))
print('GPU nodes:', [str(p) for p in Path('/dev/dri').glob('*')] if Path('/dev/dri').exists() else 'not visible')
for name in ('numpy', 'sklearn', 'torch', 'transformers', 'peft'):
    print(name + ':', 'installed' if importlib.util.find_spec(name) else 'not installed in this Python')
if importlib.util.find_spec('torch'):
    import torch
    print('PyTorch:', torch.__version__)
    print('XPU available:', torch.xpu.is_available())
    print('CUDA available:', torch.cuda.is_available())
print('No GPU required for CPU course profile.')

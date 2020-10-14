import os
from pathlib import Path


def path(filename: str) -> Path:
    return (Path(__file__).parent / filename).absolute()


hook = f'''import os

os.environ['DMONITOR_STATHAT_KEY'] = '{os.getenv('DMONITOR_STATHAT_KEY', '')}'
'''

path('hook.py').write_text(hook, encoding='utf-8')

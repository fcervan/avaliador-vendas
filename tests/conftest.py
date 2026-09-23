"""Garante que a raiz do projeto esteja no sys.path (imports `from src.*`)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

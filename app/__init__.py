# app/__init__.py
import os
import sys
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent))
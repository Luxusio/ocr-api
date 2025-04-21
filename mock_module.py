import re
import sys
import types
from typing import Dict, Any
import importlib.util


class DummyClass:
    pass

def dummy_function():
    pass

def mock_module(module_name: str, module: Dict[str, Any] | None = None):
    if module is None:
        module = {}

    dummy_module = types.ModuleType(module_name)
    for name, obj in module.items():
        setattr(dummy_module, name, obj)
    dummy_module.__name__ = module_name
    dummy_module.__file__ = f"{module_name}.py"
    dummy_module.__package__ = module_name
    dummy_module.__path__ = [f"{module_name}.py"]
    dummy_module.__spec__ = importlib.util.spec_from_loader(
        module_name,
        loader=None,
        origin=dummy_module.__file__
    )
    sys.modules[module_name] = dummy_module


def mock_import(imports_str):
    """
    Parse a string of import statements and call mock_module for each.

    - from x.y import a, b as c
      -> mock_module('x.y', {'a': dummy_func_or_class, 'b': dummy_func_or_class})
    - import x.y.z as alias, p.q
      -> mock_module('x.y.z', {})
         mock_module('p.q', {})
    """
    for line in imports_str.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Handle "from ... import ..." statements
        from_match = re.match(r'^from\s+([\w\.]+)\s+import\s+(.+)$', line)
        if from_match:
            pkg, names_str = from_match.groups()
            names = [n.strip() for n in names_str.split(',')]
            mapping = {}
            for name in names:
                # Strip alias if present
                name_match = re.match(r'^(\w+)(?:\s+as\s+\w+)?$', name)
                if not name_match:
                    raise ValueError(f"Cannot parse import name: {name}")
                orig_name = name_match.group(1)
                # Choose dummy_class if name looks like a class (capitalized), else dummy_func
                if orig_name[0].isupper():
                    mapping[orig_name] = DummyClass
                else:
                    mapping[orig_name] = dummy_function
            mock_module(pkg, mapping)
            continue

        # Handle "import ..." statements (with optional alias, multiple packages)
        import_match = re.match(r'^import\s+(.+)$', line)
        if import_match:
            parts = [p.strip() for p in import_match.group(1).split(',')]
            for part in parts:
                # Extract actual module name before any alias
                part_match = re.match(r'^([\w\.]+)(?:\s+as\s+\w+)?$', part)
                if not part_match:
                    raise ValueError(f"Cannot parse import part: {part}")
                pkg_name = part_match.group(1)
                mock_module(pkg_name, {})
            continue

        raise ValueError(f"Unsupported import statement: {line}")

def import_dummy_module():
    mock_import('''
    from paddleocr import PaddleOCR
    import pydensecrf
    from pydensecrf.densecrf import DenseCRF
    from pydensecrf.utils import compute_unary, unary_from_softmax
    from onnxruntime import InferenceSession
    import langdetect
    from omegaconf import OmegaConf
    from manga_ocr import MangaOcr
    from transformers import logging
    import deepl
    import ctranslate2
    import groq
    from google import genai
    from google.genai import types
    from freetype import Face
    from dotenv import load_dotenv
    import langcodes
    import regex
    import py3langid
    import pyclipper
    from timm.layers import trunc_normal_, AvgPool2dSame, DropPath, Mlp, GlobalResponseNormMlp, LayerNorm2d, LayerNorm, \
        create_conv2d, get_act_layer, make_divisible, to_ntuple
    import safetensors
    import safetensors.torch
    import pandas
    import aiohttp
    from langcodes import Language, closest_supported_match, standardize_tag
    import tiktoken
    from rich.console import Console
    from rich.panel import Panel
    import sentencepiece
    from hyphen import Hyphenator
    from hyphen.dictools import LANGUAGES
    from torchvision.models import resnet34
    from skimage import io
    import torchvision
    from torchvision.transforms import ToTensor
    ''')


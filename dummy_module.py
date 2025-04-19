import sys
import types
from typing import Dict, Any
import importlib.util


class DummyClass:
    pass

def dummy_function():
    pass

def add_module(module_name: str, module: Dict[str, Any] | None = None):
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

def import_dummy_module():
    add_module('paddleocr', {
        'PaddleOCR': DummyClass
    })

    add_module('pydensecrf')
    add_module('pydensecrf.densecrf', {
        'DenseCRF': DummyClass
    })
    add_module('pydensecrf.utils', {
        'compute_unary': dummy_function,
        'unary_from_softmax': dummy_function,
    })

    add_module('onnxruntime', {
        'InferenceSession': DummyClass
    })

    add_module('langdetect')

    add_module('omegaconf', {
        'OmegaConf': DummyClass,
    })

    add_module('manga_ocr', {
        'MangaOcr': DummyClass,
    })

    add_module('transformers', {
        'logging': dummy_function,
    })

    add_module('deepl')

    add_module('ctranslate2')

    add_module('groq')

    add_module('google', {
        'genai': dummy_function,
    })

    add_module('google.genai', {
        'types': DummyClass,
    })

    add_module('freetype', {
        'Face': DummyClass,
    })

    add_module('dotenv', {
        'load_dotenv': dummy_function,
    })

    add_module('langcodes')

    add_module('regex')

    add_module('py3langid')

    add_module('pyclipper')

    add_module('timm.layers', {
        'trunc_normal_': dummy_function,
        'AvgPool2dSame': dummy_function,
        'DropPath': dummy_function,
        'Mlp': dummy_function,
        'GlobalResponseNormMlp': dummy_function,
        'LayerNorm2d': dummy_function,
        'LayerNorm': dummy_function,
        'create_conv2d': dummy_function,
        'get_act_layer': dummy_function,
        'make_divisible': dummy_function,
        'to_ntuple': dummy_function,
    })

    add_module('safetensors')
    add_module('safetensors.torch')

    add_module('pandas')

    add_module('aiohttp')

    add_module('langcodes', {
        'Language': DummyClass,
        'closest_supported_match': dummy_function,
        'standardize_tag': dummy_function,
    })

    add_module('tiktoken')

    add_module('rich.console', {
        'Console': DummyClass,
    })
    add_module('rich.panel', {
        'Panel': DummyClass,
    })

    add_module('sentencepiece')

    add_module('hyphen', {
        'Hyphenator': DummyClass,
    })
    add_module('hyphen.dictools', {
        'LANGUAGES': DummyClass,
    })

"""bid-writer-pro 投标/标书写作助手。"""

__version__ = "0.1.0"
__author__ = "bid-writer-pro contributors"

__all__ = ["__version__", "generate", "list_templates", "get_template"]

from .generator import generate
from .templates import get_template, list_templates

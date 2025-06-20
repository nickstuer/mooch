"""mooch package initialization."""

from .config.config import Config
from .utils.file import File
from .utils.location import Location
from .utils.require import Require

__all__ = ["Config", "File", "Location", "Require"]

__version__ = "1.0.0dev0"

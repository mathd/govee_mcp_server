"""
Govee MCP Server - A Model Context Protocol server for controlling Govee LED devices.

This package provides a complete interface for controlling Govee LED devices through both
an MCP server implementation and a CLI interface.
"""

from .api import GoveeAPI
from .config import GoveeConfig, load_config
from .exceptions import (
    GoveeError,
    GoveeAPIError,
    GoveeConfigError,
    GoveeValidationError,
    GoveeConnectionError,
    GoveeTimeoutError
)
from .transformers import ColorTransformer
from .interfaces import PowerControl, ColorControl, BrightnessControl

__version__ = "0.1.0"
__all__ = [
    'GoveeAPI',
    'GoveeConfig',
    'load_config',
    'GoveeError',
    'GoveeAPIError',
    'GoveeConfigError',
    'GoveeValidationError',
    'GoveeConnectionError',
    'GoveeTimeoutError',
    'ColorTransformer',
    'PowerControl',
    'ColorControl',
    'BrightnessControl'
]
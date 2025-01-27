from abc import ABC, abstractmethod
from typing import Tuple
from functools import wraps
from .exceptions import GoveeValidationError

def validate_rgb(func):
    """Decorator to validate RGB color values."""
    @wraps(func)
    async def wrapper(self, r: int, g: int, b: int, *args, **kwargs):
        for name, value in [('red', r), ('green', g), ('blue', b)]:
            if not isinstance(value, int):
                raise GoveeValidationError(f"{name} value must be an integer")
            if not 0 <= value <= 255:
                raise GoveeValidationError(f"{name} value must be between 0-255")
        return await func(self, r, g, b, *args, **kwargs)
    return wrapper

class PowerControl(ABC):
    """Interface for power control capabilities."""
    @abstractmethod
    async def set_power(self, state: bool) -> Tuple[bool, str]:
        """
        Set device power state.
        
        Args:
            state: True for on, False for off
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        pass

    @abstractmethod
    async def get_power_state(self) -> Tuple[bool, str]:
        """
        Get current power state.
        
        Returns:
            Tuple of (is_on: bool, message: str)
        """
        pass

class ColorControl(ABC):
    """Interface for color control capabilities."""
    @abstractmethod
    @validate_rgb
    async def set_color(self, r: int, g: int, b: int) -> Tuple[bool, str]:
        """
        Set device color using RGB values.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        pass

    @abstractmethod
    async def get_color(self) -> Tuple[Tuple[int, int, int], str]:
        """
        Get current color values.
        
        Returns:
            Tuple of ((r, g, b): Tuple[int, int, int], message: str)
        """
        pass

class BrightnessControl(ABC):
    """Interface for brightness control capabilities."""
    @abstractmethod
    async def set_brightness(self, level: int) -> Tuple[bool, str]:
        """
        Set device brightness level.
        
        Args:
            level: Brightness level (0-100)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        pass

    @abstractmethod
    async def get_brightness(self) -> Tuple[int, str]:
        """
        Get current brightness level.
        
        Returns:
            Tuple of (level: int, message: str)
        """
        pass
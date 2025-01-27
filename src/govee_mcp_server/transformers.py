from typing import Tuple, Dict, Any
from .exceptions import GoveeValidationError

class ColorTransformer:
    """Handle color transformations and validations."""
    
    @staticmethod
    def validate_rgb(r: int, g: int, b: int) -> None:
        """
        Validate RGB color values.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            
        Raises:
            GoveeValidationError: If values are invalid
        """
        for name, value in [('red', r), ('green', g), ('blue', b)]:
            if not isinstance(value, int):
                raise GoveeValidationError(f"{name} value must be an integer")
            if not 0 <= value <= 255:
                raise GoveeValidationError(f"{name} value must be between 0-255")

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """
        Convert RGB values to hexadecimal color code.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            
        Returns:
            str: Hexadecimal color code
        """
        ColorTransformer.validate_rgb(r, g, b)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hexadecimal color code to RGB values.
        
        Args:
            hex_color: Hexadecimal color code (e.g., '#ff00ff' or 'ff00ff')
            
        Returns:
            Tuple[int, int, int]: RGB values
            
        Raises:
            GoveeValidationError: If hex color format is invalid
        """
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) != 6:
            raise GoveeValidationError("Invalid hex color format")
        
        try:
            r = int(hex_color[:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:], 16)
            return (r, g, b)
        except ValueError:
            raise GoveeValidationError("Invalid hex color format")

    @staticmethod
    def to_api_payload(r: int, g: int, b: int) -> Dict[str, Any]:
        """
        Convert RGB values to API payload format.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            
        Returns:
            Dict[str, Any]: API payload
        """
        ColorTransformer.validate_rgb(r, g, b)
        return {
            "color": {
                "r": r,
                "g": g,
                "b": b
            }
        }
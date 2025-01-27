from pathlib import Path
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from typing import Optional

@dataclass
class GoveeConfig:
    """Configuration class for Govee API settings."""
    api_key: str
    device_id: str
    sku: str

class GoveeConfigError(Exception):
    """Configuration-related errors for Govee MCP server."""
    pass

def load_config() -> GoveeConfig:
    """
    Load and validate configuration from environment variables.
    
    Returns:
        GoveeConfig: Configuration object with API settings
        
    Raises:
        GoveeConfigError: If required environment variables are missing
    """
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    load_dotenv(env_path)
    
    api_key = os.getenv('GOVEE_API_KEY')
    device_id = os.getenv('GOVEE_DEVICE_ID')
    sku = os.getenv('GOVEE_SKU')
    
    missing = []
    if not api_key:
        missing.append('GOVEE_API_KEY')
    if not device_id:
        missing.append('GOVEE_DEVICE_ID')
    if not sku:
        missing.append('GOVEE_SKU')
        
    if missing:
        raise GoveeConfigError(f"Missing required environment variables: {', '.join(missing)}")
        
    return GoveeConfig(
        api_key=api_key,
        device_id=device_id,
        sku=sku
    )
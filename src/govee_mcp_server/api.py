import aiohttp
from typing import Optional, Dict, Any, Tuple
import asyncio
from time import time
from .exceptions import (
    GoveeError,
    GoveeAPIError,
    GoveeConnectionError,
    GoveeTimeoutError
)
from .interfaces import PowerControl, ColorControl, BrightnessControl
from .transformers import ColorTransformer
from .config import GoveeConfig

class GoveeAPI(PowerControl, ColorControl, BrightnessControl):
    """
    Govee API client implementing device control interfaces.
    
    Includes connection pooling, request timeouts, and retries.
    """
    
    BASE_URL = "https://openapi.api.govee.com"
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    REQUEST_TIMEOUT = 10  # seconds

    def __init__(self, config: GoveeConfig):
        """
        Initialize API client with configuration.
        
        Args:
            config: GoveeConfig instance with API credentials
        """
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self._transformer = ColorTransformer()
        
    async def _ensure_session(self) -> None:
        """Ensure aiohttp session exists or create a new one."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "Govee-API-Key": self.config.api_key,
                    "Content-Type": "application/json"
                },
                timeout=aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
            )

    async def close(self) -> None:
        """Close the API session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Tuple[Dict[str, Any], str]:
        """
        Make HTTP request with retries and error handling.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments
            
        Returns:
            Tuple[Dict[str, Any], str]: API response data and message
            
        Raises:
            GoveeAPIError: On API errors
            GoveeConnectionError: On connection issues
            GoveeTimeoutError: On request timeout
        """
        await self._ensure_session()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.request(
                    method,
                    f"{self.BASE_URL}/{endpoint}",
                    **kwargs
                ) as response:
                    data = await response.json()
                    
                    if response.status != 200:
                        raise GoveeAPIError(
                            f"API error: {response.status} - {data.get('message', 'Unknown error')}"
                        )
                    
                    return data, data.get('message', 'Success')
                    
            except asyncio.TimeoutError:
                if attempt == self.MAX_RETRIES - 1:
                    raise GoveeTimeoutError(f"Request timed out after {self.REQUEST_TIMEOUT}s")
            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise GoveeConnectionError(f"Connection error: {str(e)}")
            
            await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
        
        raise GoveeAPIError("Max retries exceeded")

    async def set_power(self, state: bool) -> Tuple[bool, str]:
        """Implement PowerControl.set_power"""
        try:
            _, message = await self._make_request(
                "POST",
                "router/api/v1/device/control",
                json={
                    "requestId": str(int(time())),  # Using timestamp as requestId
                    "payload": {
                        "sku": self.config.sku,
                        "device": self.config.device_id,
                        "capability": {
                            "type": "devices.capabilities.on_off",
                            "instance": "powerSwitch",
                            "value": 1 if state else 0
                        }
                    }
                }
            )
            return True, message
        except GoveeError as e:
            return False, str(e)

    async def get_power_state(self) -> Tuple[bool, str]:
        """Implement PowerControl.get_power_state"""
        try:
            data, message = await self._make_request(
                "GET",
                f"devices/state",
                params={
                    "device": self.config.device_id,
                    "model": self.config.sku
                }
            )
            return data.get('powerState') == 'on', message
        except GoveeError as e:
            return False, str(e)

    async def set_color(self, r: int, g: int, b: int) -> Tuple[bool, str]:
        """Implement ColorControl.set_color"""
        try:
            color_value = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
            
            _, message = await self._make_request(
                "POST",
                "router/api/v1/device/control",
                json={
                    "requestId": str(int(time())),
                    "payload": {
                        "sku": self.config.sku,
                        "device": self.config.device_id,
                        "capability": {
                            "type": "devices.capabilities.color_setting",
                            "instance": "colorRgb",
                            "value": color_value
                        }
                    }
                }
            )
            return True, message
        except GoveeError as e:
            return False, str(e)

    async def get_color(self) -> Tuple[Tuple[int, int, int], str]:
        """Implement ColorControl.get_color"""
        try:
            data, message = await self._make_request(
                "GET",
                f"devices/state",
                params={
                    "device": self.config.device_id,
                    "model": self.config.sku
                }
            )
            color = data.get('color', {})
            return (
                color.get('r', 0),
                color.get('g', 0),
                color.get('b', 0)
            ), message
        except GoveeError as e:
            return (0, 0, 0), str(e)

    async def set_brightness(self, level: int) -> Tuple[bool, str]:
        """Implement BrightnessControl.set_brightness"""
        if not 0 <= level <= 100:
            return False, "Brightness must be between 0-100"
            
        try:
            _, message = await self._make_request(
                "POST",
                "router/api/v1/device/control",
                json={
                    "requestId": str(int(time())),
                    "payload": {
                        "sku": self.config.sku,
                        "device": self.config.device_id,
                        "capability": {
                            "type": "devices.capabilities.range",
                            "instance": "brightness",
                            "value": level
                        }
                    }
                }
            )
            return True, message
        except GoveeError as e:
            return False, str(e)

    async def get_brightness(self) -> Tuple[int, str]:
        """Implement BrightnessControl.get_brightness"""
        try:
            data, message = await self._make_request(
                "GET",
                f"devices/state",
                params={
                    "device": self.config.device_id,
                    "model": self.config.sku
                }
            )
            return data.get('brightness', 0), message
        except GoveeError as e:
            return 0, str(e)
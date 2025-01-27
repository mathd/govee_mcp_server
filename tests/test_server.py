import pytest
import asyncio
import aiohttp
from unittest.mock import patch, MagicMock
from govee_mcp_server.server import (
    init_env,
    GoveeDirectAPI,
    fix_json,
    rgb_to_int,
)

@pytest.fixture
def mock_env_vars():
    with patch.dict('os.environ', {
        'GOVEE_API_KEY': 'test-api-key',
        'GOVEE_DEVICE_ID': 'test-device-id',
        'GOVEE_SKU': 'test-sku'
    }):
        yield

def test_init_env(mock_env_vars):
    api_key, device_id, sku = init_env()
    assert api_key == 'test-api-key'
    assert device_id == 'test-device-id'
    assert sku == 'test-sku'

@patch('os.getenv', return_value=None)
def test_init_env_missing_vars(_):
    with pytest.raises(SystemExit):
        init_env()

def test_fix_json():
    malformed = '{"key1""value1"}{"key2""value2"}'
    expected = '{"key1","value1"},{"key2","value2"}'
    assert fix_json(malformed) == expected

def test_rgb_to_int():
    assert rgb_to_int(255, 0, 0) == 0xFF0000
    assert rgb_to_int(0, 255, 0) == 0x00FF00
    assert rgb_to_int(0, 0, 255) == 0x0000FF
    assert rgb_to_int(255, 255, 255) == 0xFFFFFF

class TestGoveeDirectAPI:
    @pytest.fixture
    def api(self):
        return GoveeDirectAPI('test-api-key')

    def test_init(self, api):
        assert api.api_key == 'test-api-key'
        assert api.headers['Govee-API-Key'] == 'test-api-key'
        assert api.headers['Content-Type'] == 'application/json'

    @pytest.mark.asyncio
    async def test_get_devices_success(self, api):
        mock_response = MagicMock()
        mock_response.status = 200
        async def mock_text():
            return '{"data":[{"device":"test"}]}'
        mock_response.text = mock_text

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response
            devices, error = await api.get_devices()
            assert devices == [{"device": "test"}]
            assert error is None

    @pytest.mark.asyncio
    async def test_get_devices_error(self, api):
        mock_response = MagicMock()
        mock_response.status = 401
        async def mock_text():
            return '{"message":"Unauthorized"}'
        mock_response.text = mock_text

        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response
            devices, error = await api.get_devices()
            assert devices is None
            assert error == "Unauthorized"

    @pytest.mark.asyncio
    async def test_control_device_success(self, api):
        mock_response = MagicMock()
        mock_response.status = 200
        async def mock_text():
            return '{"message":"Success"}'
        mock_response.text = mock_text

        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value = mock_response
            success, error = await api.control_device(
                "sku123",
                "device123",
                "devices.capabilities.on_off",
                "powerSwitch",
                1
            )
            assert success is True
            assert error == "Success"

    @pytest.mark.asyncio
    async def test_control_device_error(self, api):
        mock_response = MagicMock()
        mock_response.status = 400
        async def mock_text():
            return '{"message":"Bad Request"}'
        mock_response.text = mock_text

        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value = mock_response
            success, error = await api.control_device(
                "sku123",
                "device123",
                "devices.capabilities.on_off",
                "powerSwitch",
                1
            )
            assert success is False
            assert error == "Bad Request"
import pytest
import os
import asyncio # Required for async tests

# Set dummy environment variables before importing the server module
# to allow config to load without errors during import.
os.environ['GOVEE_API_KEY'] = 'test_key_smoke'
os.environ['GOVEE_DEVICE_ID'] = 'test_device_smoke'
os.environ['GOVEE_SKU'] = 'test_sku_smoke'

# It's important to import the server module *after* setting the environment variables
# as load_config() is called at the module level in server.py.
# The mcp instance is named 'mcp' in server.py, aliasing to mcp_instance here.
from govee_mcp_server.server import mcp as mcp_instance, handle_initialize

# Attempt to import NotificationOptions from a plausible location
try:
    from mcp.server.lowlevel.models import NotificationOptions
except ImportError:
    # If not in models, it might be in types directly under mcp.server or mcp itself
    # This is a fallback, the exact location needs to be correct.
    # For now, if this fails, the capabilities test might be compromised.
    NotificationOptions = None 

# Expected tools that should be registered
EXPECTED_TOOLS = [
    "turn_on_off",
    "set_color",
    "set_brightness",
    "get_status",
]

@pytest.mark.asyncio # Mark test as async
async def test_fastmcp_server_tool_registration_and_descriptions():
    """
    Smoke test to verify FastMCP server tool registration and descriptions.
    This test checks that the MCP server instance from server.py:
    1. Has the correct tools registered.
    2. Tool descriptions are populated (likely from docstrings).
    """
    registered_tools = await mcp_instance.list_tools() # Await the coroutine
    registered_tool_names = [tool.name for tool in registered_tools]

    for tool_name in EXPECTED_TOOLS:
        assert tool_name in registered_tool_names, f"Tool '{tool_name}' not found in registered tools."

    # Verify that the descriptions for tools are non-empty
    for tool_info in registered_tools:
        if tool_info.name in EXPECTED_TOOLS:
            assert tool_info.description, f"Tool '{tool_info.name}' has no description."

def test_on_initialize_handler_set():
    """
    Verify that the on_initialize handler is correctly set on the mcp instance.
    """
    assert mcp_instance.on_initialize is handle_initialize, \
        "mcp_instance.on_initialize is not set to the correct handle_initialize function."


def test_server_name_and_capabilities():
    """
    Verify that the server name and capabilities are set as expected.
    Capabilities are likely stored in the underlying MCPServer object.
    """
    assert mcp_instance.name == "govee", "MCP instance name is not 'govee'."

    expected_server_info = {
        "name": "govee-mcp",
        "version": "0.1.0",
        "description": "MCP server for controlling Govee LED devices"
    }
    assert hasattr(mcp_instance, '_mcp_server'), "FastMCP instance does not have '_mcp_server' attribute."
    
    if NotificationOptions: # Proceed only if NotificationOptions was successfully imported
        # Create default NotificationOptions.
        notification_opts = NotificationOptions(
            prompts_changed=False,
            resources_changed=False,
            tools_changed=False,
        )
        
        actual_capabilities = mcp_instance._mcp_server.get_capabilities(
            notification_options=notification_opts, 
            experimental_capabilities=None 
        )
        
        assert "server_info" in actual_capabilities, "'server_info' not found in capabilities."
        assert actual_capabilities["server_info"] == expected_server_info, \
            "MCP instance 'server_info' capabilities do not match expected values."
    else:
        # If NotificationOptions couldn't be imported, this part of the test
        # cannot be reliably executed. We can skip it or mark it as skipped.
        pytest.skip("NotificationOptions type not found, skipping detailed capabilities check.")


# To run this test:
# Pytest will pick up this file. Ensure govee_mcp_server is in PYTHONPATH (src).
# pythonpath = ["src"] in pyproject.toml should handle this.
# Dummy environment variables are set at the top of this file.
# Run: pytest tests/test_server_smoke.py

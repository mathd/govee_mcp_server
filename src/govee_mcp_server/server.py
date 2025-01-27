#!/usr/bin/env python3
import sys
from mcp.server.fastmcp import FastMCP
from govee_mcp_server.config import load_config
from govee_mcp_server.api import GoveeAPI
from govee_mcp_server.exceptions import GoveeError

# Initialize FastMCP server with WARNING log level
mcp = FastMCP(
    "govee",
    capabilities={
        "server_info": {
            "name": "govee-mcp",
            "version": "0.1.0",
            "description": "MCP server for controlling Govee LED devices"
        }
    },
    log_level='WARNING'
)

print("Loading configuration...", file=sys.stderr, flush=True)
try:
    config = load_config()
except GoveeError as e:
    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)

print("Setting up tools...", file=sys.stderr, flush=True)

@mcp.tool("turn_on_off")
async def turn_on_off(power: bool) -> str:
    """
    Turn the LED on or off.
    
    Args:
        power: True for on, False for off
    """
    api = GoveeAPI(config)
    try:
        success, message = await api.set_power(power)
        await api.close()  # Clean up the session
        return message if success else f"Failed: {message}"
    except GoveeError as e:
        await api.close()
        return f"Error: {str(e)}"
    except Exception as e:
        await api.close()
        return f"Unexpected error: {str(e)}"

@mcp.tool("set_color")
async def set_color(red: int, green: int, blue: int) -> str:
    """
    Set the LED color using RGB values.
    
    Args:
        red: Red value (0-255)
        green: Green value (0-255)
        blue: Blue value (0-255)
    """
    api = GoveeAPI(config)
    try:
        success, message = await api.set_color(red, green, blue)
        await api.close()
        return message if success else f"Failed: {message}"
    except GoveeError as e:
        await api.close()
        return f"Error: {str(e)}"
    except Exception as e:
        await api.close()
        return f"Unexpected error: {str(e)}"

@mcp.tool("set_brightness")
async def set_brightness(brightness: int) -> str:
    """
    Set the LED brightness.
    
    Args:
        brightness: Brightness level (0-100)
    """
    api = GoveeAPI(config)
    try:
        success, message = await api.set_brightness(brightness)
        await api.close()
        return message if success else f"Failed: {message}"
    except GoveeError as e:
        await api.close()
        return f"Error: {str(e)}"
    except Exception as e:
        await api.close()
        return f"Unexpected error: {str(e)}"

@mcp.tool("get_status")
async def get_status() -> dict:
    """Get the current status of the LED device."""
    api = GoveeAPI(config)
    try:
        power_state, power_msg = await api.get_power_state()
        color, color_msg = await api.get_color()
        brightness, bright_msg = await api.get_brightness()
        await api.close()
        
        return {
            "power": {
                "state": "on" if power_state else "off",
                "message": power_msg
            },
            "color": {
                "r": color[0],
                "g": color[1],
                "b": color[2],
                "message": color_msg
            },
            "brightness": {
                "level": brightness,
                "message": bright_msg
            }
        }
    except GoveeError as e:
        await api.close()
        return {"error": str(e)}
    except Exception as e:
        await api.close()
        return {"error": f"Unexpected error: {str(e)}"}

async def handle_initialize(params):
    """Handle initialize request"""
    return {
        "protocolVersion": "0.1.0",
        "capabilities": mcp.capabilities
    }

mcp.on_initialize = handle_initialize

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(mcp.run(transport='stdio'))
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)
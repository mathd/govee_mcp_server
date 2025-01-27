import pytest
import sys
import asyncio
from govee_mcp_server.cli import main
from govee_mcp_server.config import load_config, GoveeConfigError

# Delay between commands (in seconds)
DELAY = 1

@pytest.mark.asyncio
async def test_cli_interface():
    """Test CLI interface with real API calls"""
    try:
        # Load actual config from environment
        config = load_config()
        
        # Power on
        sys.argv = ['cli.py', 'power', 'on']
        await main()
        await asyncio.sleep(DELAY)
        
        # Red color
        sys.argv = ['cli.py', 'color', '255', '0', '0']
        await main()
        await asyncio.sleep(DELAY)
        
        # Green color
        sys.argv = ['cli.py', 'color', '0', '255', '0']
        await main()
        await asyncio.sleep(DELAY)
        
        # Blue color
        sys.argv = ['cli.py', 'color', '0', '0', '255']
        await main()
        await asyncio.sleep(DELAY)
        
        # Power off
        sys.argv = ['cli.py', 'power', 'off']
        await main()
        
    except GoveeConfigError as e:
        pytest.skip(f"Skipping test: {str(e)}")
        
    except Exception as e:
        # If we hit rate limits or other API errors, fail with clear message
        pytest.fail(f"API Error: {str(e)}")
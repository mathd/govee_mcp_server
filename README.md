# Govee MCP Server

[![smithery badge](https://smithery.ai/badge/@mathd/govee_mcp_server)](https://smithery.ai/server/@mathd/govee_mcp_server)

An MCP server for controlling Govee LED devices through the Govee API.

## Setup

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
GOVEE_API_KEY=your_api_key_here
GOVEE_DEVICE_ID=your_device_id_here
GOVEE_SKU=your_device_sku_here
```

To get these values:
1. Get your API key from the Govee Developer Portal
2. Use the Govee Home app to find your device ID and SKU

## Installation

### Installing via Smithery

To install Govee MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@mathd/govee_mcp_server):

```bash
npx -y @smithery/cli install @mathd/govee_mcp_server --client claude
```

### Manual Installation

```bash
# Install with pip
pip install .

# For development (includes test dependencies)
pip install -e ".[test]"
```

## Usage

### MCP Server

The MCP server provides tools for controlling Govee devices through the Model Context Protocol. It can be used with Cline or other MCP clients.

Available tools:
- `turn_on_off`: Turn the LED on or off
- `set_color`: Set the LED color using RGB values
- `set_brightness`: Set the LED brightness level

### Command Line Interface

A CLI is provided for direct control of Govee devices:

```bash
# Turn device on/off
govee-cli power on
govee-cli power off

# Set color using RGB values (0-255)
govee-cli color 255 0 0  # Red
govee-cli color 0 255 0  # Green
govee-cli color 0 0 255  # Blue

# Set brightness (0-100)
govee-cli brightness 50
```

Run `govee-cli --help` for full command documentation.

## Development

### Running Tests

To run the test suite:

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_server.py  # Server tests (mocked API calls)
pytest tests/test_cli.py    # CLI tests (real API calls)

# Run tests with verbose output
pytest tests/ -v
```

Note: The CLI tests make real API calls to your Govee device and will actually control it. Make sure your device is powered and connected before running these tests.

### Project Structure

```
.
├── src/govee_mcp_server/
│   ├── __init__.py
│   ├── server.py    # MCP server implementation
│   └── cli.py       # Command-line interface
├── tests/
│   ├── test_server.py  # Server tests (with mocked API)
│   └── test_cli.py     # CLI tests (real API calls)
└── pyproject.toml      # Project configuration
```

### Test Coverage

- Server tests cover:
  - Environment initialization
  - Govee API client methods
  - Server tools and utilities
  - Error handling

- CLI tests perform real-world integration testing by executing actual API calls to control your Govee device.

#!/usr/bin/env python3
import sys
import argparse
import asyncio
from .config import load_config
from .api import GoveeAPI
from .exceptions import GoveeError, GoveeValidationError

def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(description='Control Govee LED device')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Power command
    power_parser = subparsers.add_parser('power', help='Turn device on/off')
    power_parser.add_argument('state', choices=['on', 'off'], help='Power state')
    
    # Color command
    color_parser = subparsers.add_parser('color', help='Set device color')
    color_parser.add_argument('red', type=int, help='Red value (0-255)')
    color_parser.add_argument('green', type=int, help='Green value (0-255)')
    color_parser.add_argument('blue', type=int, help='Blue value (0-255)')
    
    # Brightness command
    brightness_parser = subparsers.add_parser('brightness', help='Set device brightness')
    brightness_parser.add_argument('level', type=int, help='Brightness level (0-100)')
    
    # Status command
    subparsers.add_parser('status', help='Show device status')
    
    return parser

async def handle_power(api: GoveeAPI, state: str) -> None:
    """Handle power command."""
    success, message = await api.set_power(state == 'on')
    if not success:
        raise GoveeError(message)
    print(message)

async def handle_color(api: GoveeAPI, red: int, green: int, blue: int) -> None:
    """Handle color command."""
    try:
        success, message = await api.set_color(red, green, blue)
        if not success:
            raise GoveeError(message)
        print(message)
    except GoveeValidationError as e:
        print(f"Error: {e}")
        sys.exit(1)

async def handle_brightness(api: GoveeAPI, level: int) -> None:
    """Handle brightness command."""
    if not 0 <= level <= 100:
        print("Error: Brightness level must be between 0 and 100")
        sys.exit(1)
        
    success, message = await api.set_brightness(level)
    if not success:
        raise GoveeError(message)
    print(message)

async def handle_status(api: GoveeAPI) -> None:
    """Handle status command."""
    # Get power state
    power_state, power_msg = await api.get_power_state()
    print(f"Power: {'ON' if power_state else 'OFF'}")
    
    # Get color
    color, color_msg = await api.get_color()
    print(f"Color: RGB({color[0]}, {color[1]}, {color[2]})")
    
    # Get brightness
    brightness, bright_msg = await api.get_brightness()
    print(f"Brightness: {brightness}%")

async def main() -> None:
    """Main CLI entrypoint."""
    try:
        # Load configuration
        config = load_config()
        api = GoveeAPI(config)
        
        # Parse arguments
        parser = create_parser()
        args = parser.parse_args()
        
        if args.command == 'power':
            await handle_power(api, args.state)
        elif args.command == 'color':
            await handle_color(api, args.red, args.green, args.blue)
        elif args.command == 'brightness':
            await handle_brightness(api, args.level)
        elif args.command == 'status':
            await handle_status(api)
        else:
            parser.print_help()
            sys.exit(1)
            
    except GoveeError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Always close the API session
        if 'api' in locals():
            await api.close()

def cli_main():
    """CLI entry point that handles running the async main."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    cli_main()
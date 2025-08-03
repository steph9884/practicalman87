# IP to Website Converter

A powerful tool to convert IP addresses to hostnames/websites with both command-line and GUI interfaces.

## Features

- **Reverse DNS Lookup**: Convert IP addresses to hostnames using DNS
- **Additional Information**: Get organization, location, and ISP details
- **Multiple Interfaces**: Both command-line and GUI applications
- **Bulk Processing**: Convert multiple IP addresses at once
- **Export Results**: Save results to files or copy to clipboard
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Installation

### Option 1: Simple Version (No Dependencies)
**Recommended for quick use** - Works immediately without any setup:
```bash
python3 ip_to_website_simple.py 8.8.8.8
```

### Option 2: Full-Featured Version
For advanced features (organization info, GUI, executables):
```bash
# Run the setup script
./setup_full_version.sh

# Then activate the environment
source venv_ip_converter/bin/activate
```

### Option 3: Use Pre-built Executables
1. Run the setup script first (Option 2)
2. Build executables with: `python build_executable.py`
3. Find executables in the `release` folder

## Usage

### Command Line Interface (CLI)

**Simple Version (no setup required):**
```bash
# Convert single IP
python3 ip_to_website_simple.py 8.8.8.8

# Verbose output
python3 ip_to_website_simple.py -v 1.1.1.1

# Convert multiple IPs from file
python3 ip_to_website_simple.py -f sample_ips.txt

# Save results to file
python3 ip_to_website_simple.py 8.8.8.8 -o results.txt
```

**Full Version (after setup):**
```bash
# Convert single IP with additional info
python ip_to_website_cli.py 8.8.8.8

# Verbose output with organization/location data
python ip_to_website_cli.py -v 1.1.1.1

# Output as JSON
python ip_to_website_cli.py --json 208.67.222.222
```

### Graphical User Interface (GUI)

Run the GUI application:
```bash
python ip_to_website_gui.py
```

Features:
- Single IP conversion with instant results
- Bulk IP processing from text input or file
- Verbose mode for detailed information
- Save results to files
- Copy results to clipboard
- Progress tracking for bulk operations

## Building Executables

To create standalone executables:

```bash
python build_executable.py
```

This will create:
- `ip-to-website-cli` - Command line executable
- `ip-to-website-gui` - GUI executable
- Complete distribution package in the `release` folder

## Examples

### CLI Examples

```bash
# Basic conversion
$ python ip_to_website_cli.py 8.8.8.8
8.8.8.8 -> dns.google

# Verbose output
$ python ip_to_website_cli.py -v 1.1.1.1
Processing IP: 1.1.1.1
  Hostname: one.one.one.one
  Organization: Cloudflare, Inc.
  Location: San Francisco, United States
  ISP: Cloudflare, Inc.
1.1.1.1 -> one.one.one.one

# Batch processing
$ python ip_to_website_cli.py -f sample_ips.txt
8.8.8.8 -> dns.google
1.1.1.1 -> one.one.one.one
208.67.222.222 -> resolver1.opendns.com
```

### Sample IP File Format

Create a text file with one IP per line:
```
8.8.8.8
1.1.1.1
208.67.222.222
9.9.9.9
```

## API Information Sources

The tool uses multiple sources to gather comprehensive information:

1. **Reverse DNS Lookup**: Standard DNS PTR record lookup
2. **IP-API.com**: Free geolocation and ISP information
3. **IPWho.is**: Additional WHOIS and organization data

## Requirements

- Python 3.6+
- Internet connection for API lookups
- Dependencies listed in `requirements.txt`

## Dependencies

- `socket` - Built-in DNS lookup functionality
- `requests` - HTTP requests for API calls
- `tkinter` - GUI framework (usually included with Python)
- `dnspython` - Enhanced DNS functionality
- `pyinstaller` - For building executables

## Error Handling

The tool gracefully handles:
- Invalid IP addresses
- Network connectivity issues
- DNS resolution failures
- API rate limits and timeouts

## Privacy and Security

- No IP addresses are logged or stored
- All lookups are performed in real-time
- Uses only public DNS and API services
- No personal data is collected or transmitted

## License

This project is open source. Feel free to use, modify, and distribute.

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Troubleshooting

### Common Issues

1. **"Invalid IP address" error**: Ensure the IP address format is correct (e.g., 192.168.1.1)
2. **No hostname found**: Some IP addresses may not have reverse DNS records
3. **Network errors**: Check your internet connection
4. **Executable not working**: Ensure all dependencies are included in the build

### Getting Help

If you encounter issues:
1. Check the error message for specific details
2. Verify your internet connection
3. Try with a known public IP address (e.g., 8.8.8.8)
4. Check if the IP address has a valid reverse DNS record
# URL Obfuscation Tool

A comprehensive Python toolkit for generating obfuscated URLs with dynamic components to protect website access patterns and enhance security through obscurity.

## 🔒 Features

- **Dynamic URL Generation**: Create URLs with random components that change on each generation
- **Multiple Templates**: Built-in templates for various use cases (webmail, admin portals, APIs)
- **Custom Templates**: Support for user-defined URL patterns
- **Batch Processing**: Process multiple emails/domains from CSV or JSON files
- **Web Interface**: Beautiful web UI for interactive URL generation
- **Multiple Output Formats**: Plain text, JSON, CSV
- **Email Obfuscation**: Base64, URL encoding, and other methods
- **Configurable Security**: Adjustable randomness and complexity levels

## 🚀 Quick Start

### Basic Usage

```bash
# Generate a single obfuscated URL
python url_obfuscator.py --email user@example.com --domain mysite.com

# Use a specific template
python url_obfuscator.py --template admin_portal --email admin@corp.com --domain secure.corp.com

# Generate multiple URLs
python url_obfuscator.py --template webmail_style --email user@test.com --count 5

# Use custom template
python url_obfuscator.py --custom-template "https://{domain}/secure/[[random_hex(16)]]?user=[[base64_email]]&token=[[random_string(20)]]"
```

### Web Interface

```bash
# Start the web server
python obfuscation_server.py

# Or specify a port
python obfuscation_server.py --port 8080
```

Then open `http://localhost:8080` in your browser.

### Batch Processing

```bash
# Create sample files
python batch_obfuscate.py --create-samples

# Process CSV file
python batch_obfuscate.py --csv sample_input.csv --template admin_portal --count 3

# Process JSON configuration
python batch_obfuscate.py --json sample_batch.json --output results.json
```

## 📋 Installation

1. **Clone or download the scripts** to your working directory

2. **No additional dependencies required** - uses only Python standard library

3. **Make scripts executable** (Linux/macOS):
   ```bash
   chmod +x url_obfuscator.py obfuscation_server.py batch_obfuscate.py
   ```

## 🎯 URL Templates

### Built-in Templates

| Template | Description | Example Output |
|----------|-------------|----------------|
| `webmail_style` | Similar to the provided example | `https://mysite.com/cpsess/12345678901/prompt?fromPWA=1&pwd=abc123...` |
| `admin_portal` | Administrative interface style | `https://mysite.com/admin/a1b2c3d4/dashboard?session=xyz...` |
| `api_endpoint` | REST API style | `https://mysite.com/api/v2/endpoint123/data?key=abc...` |
| `secure_login` | Authentication portal | `https://mysite.com/auth/secure123/login?challenge=xyz...` |
| `file_access` | File download portal | `https://mysite.com/files/12345/download?id=abc...` |

### Template Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[[random_digits(n)]]` | Random digits | `12345678901` |
| `[[random_string(n)]]` | Random alphanumeric | `aBc123XyZ` |
| `[[random_hex(n)]]` | Random hexadecimal | `a1b2c3d4e5f6` |
| `[[random_uuid]]` | UUID v4 | `123e4567-e89b-12d3-a456-426614174000` |
| `[[base64_email]]` | Base64 encoded email | `dXNlckBleGFtcGxlLmNvbQ==` |
| `[[url_encode_email]]` | URL encoded email | `user%40example.com` |
| `[[timestamp]]` | Current timestamp | `1709509974548` |
| `[[hash_token]]` | SHA256 hash (truncated) | `a1b2c3d4e5f6g7h8` |

## 📊 Example Outputs

### Webmail Style (like your example)
```
https://webmail-authoss.avsqone.com/cpsess/12345678901/prompt?fromPWA=1&pwd=aBcD3fGhI5kLmN8pQrS7&_x_zm_rtaid=I7SQ3VeP.1709509974548.RPS/cndRs57BvQ/aBcD3fGhI5kLmN8pQrS7&_x_zm_rhtaid=341%27#dXNlckBleGFtcGxlLmNvbQ==
```

### Admin Portal
```
https://secure-portal.com/admin/a1b2c3d4e5f6g7h8/dashboard?session=aBcD3fGhI5kLmN8pQrS7tUvWxYz123&token=1709509974548&hash=def456abc789&user=YWRtaW5AY29ycC5jb20=
```

### API Endpoint
```
https://api.service.com/api/v2/endpoint7/data?key=aBcD3fGhI5kLmN8pQrS7tUvWxYz123456789&sig=abc123def456&ts=1709509974548&uid=123e4567-e89b-12d3-a456-426614174000
```

## ⚙️ Configuration

### JSON Configuration File

```json
{
  "domains": ["secure-site.com", "portal.example.org"],
  "email_obfuscation_method": "base64",
  "url_generation": {
    "random_length_min": 12,
    "random_length_max": 32,
    "use_timestamps": true,
    "use_hash_tokens": true
  },
  "security": {
    "add_decoy_params": true,
    "randomize_param_order": true,
    "use_fragments": true
  }
}
```

### Batch Processing Input

**CSV Format:**
```csv
email,domain
user1@company.com,secure-portal.com
admin@corp.net,admin.corp.net
test@example.org,api.example.org
```

**JSON Format:**
```json
{
  "entries": [
    {
      "email": "user@company.com",
      "domain": "secure-portal.com",
      "template": "webmail_style",
      "count": 3
    },
    {
      "email": "admin@corp.net",
      "domain": "admin.corp.net",
      "template": "https://{domain}/custom/[[random_string(12)]]?user=[[base64_email]]",
      "count": 1
    }
  ]
}
```

## 🛡️ Security Features

### Obfuscation Methods
- **Random Components**: Each URL contains multiple random elements
- **Timestamp Tokens**: Time-based components for session management
- **Hash Tokens**: Cryptographic hashes for additional security
- **Email Encoding**: Multiple methods to obscure email addresses
- **Path Randomization**: Dynamic path components

### Security Levels
1. **Basic**: Simple random strings and digits
2. **Enhanced**: Timestamps, hashes, and encoded emails
3. **Advanced**: Custom algorithms and complex patterns

## 📖 API Reference

### Command Line Options

#### url_obfuscator.py
```bash
--template, -t          Template name to use
--custom-template       Custom template string
--email, -e            Email address to obfuscate
--domain, -d           Domain to use in URLs
--count, -c            Number of URLs to generate
--config               Configuration file path
--list-templates       List available templates
--output, -o           Output file path
--format               Output format (plain, json)
```

#### batch_obfuscate.py
```bash
--csv                  Input CSV file
--json                 Input JSON file
--output, -o           Output file path
--template, -t         Template to use
--count, -c            URLs per entry
--config               Configuration file
--create-samples       Create example files
--list-templates       List available templates
```

#### obfuscation_server.py
```bash
--port, -p             Port to run server on
```

### Python API

```python
from url_obfuscator import URLObfuscator, URLTemplateEngine

# Initialize
obfuscator = URLObfuscator()
template_engine = URLTemplateEngine(obfuscator)

# Generate single URL
url = template_engine.process_template(
    template_engine.templates['webmail_style'],
    email='user@example.com',
    domain='mysite.com'
)

# Custom template
custom_url = template_engine.process_template(
    'https://{domain}/[[random_string(8)]]?id=[[base64_email]]',
    email='test@domain.com',
    domain='secure.com'
)
```

## 🔧 Customization

### Creating Custom Templates

Templates use placeholder syntax `[[function_name(args)]]`:

```python
# Simple template
template = "https://{domain}/path/[[random_string(8)]]?id=[[base64_email]]"

# Complex template with multiple components
template = """https://{domain}/secure/[[random_hex(16)]]/auth?
session=[[random_string(32)]]&
token=[[timestamp]]&
hash=[[hash_token]]&
user=[[base64_email]]&
challenge=[[random_string(24)]]"""
```

### Adding New Placeholders

Extend the `URLTemplateEngine._process_placeholder()` method:

```python
elif placeholder == 'custom_function':
    return self.obfuscator.custom_method()
```

## 📝 Use Cases

1. **Penetration Testing**: Generate realistic-looking URLs for testing
2. **Security Research**: Create obfuscated endpoints for analysis
3. **Privacy Protection**: Hide actual URL patterns from logs
4. **Development**: Generate test URLs with realistic complexity
5. **Training**: Create scenarios for security awareness

## ⚠️ Important Notes

- **Educational Purpose**: This tool is for legitimate security testing and research
- **Legal Compliance**: Ensure you have permission before testing any systems
- **Not Real Security**: Obfuscation provides obscurity, not actual security
- **Responsible Use**: Use only on systems you own or have explicit permission to test

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Test your changes thoroughly
4. Submit a pull request with detailed description

## 📜 License

This project is released under the MIT License. See LICENSE file for details.

## 🆘 Support

For issues, questions, or contributions:

1. Check existing documentation
2. Search for similar issues
3. Create detailed bug reports
4. Provide example inputs/outputs for problems

---

**Disclaimer**: This tool is for educational and authorized testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.
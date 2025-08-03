#!/usr/bin/env python3
"""
Batch URL Obfuscation Script
============================

Process multiple URLs and email addresses in batch mode.
Supports CSV input/output and various configuration options.
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from url_obfuscator import URLObfuscator, URLTemplateEngine, ObfuscationConfig
from datetime import datetime


class BatchProcessor:
    """Batch processor for URL obfuscation."""
    
    def __init__(self, config_file=None):
        self.obfuscator = URLObfuscator()
        self.template_engine = URLTemplateEngine(self.obfuscator)
        self.config = ObfuscationConfig(config_file)
        
    def process_csv_file(self, input_file, output_file, template_name='webmail_style', count_per_entry=1):
        """Process a CSV file with email/domain combinations."""
        results = []
        
        try:
            with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row_num, row in enumerate(reader, 1):
                    email = row.get('email', '')
                    domain = row.get('domain', 'example.com')
                    custom_template = row.get('template', '')
                    
                    if not email:
                        print(f"Warning: No email in row {row_num}, skipping...")
                        continue
                    
                    # Use custom template if provided, otherwise use the specified template
                    if custom_template:
                        template = custom_template
                    else:
                        template = self.template_engine.templates.get(template_name, 
                                                                   self.template_engine.templates['webmail_style'])
                    
                    # Generate URLs for this entry
                    for i in range(count_per_entry):
                        url = self.template_engine.process_template(template, email, domain)
                        results.append({
                            'row_number': row_num,
                            'email': email,
                            'domain': domain,
                            'template': template_name,
                            'url': url,
                            'timestamp': datetime.now().isoformat(),
                            'url_index': i + 1
                        })
                        
        except FileNotFoundError:
            print(f"Error: Input file '{input_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing CSV: {e}")
            sys.exit(1)
        
        # Write results
        self._write_results(results, output_file)
        return results
    
    def process_json_file(self, input_file, output_file):
        """Process a JSON file with batch configuration."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                batch_config = json.load(f)
        except FileNotFoundError:
            print(f"Error: Input file '{input_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{input_file}': {e}")
            sys.exit(1)
        
        results = []
        
        for entry_num, entry in enumerate(batch_config.get('entries', []), 1):
            email = entry.get('email', '')
            domain = entry.get('domain', 'example.com')
            template_name = entry.get('template', 'webmail_style')
            count = entry.get('count', 1)
            custom_vars = entry.get('custom_vars', {})
            
            if not email:
                print(f"Warning: No email in entry {entry_num}, skipping...")
                continue
            
            # Get template
            if template_name in self.template_engine.templates:
                template = self.template_engine.templates[template_name]
            else:
                template = template_name  # Assume it's a custom template string
            
            # Generate URLs for this entry
            for i in range(count):
                url = self.template_engine.process_template(template, email, domain, custom_vars)
                results.append({
                    'entry_number': entry_num,
                    'email': email,
                    'domain': domain,
                    'template': template_name,
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                    'url_index': i + 1,
                    'custom_vars': custom_vars
                })
        
        # Write results
        self._write_results(results, output_file)
        return results
    
    def _write_results(self, results, output_file):
        """Write results to output file."""
        output_path = Path(output_file)
        
        if output_path.suffix.lower() == '.csv':
            self._write_csv_results(results, output_file)
        elif output_path.suffix.lower() == '.json':
            self._write_json_results(results, output_file)
        else:
            # Default to text format
            self._write_text_results(results, output_file)
    
    def _write_csv_results(self, results, output_file):
        """Write results to CSV file."""
        if not results:
            return
        
        fieldnames = results[0].keys()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    def _write_json_results(self, results, output_file):
        """Write results to JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def _write_text_results(self, results, output_file):
        """Write results to text file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"{result['url']}\n")


def create_sample_csv():
    """Create a sample CSV file for demonstration."""
    sample_data = [
        {'email': 'user1@company.com', 'domain': 'secure-portal.com'},
        {'email': 'admin@corp.net', 'domain': 'admin.corp.net'},
        {'email': 'test@example.org', 'domain': 'api.example.org'},
        {'email': 'support@service.io', 'domain': 'app.service.io'}
    ]
    
    with open('sample_input.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['email', 'domain']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)
    
    print("Created sample_input.csv with example data")


def create_sample_json():
    """Create a sample JSON file for demonstration."""
    sample_config = {
        "entries": [
            {
                "email": "user1@company.com",
                "domain": "secure-portal.com",
                "template": "webmail_style",
                "count": 3
            },
            {
                "email": "admin@corp.net",
                "domain": "admin.corp.net",
                "template": "admin_portal",
                "count": 2,
                "custom_vars": {
                    "special_token": "abc123def456"
                }
            },
            {
                "email": "api@service.com",
                "domain": "api.service.com",
                "template": "https://{domain}/custom/[[random_string(12)]]?user=[[base64_email]]&key=[[special_token]]",
                "count": 1,
                "custom_vars": {
                    "special_token": "xyz789"
                }
            }
        ]
    }
    
    with open('sample_batch.json', 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, indent=2)
    
    print("Created sample_batch.json with example configuration")


def main():
    """Main function for batch processing."""
    parser = argparse.ArgumentParser(
        description='Batch URL Obfuscation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --csv input.csv --output results.csv --template admin_portal --count 5
  %(prog)s --json batch_config.json --output results.json
  %(prog)s --create-samples
  %(prog)s --csv sample_input.csv --output urls.txt --template webmail_style
        """
    )
    
    parser.add_argument('--csv', help='Input CSV file with email/domain columns')
    parser.add_argument('--json', help='Input JSON file with batch configuration')
    parser.add_argument('--output', '-o', required=False, help='Output file path')
    parser.add_argument('--template', '-t', default='webmail_style',
                       help='Template to use (default: webmail_style)')
    parser.add_argument('--count', '-c', type=int, default=1,
                       help='Number of URLs per entry (default: 1)')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--create-samples', action='store_true',
                       help='Create sample input files')
    parser.add_argument('--list-templates', action='store_true',
                       help='List available templates')
    
    args = parser.parse_args()
    
    # Create sample files if requested
    if args.create_samples:
        create_sample_csv()
        create_sample_json()
        return
    
    # Initialize processor
    processor = BatchProcessor(args.config)
    
    # List templates if requested
    if args.list_templates:
        print("Available templates:")
        for name in processor.template_engine.templates.keys():
            print(f"  - {name}")
        return
    
    # Validate input arguments
    if not args.csv and not args.json:
        print("Error: Either --csv or --json input file is required")
        print("Use --create-samples to generate example files")
        sys.exit(1)
    
    if not args.output:
        if args.csv:
            args.output = args.csv.replace('.csv', '_obfuscated.csv')
        elif args.json:
            args.output = args.json.replace('.json', '_obfuscated.json')
    
    # Process files
    try:
        if args.csv:
            results = processor.process_csv_file(args.csv, args.output, args.template, args.count)
            print(f"Processed {len(results)} URLs from CSV file")
        elif args.json:
            results = processor.process_json_file(args.json, args.output)
            print(f"Processed {len(results)} URLs from JSON file")
        
        print(f"Results saved to: {args.output}")
        
        # Show summary
        if results:
            unique_emails = len(set(r['email'] for r in results))
            unique_domains = len(set(r['domain'] for r in results))
            print(f"Summary: {len(results)} URLs for {unique_emails} emails across {unique_domains} domains")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
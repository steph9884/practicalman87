#!/usr/bin/env python3
"""
Simple IP to Website Converter - Built-in modules only
Converts IP addresses to hostnames using only built-in Python modules.
"""

import socket
import sys
import argparse
from typing import Optional


def is_valid_ip(ip: str) -> bool:
    """Check if the given string is a valid IP address."""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def reverse_dns_lookup(ip: str) -> Optional[str]:
    """Perform reverse DNS lookup to get hostname from IP."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.herror, socket.gaierror):
        return None


def convert_ip_to_hostname(ip: str, verbose: bool = False) -> dict:
    """Convert IP address to hostname."""
    if not is_valid_ip(ip):
        return {"error": f"Invalid IP address: {ip}"}
    
    if verbose:
        print(f"Processing IP: {ip}")
    
    hostname = reverse_dns_lookup(ip)
    
    result = {
        "ip": ip,
        "hostname": hostname or "No hostname found"
    }
    
    if verbose and hostname:
        print(f"  Hostname: {hostname}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Convert IP addresses to hostnames (simple version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 8.8.8.8
  %(prog)s -v 1.1.1.1
  %(prog)s -f ip_list.txt
        """
    )
    
    parser.add_argument("ip", nargs="?", help="IP address to convert")
    parser.add_argument("-f", "--file", help="File containing list of IP addresses")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if not args.ip and not args.file:
        parser.print_help()
        sys.exit(1)
    
    results = []
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                ip_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            for ip in ip_list:
                result = convert_ip_to_hostname(ip, args.verbose)
                results.append(result)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        result = convert_ip_to_hostname(args.ip, args.verbose)
        results = [result]
    
    # Format and output results
    output_lines = []
    for result in results:
        if "error" in result:
            output_lines.append(f"ERROR: {result['error']}")
        else:
            ip = result["ip"]
            hostname = result["hostname"]
            output_lines.append(f"{ip} -> {hostname}")
    
    output = "\n".join(output_lines)
    
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"Error writing to file: {e}")
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
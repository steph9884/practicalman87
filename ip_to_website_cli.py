#!/usr/bin/env python3
"""
IP to Website Converter - Command Line Interface
Converts IP addresses to hostnames/websites using reverse DNS lookup.
"""

import socket
import sys
import argparse
import requests
import json
from typing import Optional, List, Dict, Any
import re


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


def get_ip_info_api(ip: str) -> Dict[str, Any]:
    """Get IP information from ip-api.com service."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return {}


def get_whois_info(ip: str) -> Dict[str, Any]:
    """Get WHOIS information for the IP address."""
    try:
        response = requests.get(f"http://ipwho.is/{ip}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return {}


def convert_ip_to_websites(ip: str, verbose: bool = False) -> Dict[str, Any]:
    """Convert IP address to website information."""
    if not is_valid_ip(ip):
        return {"error": f"Invalid IP address: {ip}"}
    
    result = {
        "ip": ip,
        "hostname": None,
        "domains": [],
        "organization": None,
        "country": None,
        "city": None,
        "isp": None
    }
    
    if verbose:
        print(f"Processing IP: {ip}")
    
    # Reverse DNS lookup
    hostname = reverse_dns_lookup(ip)
    if hostname:
        result["hostname"] = hostname
        result["domains"].append(hostname)
        if verbose:
            print(f"  Hostname: {hostname}")
    
    # Get additional info from IP-API
    ip_info = get_ip_info_api(ip)
    if ip_info and ip_info.get("status") == "success":
        result["organization"] = ip_info.get("org")
        result["country"] = ip_info.get("country")
        result["city"] = ip_info.get("city")
        result["isp"] = ip_info.get("isp")
        
        if verbose:
            print(f"  Organization: {result['organization']}")
            print(f"  Location: {result['city']}, {result['country']}")
            print(f"  ISP: {result['isp']}")
    
    # Get WHOIS info
    whois_info = get_whois_info(ip)
    if whois_info and whois_info.get("success"):
        if not result["organization"]:
            result["organization"] = whois_info.get("connection", {}).get("org")
        if not result["country"]:
            result["country"] = whois_info.get("country")
        if not result["city"]:
            result["city"] = whois_info.get("city")
    
    return result


def process_ip_list(ip_list: List[str], verbose: bool = False) -> List[Dict[str, Any]]:
    """Process a list of IP addresses."""
    results = []
    for ip in ip_list:
        ip = ip.strip()
        if ip:  # Skip empty lines
            result = convert_ip_to_websites(ip, verbose)
            results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert IP addresses to websites/hostnames",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 8.8.8.8
  %(prog)s -v 1.1.1.1
  %(prog)s -f ip_list.txt
  %(prog)s --json 208.67.222.222
        """
    )
    
    parser.add_argument("ip", nargs="?", help="IP address to convert")
    parser.add_argument("-f", "--file", help="File containing list of IP addresses")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if not args.ip and not args.file:
        parser.print_help()
        sys.exit(1)
    
    results = []
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                ip_list = f.readlines()
            results = process_ip_list(ip_list, args.verbose)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        result = convert_ip_to_websites(args.ip, args.verbose)
        results = [result]
    
    # Output results
    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output_lines = []
        for result in results:
            if "error" in result:
                output_lines.append(f"ERROR: {result['error']}")
            else:
                ip = result["ip"]
                hostname = result["hostname"] or "No hostname found"
                output_lines.append(f"{ip} -> {hostname}")
                
                if args.verbose:
                    if result["organization"]:
                        output_lines.append(f"  Organization: {result['organization']}")
                    if result["country"] and result["city"]:
                        output_lines.append(f"  Location: {result['city']}, {result['country']}")
                    if result["isp"]:
                        output_lines.append(f"  ISP: {result['isp']}")
                    output_lines.append("")
        
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
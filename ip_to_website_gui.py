#!/usr/bin/env python3
"""
IP to Website Converter - GUI Application
Modern GUI interface for converting IP addresses to hostnames/websites.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
from typing import List, Dict, Any
import os
import sys

# Import the conversion functions from CLI script
from ip_to_website_cli import convert_ip_to_websites, is_valid_ip, process_ip_list


class IPToWebsiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IP to Website Converter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="IP to Website Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Single IP input
        ttk.Label(input_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.ip_entry = ttk.Entry(input_frame, width=20)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.ip_entry.bind('<Return>', lambda e: self.convert_single_ip())
        
        ttk.Button(input_frame, text="Convert", 
                  command=self.convert_single_ip).grid(row=0, column=2, padx=(5, 0))
        
        # Bulk input
        ttk.Label(input_frame, text="Bulk Input:").grid(row=1, column=0, sticky=(tk.W, tk.N), 
                                                        padx=(0, 5), pady=(10, 0))
        
        bulk_frame = ttk.Frame(input_frame)
        bulk_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        bulk_frame.columnconfigure(0, weight=1)
        
        self.bulk_text = scrolledtext.ScrolledText(bulk_frame, height=5, width=50)
        self.bulk_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(bulk_frame, text="Load from File", 
                  command=self.load_from_file).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Button(bulk_frame, text="Convert All", 
                  command=self.convert_bulk_ips).grid(row=1, column=1, sticky=tk.E, pady=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.verbose_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Verbose output (show additional info)", 
                       variable=self.verbose_var).grid(row=0, column=0, sticky=tk.W)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Clear Results", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Results", 
                  command=self.save_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        
    def update_status(self, message):
        """Update status bar message."""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def show_progress(self):
        """Show progress bar."""
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        self.progress.start()
        
    def hide_progress(self):
        """Hide progress bar."""
        self.progress.stop()
        self.progress.grid_remove()
        
    def append_result(self, text):
        """Append text to results area."""
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_results(self):
        """Clear the results text area."""
        self.results_text.delete(1.0, tk.END)
        
    def convert_single_ip(self):
        """Convert a single IP address."""
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("Warning", "Please enter an IP address")
            return
            
        if not is_valid_ip(ip):
            messagebox.showerror("Error", f"Invalid IP address: {ip}")
            return
            
        # Run conversion in thread to avoid blocking UI
        threading.Thread(target=self._convert_single_ip_thread, args=(ip,), daemon=True).start()
        
    def _convert_single_ip_thread(self, ip):
        """Thread function for converting single IP."""
        self.update_status(f"Converting {ip}...")
        self.show_progress()
        
        try:
            result = convert_ip_to_websites(ip, verbose=False)
            self._display_result(result)
        except Exception as e:
            self.append_result(f"Error converting {ip}: {str(e)}")
        finally:
            self.hide_progress()
            self.update_status("Ready")
            
    def convert_bulk_ips(self):
        """Convert multiple IP addresses."""
        text = self.bulk_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter IP addresses in the bulk input area")
            return
            
        ip_list = [line.strip() for line in text.split('\n') if line.strip()]
        if not ip_list:
            messagebox.showwarning("Warning", "No valid IP addresses found")
            return
            
        # Run conversion in thread
        threading.Thread(target=self._convert_bulk_ips_thread, args=(ip_list,), daemon=True).start()
        
    def _convert_bulk_ips_thread(self, ip_list):
        """Thread function for converting bulk IPs."""
        self.update_status(f"Converting {len(ip_list)} IP addresses...")
        self.show_progress()
        
        try:
            self.append_result(f"Converting {len(ip_list)} IP addresses...\n")
            
            for i, ip in enumerate(ip_list, 1):
                if not is_valid_ip(ip):
                    self.append_result(f"{i}. ERROR: Invalid IP address: {ip}")
                    continue
                    
                self.update_status(f"Converting {ip} ({i}/{len(ip_list)})...")
                result = convert_ip_to_websites(ip, verbose=False)
                self.append_result(f"{i}. {self._format_result_line(result)}")
                
        except Exception as e:
            self.append_result(f"Error during bulk conversion: {str(e)}")
        finally:
            self.hide_progress()
            self.update_status("Ready")
            self.append_result("\nBulk conversion completed.")
            
    def _display_result(self, result):
        """Display a single conversion result."""
        if "error" in result:
            self.append_result(f"ERROR: {result['error']}")
            return
            
        ip = result["ip"]
        hostname = result["hostname"] or "No hostname found"
        
        self.append_result(f"IP: {ip}")
        self.append_result(f"Hostname: {hostname}")
        
        if self.verbose_var.get():
            if result["organization"]:
                self.append_result(f"Organization: {result['organization']}")
            if result["country"] and result["city"]:
                self.append_result(f"Location: {result['city']}, {result['country']}")
            if result["isp"]:
                self.append_result(f"ISP: {result['isp']}")
                
        self.append_result("-" * 50)
        
    def _format_result_line(self, result):
        """Format result as a single line."""
        if "error" in result:
            return f"ERROR: {result['error']}"
            
        ip = result["ip"]
        hostname = result["hostname"] or "No hostname found"
        return f"{ip} -> {hostname}"
        
    def load_from_file(self):
        """Load IP addresses from a file."""
        file_path = filedialog.askopenfilename(
            title="Select file with IP addresses",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.bulk_text.delete(1.0, tk.END)
                self.bulk_text.insert(1.0, content)
                self.update_status(f"Loaded {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def save_results(self):
        """Save results to a file."""
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No results to save")
            return
            
        file_path = filedialog.asksavename(
            title="Save results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Results saved to {file_path}")
                self.update_status(f"Saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def copy_to_clipboard(self):
        """Copy results to clipboard."""
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No results to copy")
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Success", "Results copied to clipboard")
        self.update_status("Copied to clipboard")


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = IPToWebsiteGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
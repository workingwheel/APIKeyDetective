import re
import json
import os
from datetime import datetime
from colorama import init, Fore, Style

init()

class APIKeyIdentifier:
    def __init__(self):
        self.load_patterns()

    def load_patterns(self):
        """Load API patterns from JSON file"""
        try:
            with open('api_patterns.json', 'r') as file:
                self.api_services = json.load(file)
        except FileNotFoundError:
            print(f"{Fore.RED}Error: api_patterns.json not found!{Style.RESET_ALL}")
            exit(1)

    def identify_key(self, key):
        """Identify the API key and return detailed information"""
        if not key:
            return {
                "status": "error",
                "message": "No API key provided"
            }
        
        key = key.strip()  # Remove any whitespace
        
        for service, info in self.api_services.items():
            if re.match(info['pattern'], key):
                return {
                    "status": "success",
                    "service": service,
                    "description": info['description'],
                    "documentation": info['url']
                }
        
        return {
            "status": "unknown",
            "message": "Unknown API key format"
        }

def print_result(result):
    """Print the identification result in a formatted way"""
    print("\n" + "="*50)
    
    if result["status"] == "success":
        print(f"{Fore.GREEN}✓ API Key Identified!{Style.RESET_ALL}")
        print(f"\n{Fore.BLUE}Service:{Style.RESET_ALL} {result['service']}")
        print(f"{Fore.BLUE}Description:{Style.RESET_ALL} {result['description']}")
        print(f"{Fore.BLUE}Documentation:{Style.RESET_ALL} {result['documentation']}")
    
    elif result["status"] == "unknown":
        print(f"{Fore.YELLOW}❌ {result['message']}{Style.RESET_ALL}")
    
    else:  # error
        print(f"{Fore.RED}Error: {result['message']}{Style.RESET_ALL}")
    
    print("="*50 + "\n")

def main():
    identifier = APIKeyIdentifier()
    
    print(f"\n{Fore.CYAN}=== API Key Identifier Tool ==={Style.RESET_ALL}")
    print(f"{Fore.CYAN}Enter 'quit' to exit{Style.RESET_ALL}\n")
    
    while True:
        try:
            key = input(f"{Fore.GREEN}Enter API key to identify: {Style.RESET_ALL}").strip()
            
            if key.lower() == 'quit':
                print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}\n")
                break
                
            result = identifier.identify_key(key)
            print_result(result)
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Program terminated by user.{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
import os
import sys
import platform
import time
import requests
import base64
import json
import logging
from colorama import Fore, init, Style
from typing import Dict, List, Optional

init(autoreset=True)

config = {}
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

try:
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        print(f"{Fore.YELLOW}Config file not found. Using interactive mode.{Style.RESET_ALL}")
except json.JSONDecodeError:
    print(f"{Fore.RED}Error: config.json is malformed. Using interactive mode.{Style.RESET_ALL}")
    config = {}
except Exception as e:
    print(f"{Fore.RED}Error loading config: {e}. Using interactive mode.{Style.RESET_ALL}")
    config = {}

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloner.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

abt = "Azus Cloner - Lynx"

if platform.system() == "Windows":
    os.system("title " + abt)
else:
    sys.stdout.write(f"\033]0;{abt}\007")
    sys.stdout.flush()

if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")
    print(chr(27) + "[2J")

banner = r"""
[0;32;40m▄[0;32;42m [0;92;1;42m░[0;32;40m▀[0;92;1;42m░ [0;32;40m▄[0;37;40m [0;32;40m█[0;32;42m [0;92;1;42m░[0;32;40m▀[0;92;1;42m░ [0;32;40m▄[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;32;40m▄[0;92;1;42m ░[0;32;40m▀[0;92;1;42m░[0;32;42m [0;32;40m█[0;37;40m      [0;32;40m▄[0;32;42m [0;92;1;42m░[0;32;40m▀[0;92;1;42m░ [0;32;40m▄[0;37;40m [0;92;1;42m░ ░[0;37;40m   [0;32;40m▄[0;32;42m [0;92;1;42m░[0;32;40m▀[0;92;1;42m░ [0;32;40m▄[0;37;40m [0;32;40m▀▀▀▀[0;92;1;42m▒░[0;32;40m▄[0;37;40m [0;32;40m▄[0;32;42m [0;92;1;42m░[0;32;40m▀[0;92;1;42m░ [0;32;40m▄[0;37;40m [0;32;40m▀▀▀▀[0;92;1;42m░ [0;32;40m▄[0m
[0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m      [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m   [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░▒[0;37;40m [0;92;1;42m▒░[0;32;40m▀[0m
[0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;90;1;40m▄▄[0;92;1;40m▀[0;37;40m [0;92;1;40m▀[0;90;1;40m▄[0;92;1;40m▀[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m      [0;92;1;42m▓[0;92;1;40m▀▀[0;37;40m     [0;92;1;42m▓▒▓[0;37;40m   [0;92;1;42m▓▒▓[0;37;40m [0;92;1;42m▓▒▓[0;37;40m [0;90;1;40m▄[0;92;1;40m▀▀[0;37;40m [0;92;1;42m█▓[0;92;1;40m▀[0;37;40m [0;92;1;42m▓[0;92;1;40m▀▀[0;37;40m     [0;92;1;42m▓▒▓[0;37;40m [0;92;1;40m▄▄[0;37;40m [0m
[0;92;1;40m▀█▀[0;32;40m▀[0;92;1;40m▀[0;92;1;42m█[0;92;1;40m▀[0;37;40m   [0;32;40m▄[0;92;1;40m▄[0;92;1;42m██[0;92;1;40m▀[0;37;40m [0;90;1;42m█▓█[0;37;40m [0;90;1;42m█▓█[0;37;40m [0;92;1;40m▀[0;92;1;42m██[0;92;1;40m▄[0;32;40m▄[0;37;40m        [0;90;1;40m▄[0;90;1;42m▓▓[0;37;40m     [0;92;1;42m█[0;92;1;40m▀[0;92;1;42m█[0;37;40m   [0;92;1;42m█[0;92;1;40m▀▀[0;37;40m [0;92;1;42m██[0;92;1;40m▀[0;37;40m [0;90;1;42m█▓█[0;37;40m [0;90;1;40m▄▄[0;90;1;42m█[0;37;40m [0;90;1;40m▄[0;90;1;42m▓▓[0;90;1;40m▀[0;37;40m    [0;92;1;40m▀[0;90;1;40m▄[0;92;1;40m▀[0;37;40m [0;90;1;40m▄▄[0;92;1;40m▀[0m
[0;32;40m█▄█[0;37;40m [0;32;40m█[0;90;1;40m▄[0;90;1;42m▓[0;37;40m [0;90;1;40m▄[0;90;1;42m▓▓[0;32;40m▀▀[0;37;40m   [0;90;1;42m▓▒▓[0;37;40m [0;90;1;42m▓▒▓[0;37;40m   [0;32;40m▀▀[0;90;1;42m▓▓[0;90;1;40m▄[0;37;40m      [0;90;1;42m▓▒▒[0;37;40m     [0;90;1;40m▄[0;90;1;42m▓[0;90;1;40m▄[0;37;40m   [0;90;1;40m▄[0;90;1;42m▓▓[0;37;40m [0;90;1;40m▄▄[0;90;1;42m▓[0;37;40m [0;90;1;42m▓▒▓[0;37;40m [0;90;1;42m▓▒▓[0;37;40m [0;90;1;42m▓▒▒[0;37;40m     [0;90;1;40m▐[0;90;1;42m▓▓[0;37;40m [0;90;1;42m▓▒▓[0m
[0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m      [0;90;1;42m▒░░[0;37;40m [0;90;1;42m░ ░[0;37;40m [0;90;1;42m▒░▒[0;37;40m   [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░░[0;37;40m [0;90;1;42m░ ░[0;37;40m [0;90;1;42m▒░▒[0;37;40m [0;90;1;42m▒░▒[0m
[0;32;40m█[0;32;42m [0;90;1;42m░[0;37;40m [0;90;1;42m░ [0;32;40m█[0;37;40m [0;32;40m▀[0;32;42m [0;90;1;42m░[0;32;40m▄[0;90;1;42m░ [0;32;40m█[0;37;40m [0;32;40m▀[0;32;42m [0;90;1;42m░[0;32;40m▄[0;90;1;42m░ [0;32;40m▀[0;37;40m [0;32;40m█[0;90;1;42m ░[0;32;40m▄[0;90;1;42m░[0;32;42m [0;32;40m▀[0;37;40m      [0;32;40m▀[0;32;42m  [0;32;40m▄[0;32;42m  [0;32;40m▀[0;37;40m [0;90;1;42m░ ░[0;32;40m▄▄[0;37;40m [0;32;40m▀[0;32;42m [0;90;1;42m░[0;32;40m▄[0;90;1;42m░ [0;32;40m▀[0;37;40m [0;90;1;42m░ ░[0;37;40m [0;90;1;42m░ ░[0;37;40m [0;32;40m▀[0;32;42m  [0;32;40m▄[0;32;42m  [0;32;40m▀[0;37;40m [0;90;1;42m░ ░[0;37;40m [0;90;1;42m░ ░[0m
"""

print(f"{banner}")
print(f"{Fore.CYAN}    </> Dev: Lynx{Style.RESET_ALL}\n")

token = config.get('token', '')
guild_s = config.get('source', '')
guild = config.get('destination', '')

if not token:
    token = input(f'{Fore.CYAN}-> Enter account token:\n >> {Style.RESET_ALL}')
    token = token.strip()
if not guild_s:
    guild_s = input(f'{Fore.CYAN}-> ID of the server to copy:\n >> {Style.RESET_ALL}')
if not guild:
    guild = input(f'{Fore.CYAN}-> ID of the server to paste into:\n >> {Style.RESET_ALL}')

input_guild_id = guild_s
output_guild_id = guild

print("\n")

headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}

def print_add(message):
    logging.info(f"[+] {message}")
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    logging.info(f"[-] {message}")
    print(f'{Fore.BLUE}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    logging.warning(f"[WARNING] {message}")
    print(f'{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    logging.error(f"[ERROR] {message}")
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

def print_info(message):
    logging.info(f"[INFO] {message}")
    print(f'{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}')

def api_request(method, endpoint, data=None, max_retries=3):
    url = f"https://discord.com/api/v10{endpoint}"
    
    for attempt in range(max_retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                return None, "Invalid method"
            
            if response.status_code == 429:
                retry_after = response.json().get('retry_after', 1)
                print_warning(f"Rate limited! Waiting {retry_after:.2f} seconds...")
                time.sleep(retry_after + 0.5)
                continue
                
            try:
                json_data = response.json() if response.text else None
            except:
                json_data = {"message": response.text} if response.text else None
                
            return response.status_code, json_data
            
        except requests.exceptions.RequestException as e:
            print_error(f"Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None, str(e)
        except Exception as e:
            print_error(f"Unexpected error in API request: {e}")
            return None, str(e)
    
    return None, "Max retries exceeded"

def is_success(status):
    return status is not None and 200 <= status < 300

class Progress:
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0
        
    def next_step(self, message):
        self.current_step += 1
        print(f"\n{Fore.CYAN}[{self.current_step}/{self.total_steps}] {message}{Style.RESET_ALL}")
        
    def show_progress(self, current, total, label):
        bar_length = 30
        try:
            progress = current / total if total > 0 else 0
        except:
            progress = 0
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r{Fore.YELLOW}{label}: {bar} {current}/{total}{Style.RESET_ALL}", end="")

class RateLimiter:
    def __init__(self, delay=0.5):
        self.delay = delay
        
    def wait(self):
        time.sleep(self.delay)

class Cloner:
    def __init__(self, source_guild_id: str, dest_guild_id: str):
        self.source_guild_id = source_guild_id
        self.dest_guild_id = dest_guild_id
        self.role_map: Dict[str, Dict] = {}
        self.channel_map: Dict[str, Dict] = {}
        self.rate_limiter = RateLimiter()
        self.progress = Progress(9)
        
    def get_guild_info(self, guild_id):
        status, data = api_request("GET", f"/guilds/{guild_id}")
        if is_success(status):
            return data
        else:
            print_error(f"Error getting guild info: {data}")
            return None
            
    def get_guild_channels(self, guild_id):
        status, data = api_request("GET", f"/guilds/{guild_id}/channels")
        if is_success(status):
            return data
        else:
            print_error(f"Error getting channels: {data}")
            return None
            
    def get_guild_roles(self, guild_id):
        status, data = api_request("GET", f"/guilds/{guild_id}/roles")
        if is_success(status):
            return data
        else:
            print_error(f"Error getting roles: {data}")
            return None
            
    def get_guild_emojis(self, guild_id):
        status, data = api_request("GET", f"/guilds/{guild_id}/emojis")
        if is_success(status):
            return data
        else:
            print_error(f"Error getting emojis: {data}")
            return None

    def edit_guild(self):
        self.progress.next_step("Copying server name and icon...")
        
        source_guild = self.get_guild_info(self.source_guild_id)
        if not source_guild:
            return False
            
        try:
            data = {"name": source_guild.get("name")}
            
            if source_guild.get("icon"):
                try:
                    icon_url = f"https://cdn.discordapp.com/icons/{self.source_guild_id}/{source_guild['icon']}.png"
                    icon_response = requests.get(icon_url)
                    if icon_response.status_code == 200:
                        icon_b64 = base64.b64encode(icon_response.content).decode('utf-8')
                        data["icon"] = f"data:image/png;base64,{icon_b64}"
                        print_add(f"Changed server icon: {source_guild['name']}")
                    else:
                        print_warning("Could not download icon")
                except Exception as e:
                    print_error(f"Error changing icon: {e}")
            
            status, response = api_request("PATCH", f"/guilds/{self.dest_guild_id}", data)
            if is_success(status):
                print_add(f"Changed server name to: {source_guild['name']}")
                return True
            else:
                print_error(f"Error editing guild: Status {status} - {response}")
                return False
                
        except Exception as e:
            print_error(f"Error editing guild: {e}")
            return False

    def delete_roles(self):
        self.progress.next_step("Deleting existing roles...")
        
        try:
            roles = self.get_guild_roles(self.dest_guild_id)
            if not roles:
                return
                
            roles_to_delete = [r for r in roles if r.get("name") != "@everyone"]
            total = len(roles_to_delete)
            
            for i, role in enumerate(roles_to_delete):
                try:
                    status, response = api_request("DELETE", f"/guilds/{self.dest_guild_id}/roles/{role['id']}")
                    if is_success(status):
                        print_delete(f"Deleted Role: {role['name']}")
                    else:
                        print_error(f"Cannot delete role: {role['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Deleting roles")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error deleting role {role['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in delete_roles: {e}")

    def delete_channels(self):
        self.progress.next_step("Deleting existing channels...")
        
        try:
            channels = self.get_guild_channels(self.dest_guild_id)
            if not channels:
                return
                
            total = len(channels)
            
            for i, channel in enumerate(channels):
                try:
                    status, response = api_request("DELETE", f"/channels/{channel['id']}")
                    if is_success(status):
                        print_delete(f"Deleting channel: {channel['name']}")
                    else:
                        print_error(f"Cannot delete channel: {channel['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Deleting channels")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error deleting channel {channel['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in delete_channels: {e}")

    def create_roles(self):
        self.progress.next_step("Creating roles...")
        
        try:
            source_roles = self.get_guild_roles(self.source_guild_id)
            if not source_roles:
                return
                
            roles = [r for r in source_roles if r.get("name") != "@everyone"]
            roles = roles[::-1]
            total = len(roles)
            
            for i, role in enumerate(roles):
                try:
                    data = {
                        "name": role["name"],
                        "color": role.get("color", 0),
                        "hoist": role.get("hoist", False),
                        "mentionable": role.get("mentionable", False),
                        "permissions": str(role.get("permissions", "0"))
                    }
                    status, response = api_request("POST", f"/guilds/{self.dest_guild_id}/roles", data)
                    if is_success(status):
                        new_role = response
                        self.role_map[role["id"]] = new_role
                        print_add(f"Created Role: {role['name']}")
                    else:
                        print_error(f"Cannot create role: {role['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Creating roles")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error creating role {role['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in create_roles: {e}")

    def create_categories(self):
        self.progress.next_step("Creating categories...")
        
        try:
            source_channels = self.get_guild_channels(self.source_guild_id)
            if not source_channels:
                return
                
            categories = [c for c in source_channels if c.get("type") == 4]
            total = len(categories)
            
            for i, category in enumerate(categories):
                try:
                    data = {
                        "name": category["name"],
                        "type": 4
                    }
                    
                    if "position" in category:
                        data["position"] = category["position"]
                    
                    status, response = api_request("POST", f"/guilds/{self.dest_guild_id}/channels", data)
                    if is_success(status):
                        self.channel_map[category["id"]] = response
                        print_add(f"Created category: {category['name']}")
                    else:
                        print_error(f"Cannot create category: {category['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Creating categories")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error creating category {category['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in create_categories: {e}")

    def create_text_channels(self):
        self.progress.next_step("Creating text channels...")
        
        try:
            source_channels = self.get_guild_channels(self.source_guild_id)
            if not source_channels:
                return
                
            text_channels = [c for c in source_channels if c.get("type") == 0]
            total = len(text_channels)
            
            for i, channel in enumerate(text_channels):
                try:
                    data = {
                        "name": channel["name"],
                        "type": 0
                    }
                    
                    if "topic" in channel and channel["topic"]:
                        data["topic"] = channel["topic"]
                    if "nsfw" in channel:
                        data["nsfw"] = channel["nsfw"]
                    if "rate_limit_per_user" in channel:
                        data["rate_limit_per_user"] = channel["rate_limit_per_user"]
                    if "position" in channel:
                        data["position"] = channel["position"]
                    if "default_auto_archive_duration" in channel:
                        data["default_auto_archive_duration"] = channel["default_auto_archive_duration"]
                    if "default_thread_rate_limit_per_user" in channel:
                        data["default_thread_rate_limit_per_user"] = channel["default_thread_rate_limit_per_user"]
                    
                    if channel.get("parent_id") and channel["parent_id"] in self.channel_map:
                        data["parent_id"] = int(self.channel_map[channel["parent_id"]]["id"])
                    
                    status, response = api_request("POST", f"/guilds/{self.dest_guild_id}/channels", data)
                    if is_success(status):
                        print_add(f"Created text channel: {channel['name']}")
                    else:
                        print_error(f"Cannot create text channel: {channel['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Creating text channels")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error creating text channel {channel['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in create_text_channels: {e}")

    def create_voice_channels(self):
        self.progress.next_step("Creating voice channels...")
        
        try:
            source_channels = self.get_guild_channels(self.source_guild_id)
            if not source_channels:
                return
                
            voice_channels = [c for c in source_channels if c.get("type") == 2]
            total = len(voice_channels)
            
            for i, channel in enumerate(voice_channels):
                try:
                    data = {
                        "name": channel["name"],
                        "type": 2
                    }
                    
                    if "bitrate" in channel:
                        data["bitrate"] = channel["bitrate"]
                    if "user_limit" in channel:
                        data["user_limit"] = channel["user_limit"]
                    if "position" in channel:
                        data["position"] = channel["position"]
                    if "rtc_region" in channel and channel["rtc_region"]:
                        data["rtc_region"] = channel["rtc_region"]
                    
                    if channel.get("parent_id") and channel["parent_id"] in self.channel_map:
                        data["parent_id"] = int(self.channel_map[channel["parent_id"]]["id"])
                    
                    status, response = api_request("POST", f"/guilds/{self.dest_guild_id}/channels", data)
                    if is_success(status):
                        print_add(f"Created voice channel: {channel['name']}")
                    else:
                        print_error(f"Cannot create voice channel: {channel['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Creating voice channels")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error creating voice channel {channel['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in create_voice_channels: {e}")

    def delete_emojis(self):
        self.progress.next_step("Deleting existing emojis...")
        
        try:
            emojis = self.get_guild_emojis(self.dest_guild_id)
            if not emojis:
                return
                
            total = len(emojis)
            
            for i, emoji in enumerate(emojis):
                try:
                    status, response = api_request("DELETE", f"/guilds/{self.dest_guild_id}/emojis/{emoji['id']}")
                    if is_success(status):
                        print_delete(f"Deleted Emoji: {emoji['name']}")
                    else:
                        print_error(f"Cannot delete emoji: {emoji['name']} (Status {status}) -> {response}")
                    self.progress.show_progress(i + 1, total, "Deleting emojis")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error deleting emoji {emoji['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in delete_emojis: {e}")

    def copy_emojis(self):
        self.progress.next_step("Copying emojis...")
        
        try:
            source_emojis = self.get_guild_emojis(self.source_guild_id)
            if not source_emojis:
                print_info("No emojis to copy")
                return
                
            total = len(source_emojis)
            
            for i, emoji in enumerate(source_emojis):
                try:
                    emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.png"
                    if emoji.get("animated"):
                        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.gif"
                    
                    response = requests.get(emoji_url)
                    if response.status_code == 200:
                        emoji_b64 = base64.b64encode(response.content).decode('utf-8')
                        data = {
                            "name": emoji["name"],
                            "image": f"data:image/png;base64,{emoji_b64}"
                        }
                        status, resp = api_request("POST", f"/guilds/{self.dest_guild_id}/emojis", data)
                        if is_success(status):
                            print_add(f"Created Emoji: {emoji['name']}")
                        else:
                            print_error(f"Cannot create emoji: {emoji['name']} (Status {status}) -> {resp}")
                    else:
                        print_error(f"Could not download emoji: {emoji['name']} (HTTP {response.status_code})")
                    self.progress.show_progress(i + 1, total, "Copying emojis")
                    self.rate_limiter.wait()
                except Exception as e:
                    print_error(f"Error creating emoji {emoji['name']}: {e}")
                    
            print()
        except Exception as e:
            print_error(f"Error in copy_emojis: {e}")

    def clone(self):
        source_guild = self.get_guild_info(self.source_guild_id)
        dest_guild = self.get_guild_info(self.dest_guild_id)
        
        if not source_guild or not dest_guild:
            print_error("Could not get guild info")
            return
            
        print(f"\n{Fore.CYAN}Cloning: {source_guild['name']} → {dest_guild['name']}{Style.RESET_ALL}")
        print("=" * 60)
        
        self.delete_channels()
        self.delete_roles()
        self.delete_emojis()
        
        self.edit_guild()
        self.create_roles()
        self.create_categories()
        self.create_text_channels()
        self.create_voice_channels()
        self.copy_emojis()
        
        print("=" * 60)
        completion_banner = r"""
            Finished
        """
        print(f"{Fore.BLUE}{completion_banner}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        test_status, test_response = api_request("GET", "/users/@me")
        if is_success(test_status):
            print_info(f"Valid Token!: {test_response.get('username', 'Unknown')}")
            cloner = Cloner(input_guild_id, output_guild_id)
            cloner.clone()
        elif test_status == 401:
            print_error(f"Invalid token! Please verify its a valid token")
            print_error(f"Response: {test_response}")
        else:
            print_error(f"Error: Status {test_status} - {test_response}")
    except Exception as e:
        print_error(f"Error: {e}")

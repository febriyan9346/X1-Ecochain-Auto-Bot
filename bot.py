import os
import time
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import warnings
import sys

warnings.filterwarnings('ignore')
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

os.system('clear' if os.name == 'posix' else 'cls')

init(autoreset=True)

import requests
import json
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

class X1EcoChainBot:
    def __init__(self, private_key=None, proxy=None):
        self.base_url = "https://tapi.kod.af"
        self.session = requests.Session()
        self.token = None
        self.wallet = None
        self.proxy = proxy
        self.user_info = None
        
        if self.proxy:
            self.setup_proxy(proxy)
        
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://testnet.x1ecochain.com",
            "pragma": "no-cache",
            "referer": "https://testnet.x1ecochain.com/",
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        }
        
        if private_key:
            self.setup_wallet(private_key)
    
    def setup_proxy(self, proxy):
        try:
            if not proxy.startswith('http://') and not proxy.startswith('https://') and not proxy.startswith('socks5://'):
                proxy = 'http://' + proxy
            
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
        except Exception as e:
            pass
    
    def setup_wallet(self, private_key):
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key
        
        try:
            self.wallet = Account.from_key(private_key)
        except Exception as e:
            pass
    
    def create_signature(self, message):
        if not self.wallet:
            raise Exception("Wallet belum di-setup!")
        
        encoded_msg = encode_defunct(text=message)
        signed = self.wallet.sign_message(encoded_msg)
        return signed.signature.hex()
    
    def get_signin_message(self):
        if not self.wallet:
            raise Exception("Wallet belum di-setup!")
        
        endpoints = [
            f"/auth/message?address={self.wallet.address}",
            f"/message?address={self.wallet.address}",
            f"/auth/nonce?address={self.wallet.address}",
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    data = response.json()
                    message = (
                        data.get('message') or 
                        data.get('data', {}).get('message') or
                        data.get('nonce') or
                        data.get('data', {}).get('nonce')
                    )
                    if message:
                        return message
            except:
                continue
        
        return "X1 Testnet Auth"
    
    def get_user_info(self):
        if not self.token:
            return None
        
        url = f"{self.base_url}/me"
        headers = self.headers.copy()
        headers['authorization'] = self.token
        
        try:
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.user_info = data
                return data
            else:
                return None
        except Exception as e:
            return None
    
    def signin(self, signature=None, custom_message=None):
        url = f"{self.base_url}/signin"
        
        if not signature:
            if not self.wallet:
                raise Exception("Wallet atau signature harus disediakan!")
            
            message = custom_message or "X1 Testnet Auth"
            signature = self.create_signature(message)
            
            if not signature.startswith('0x'):
                signature = '0x' + signature
        
        payload = {"signature": signature}
        
        try:
            response = self.session.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.token = data.get('token') or data.get('access_token') or data.get('data', {}).get('token')
                    return True
                except json.JSONDecodeError as e:
                    return False
            else:
                return False
                
        except Exception as e:
            return False
    
    def claim_faucet(self):
        if not self.wallet or not self.token:
            return {'success': False, 'message': 'Not configured', 'already_done': False}
        
        url = "https://nft-api.x1.one/testnet/faucet"
        
        headers = self.headers.copy()
        headers["authorization"] = self.token
        
        params = {"address": self.wallet.address}
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {'success': True, 'message': 'Claimed', 'data': data, 'already_done': False}
            else:
                error_msg = response.text
                if "24 hours" in error_msg or "once every" in error_msg:
                    return {'success': False, 'message': 'Already claimed (24h cooldown)', 'already_done': True}
                else:
                    return {'success': False, 'message': 'Claim failed', 'already_done': False}
        except Exception as e:
            return {'success': False, 'message': str(e), 'already_done': False}
    
    def complete_quest(self, quest_id):
        if not self.token:
            return None
        
        url = f"{self.base_url}/quests"
        headers = self.headers.copy()
        headers['authorization'] = self.token
        headers['content-length'] = '0'
        params = {"quest_id": quest_id}
        
        try:
            response = self.session.post(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                reward = data.get('reward', 0)
                return {'success': True, 'reward': reward, 'already_claimed': False}
            else:
                error_msg = response.text.lower()
                if "already" in error_msg or "claimed" in error_msg or "completed" in error_msg:
                    return {'success': False, 'already_claimed': True, 'reward': 0}
                else:
                    return {'success': False, 'already_claimed': False, 'reward': 0}
        except Exception as e:
            return {'success': False, 'already_claimed': False, 'reward': 0}
    
    def get_quests(self):
        if not self.token:
            return None
        
        url = f"{self.base_url}/quests"
        headers = self.headers.copy()
        headers['authorization'] = self.token
        
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
    
    def auto_complete_quests(self):
        quests = self.get_quests()
        if not quests:
            return {'completed': 0, 'total_reward': 0, 'quest_details': []}
        
        quest_list = []
        if isinstance(quests, dict):
            quest_list = quests.get('quests', []) or quests.get('data', [])
        elif isinstance(quests, list):
            quest_list = quests
        
        if not quest_list:
            return {'completed': 0, 'total_reward': 0, 'quest_details': []}
        
        completed = 0
        total_reward = 0
        quest_details = []
        
        for quest in quest_list:
            quest_id = quest.get('_id') or quest.get('id')
            quest_name = quest.get('name') or quest.get('title', 'Unknown Quest')
            is_completed = quest.get('completed', False)
            
            if is_completed:
                quest_details.append({
                    'name': quest_name,
                    'status': 'already_completed',
                    'reward': 0
                })
            else:
                time.sleep(random.randint(1, 2))
                result = self.complete_quest(quest_id)
                if result and result.get('success'):
                    completed += 1
                    reward = result.get('reward', 0)
                    total_reward += reward
                    quest_details.append({
                        'name': quest_name,
                        'status': 'completed',
                        'reward': reward
                    })
                elif result and result.get('already_claimed'):
                    quest_details.append({
                        'name': quest_name,
                        'status': 'already_completed',
                        'reward': 0
                    })
                else:
                    quest_details.append({
                        'name': quest_name,
                        'status': 'failed',
                        'reward': 0
                    })
        
        return {'completed': completed, 'total_reward': total_reward, 'quest_details': quest_details}


class BotManager:
    def __init__(self):
        self.wib = pytz.timezone('Asia/Jakarta')
    
    def get_wib_time(self):
        return datetime.now(self.wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}X1 ECOCHAIN AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self, min_sec=1, max_sec=3):
        delay = random.randint(min_sec, max_sec)
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def load_private_keys(self, filename="accounts.txt"):
        if not os.path.exists(filename):
            self.log(f"File {filename} not found!", "ERROR")
            self.log(f"Creating sample file: {filename}", "INFO")
            with open(filename, 'w') as f:
                f.write("# Enter your private keys here, one per line\n")
                f.write("# Example: 0x1234567890abcdef...\n")
            return []
        
        private_keys = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                clean_key = line.replace('0x', '')
                if len(clean_key) == 64:
                    private_keys.append(line)
        return private_keys
    
    def load_proxies(self, filename="proxy.txt"):
        if not os.path.exists(filename):
            self.log(f"File {filename} not found! Running without proxy...", "WARNING")
            with open(filename, 'w') as f:
                f.write("# Enter your proxies here, one per line\n")
                f.write("# Format: protocol://host:port or protocol://user:pass@host:port\n")
                f.write("# Example: http://123.456.789.0:8080\n")
            return []
        
        proxies = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): 
                    continue
                proxies.append(line)
        
        return proxies
    
    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        use_proxy = (choice == '1')
        
        private_keys = self.load_private_keys()
        
        if not private_keys:
            self.log("No accounts found in accounts.txt!", "ERROR")
            return
        
        proxies = []
        if use_proxy:
            proxies = self.load_proxies()
            if proxies:
                self.log(f"Running with proxy", "INFO")
            else:
                self.log("No proxies found, running without proxy", "WARNING")
                use_proxy = False
        else:
            self.log("Running without proxy", "INFO")
        
        self.log(f"Loaded {len(private_keys)} accounts successfully", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(private_keys)
            
            for idx, private_key in enumerate(private_keys, 1):
                self.log(f"Account #{idx}/{total_accounts}", "INFO")
                
                proxy = None
                if use_proxy and proxies:
                    proxy = proxies[(idx - 1) % len(proxies)]
                    proxy_display = proxy.split('@')[-1] if '@' in proxy else proxy
                    self.log(f"Proxy: {proxy_display[:30]}...", "INFO")
                else:
                    self.log(f"Proxy: No Proxy", "INFO")
                
                try:
                    bot = X1EcoChainBot(private_key=private_key, proxy=proxy)
                    
                    if not bot.wallet:
                        self.log(f"Failed to load wallet", "ERROR")
                        continue
                    
                    masked_addr = f"{bot.wallet.address[:6]}...{bot.wallet.address[-4:]}"
                    self.log(f"{masked_addr}", "INFO")
                    
                    self.random_delay(1, 3)
                    
                    if bot.signin():
                        time_str = self.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                    else:
                        self.log(f"Login failed", "ERROR")
                        continue
                    
                    self.random_delay(1, 2)
                    
                    user_info = bot.get_user_info()
                    initial_points = 0
                    rank = "N/A"
                    if user_info:
                        initial_points = user_info.get('points', 0)
                        rank = user_info.get('rank', 'N/A')
                    
                    self.log(f"Processing Tasks:", "INFO")
                    
                    self.random_delay(1, 2)
                    
                    faucet_result = bot.claim_faucet()
                    time_str = self.get_wib_time()
                    if faucet_result.get('success'):
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Task: Claim Faucet | Status: Success{Style.RESET_ALL}")
                    elif faucet_result.get('already_done'):
                        print(f"[{time_str}] {Fore.YELLOW}[WARNING] Task: Claim Faucet | Status: Already Claimed{Style.RESET_ALL}")
                    else:
                        print(f"[{time_str}] {Fore.RED}[ERROR] Task: Claim Faucet | Status: Failed{Style.RESET_ALL}")
                    
                    self.random_delay(1, 2)
                    
                    quest_result = bot.auto_complete_quests()
                    quest_details = quest_result.get('quest_details', [])
                    
                    for quest in quest_details:
                        time_str = self.get_wib_time()
                        quest_name = quest.get('name', 'Unknown')
                        status = quest.get('status', 'unknown')
                        reward = quest.get('reward', 0)
                        
                        if status == 'completed':
                            print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Task: {quest_name} | Reward: +{reward} Points{Style.RESET_ALL}")
                        elif status == 'already_completed':
                            print(f"[{time_str}] {Fore.YELLOW}[WARNING] Task: {quest_name} | Status: Already Completed{Style.RESET_ALL}")
                        elif status == 'failed':
                            print(f"[{time_str}] {Fore.RED}[ERROR] Task: {quest_name} | Status: Failed{Style.RESET_ALL}")
                        
                        time.sleep(0.5)
                    
                    completed_quests = quest_result.get('completed', 0)
                    total_reward = quest_result.get('total_reward', 0)
                    
                    self.random_delay(1, 2)
                    
                    updated_info = bot.get_user_info()
                    final_points = 0
                    if updated_info:
                        final_points = updated_info.get('points', 0)
                        rank = updated_info.get('rank', 'N/A')
                    
                    time_str = self.get_wib_time()
                    points_gained = final_points - initial_points
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Total Points: {final_points:,} | Rank: #{rank} | Today: +{points_gained}{Style.RESET_ALL}")
                    
                    success_count += 1
                
                except Exception as e:
                    self.log(f"Error processing account: {str(e)}", "ERROR")
                
                if idx < total_accounts:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 24 * 60 * 60
            self.countdown(wait_time)

if __name__ == "__main__":
    bot_manager = BotManager()
    bot_manager.run()

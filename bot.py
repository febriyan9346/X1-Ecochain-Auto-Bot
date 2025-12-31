import os
import time
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import warnings
import sys
import requests
import json
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

warnings.filterwarnings('ignore')
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

os.system('clear' if os.name == 'posix' else 'cls')

init(autoreset=True)

class X1EcoChainBot:
    def __init__(self, private_key=None, proxy=None, ref_code=None):
        self.base_url = "https://testnet-api.x1.one"
        self.rpc_url = "https://testnet-rpc.x1.one"
        self.session = requests.Session()
        self.token = None
        self.wallet = None
        self.proxy = proxy
        self.user_info = None
        self.ref_code = ref_code if ref_code is not None else ""
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        if self.proxy:
            self.setup_proxy(proxy)
        
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://testnet.x1ecochain.com",
            "referer": "https://testnet.x1ecochain.com/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
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
        
        return "X1 AuthMessage, Address {}".format(self.wallet.address.lower())
    
    def get_user_info(self):
        if not self.token:
            return None
        
        url = "{}/me".format(self.base_url)
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
    
    def check_points(self):
        if not self.token:
            return None
        
        url = "{}/me".format(self.base_url)
        headers = self.headers.copy()
        headers['authorization'] = self.token
        
        try:
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'points': data.get('points', 0),
                    'ref_points': data.get('ref_points', 0),
                    'rank': data.get('rank', 'N/A'),
                    'referral_rank': data.get('referral_rank', 'N/A'),
                    'referrals_count': data.get('referrals_count', 0),
                    'address': data.get('address', ''),
                    'ref_code': data.get('ref_code', '')
                }
            else:
                return {'success': False}
        except Exception as e:
            return {'success': False}
    
    def signin(self):
        url = "{}/signin".format(self.base_url)
        
        if not self.wallet:
            raise Exception("Wallet harus disediakan!")
        
        message = self.get_signin_message()
        signature = self.create_signature(message)
        
        if not signature.startswith('0x'):
            signature = '0x' + signature
        
        payload = {
            "address": self.wallet.address,
            "ref_code": self.ref_code,
            "signature": signature
        }
        
        try:
            response = self.session.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.token = data.get('token')
                    if data.get('user'):
                        self.user_info = data.get('user')
                    return True
                except json.JSONDecodeError as e:
                    return False
            else:
                return False
                
        except Exception as e:
            return False
    
    def perform_self_transfer(self):
        if not self.wallet:
            return False
        
        try:
            account_address = self.wallet.address
            nonce = self.web3.eth.get_transaction_count(account_address)
            gas_price = self.web3.eth.gas_price
            
            amount_in_ether = 0.011 
            value = self.web3.to_wei(amount_in_ether, 'ether')
            
            tx = {
                'nonce': nonce,
                'to': account_address, 
                'value': value,
                'gas': 21000,
                'gasPrice': gas_price,
                'chainId': self.web3.eth.chain_id
            }
            
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.wallet.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True
        except Exception as e:
            return False

    def claim_faucet(self):
        if not self.wallet or not self.token:
            return {'success': False, 'message': 'Not configured', 'already_done': False}
        
        url = "{}/faucet".format(self.base_url)
        
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
    
    def complete_quest_request(self, quest_id):
        if not self.token:
            return None
        
        url = "{}/quests".format(self.base_url)
        headers = self.headers.copy()
        headers['authorization'] = self.token
        headers['areyouahuman'] = 'true'
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
        
        url = "{}/quests".format(self.base_url)
        headers = self.headers.copy()
        headers['authorization'] = self.token
        headers['areyouahuman'] = 'true'
        
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
    
    def process_quests(self):
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
        
        completed_count = 0
        total_reward = 0
        quest_details = []
        
        for quest in quest_list:
            quest_id = quest.get('id')
            quest_title = quest.get('title', 'Unknown Quest')
            quest_type = quest.get('type')
            periodicity = quest.get('periodicity')
            
            is_completed = quest.get('is_completed', False)
            is_completed_today = quest.get('is_completed_today', False)
            
            should_process = False
            
            if periodicity == 'one_time':
                if not is_completed:
                    should_process = True
            elif periodicity == 'daily':
                if not is_completed_today:
                    should_process = True
            
            if not should_process:
                quest_details.append({
                    'name': quest_title,
                    'status': 'already_completed',
                    'reward': 0
                })
                continue
            
            time.sleep(random.randint(1, 2))
            
            if quest_type == 'transfer':
                print(f"{Fore.CYAN}    -> Performing On-Chain Transfer for Quest...{Style.RESET_ALL}")
                tx_success = self.perform_self_transfer()
                if tx_success:
                    print(f"{Fore.GREEN}    -> Transfer Success! Verifying...{Style.RESET_ALL}")
                    time.sleep(2)
                else:
                    print(f"{Fore.RED}    -> Transfer Failed (Insufficient Balance?){Style.RESET_ALL}")
                    quest_details.append({'name': quest_title, 'status': 'failed', 'reward': 0})
                    continue

            result = self.complete_quest_request(quest_id)
            
            if result and result.get('success'):
                completed_count += 1
                reward = result.get('reward', 0)
                total_reward += reward
                quest_details.append({
                    'name': quest_title,
                    'status': 'completed',
                    'reward': reward
                })
            elif result and result.get('already_claimed'):
                quest_details.append({
                    'name': quest_title,
                    'status': 'already_completed',
                    'reward': 0
                })
            else:
                quest_details.append({
                    'name': quest_title,
                    'status': 'failed',
                    'reward': 0
                })
        
        return {'completed': completed_count, 'total_reward': total_reward, 'quest_details': quest_details}


class BotManager:
    def __init__(self):
        self.wib = pytz.timezone('Asia/Jakarta')
        self.ref_code = ""
    
    def get_wib_time(self):
        return datetime.now(self.wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = """
{}X1 ECOCHAIN AUTO BOT{}
{}By: FEBRIYAN{}
{}============================================================{}
""".format(Fore.CYAN, Style.RESET_ALL, Fore.WHITE, Style.RESET_ALL, Fore.CYAN, Style.RESET_ALL)
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
        
        print("[{}] {}{} {}{}".format(time_str, color, symbol, message, Style.RESET_ALL))
    
    def random_delay(self, min_sec=1, max_sec=3):
        delay = random.randint(min_sec, max_sec)
        time.sleep(delay)
    
    def show_menu(self):
        print("{}============================================================{}".format(Fore.CYAN, Style.RESET_ALL))
        print("{}Select Mode:{}".format(Fore.CYAN, Style.RESET_ALL))
        print("{}1. Run with proxy".format(Fore.GREEN))
        print("2. Run without proxy{}".format(Style.RESET_ALL))
        print("{}============================================================{}".format(Fore.CYAN, Style.RESET_ALL))
        
        while True:
            try:
                choice = input("{}Enter your choice (1/2): {}".format(Fore.GREEN, Style.RESET_ALL)).strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print("{}Invalid choice! Please enter 1 or 2.{}".format(Fore.RED, Style.RESET_ALL))
            except KeyboardInterrupt:
                print("\n{}Program terminated by user.{}".format(Fore.RED, Style.RESET_ALL))
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print("\r[COUNTDOWN] Next cycle in: {:02d}:{:02d}:{:02d} ".format(hours, minutes, secs), end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def load_private_keys(self, filename="accounts.txt"):
        if not os.path.exists(filename):
            self.log("File {} not found!".format(filename), "ERROR")
            self.log("Creating sample file: {}".format(filename), "INFO")
            with open(filename, 'w') as f:
                f.write("0x1234567890abcdef...\n")
            return []
        
        private_keys = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): 
                    continue
                clean_key = line.replace('0x', '')
                if len(clean_key) == 64:
                    private_keys.append(line)
        return private_keys
    
    def load_proxies(self, filename="proxy.txt"):
        if not os.path.exists(filename):
            self.log("File {} not found! Running without proxy...".format(filename), "WARNING")
            with open(filename, 'w') as f:
                f.write("http://123.456.789.0:8080\n")
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
                self.log("Running with proxy", "INFO")
            else:
                self.log("No proxies found, running without proxy", "WARNING")
                use_proxy = False
        else:
            self.log("Running without proxy", "INFO")
        
        self.log("Loaded {} accounts successfully".format(len(private_keys)), "INFO")
        
        print("\n{}============================================================{}\n".format(Fore.CYAN, Style.RESET_ALL))
        
        cycle = 1
        while True:
            self.log("Cycle #{} Started".format(cycle), "CYCLE")
            print("{}------------------------------------------------------------{}".format(Fore.CYAN, Style.RESET_ALL))
            
            success_count = 0
            total_accounts = len(private_keys)
            
            for idx, private_key in enumerate(private_keys, 1):
                self.log("Account #{}/{}".format(idx, total_accounts), "INFO")
                
                proxy = None
                if use_proxy and proxies:
                    proxy = proxies[(idx - 1) % len(proxies)]
                    proxy_display = proxy.split('@')[-1] if '@' in proxy else proxy
                    self.log("Proxy: {}...".format(proxy_display[:30]), "INFO")
                else:
                    self.log("Proxy: No Proxy", "INFO")
                
                try:
                    bot = X1EcoChainBot(private_key=private_key, proxy=proxy, ref_code=self.ref_code)
                    
                    if not bot.wallet:
                        self.log("Failed to load wallet", "ERROR")
                        continue
                    
                    masked_addr = "{}...{}".format(bot.wallet.address[:6], bot.wallet.address[-4:])
                    self.log(masked_addr, "INFO")
                    
                    self.random_delay(1, 3)
                    
                    login_result = bot.signin()
                    if login_result:
                        time_str = self.get_wib_time()
                        print("[{}] {}[SUCCESS] Login successful!{}".format(time_str, Fore.GREEN, Style.RESET_ALL))
                    else:
                        self.log("Login failed", "ERROR")
                        continue
                    
                    self.random_delay(1, 2)
                    
                    user_info = bot.get_user_info()
                    initial_points = 0
                    rank = "N/A"
                    if user_info:
                        initial_points = user_info.get('points', 0)
                        rank = user_info.get('rank', 'N/A')
                    
                    self.log("ProcessingTasks...", "INFO")
                    
                    self.random_delay(1, 2)
                    
                    faucet_result = bot.claim_faucet()
                    time_str = self.get_wib_time()
                    if faucet_result.get('success'):
                       print("[{}] {}[SUCCESS] Task: Faucet Claim | Status: Success{}".format(time_str, Fore.GREEN, Style.RESET_ALL))
                    elif faucet_result.get('already_done'):
                        print("[{}] {}[WARNING] Task: Faucet Claim | Status: Cooldown{}".format(time_str, Fore.YELLOW, Style.RESET_ALL))
                    
                    self.random_delay(2, 4)
                    
                    quest_result = bot.process_quests()
                    quest_details = quest_result.get('quest_details', [])
                    
                    for quest in quest_details:
                        time_str = self.get_wib_time()
                        quest_name = quest.get('name', 'Unknown')
                        status = quest.get('status', 'unknown')
                        reward = quest.get('reward', 0)
                        
                        if status == 'completed':
                            print("[{}] {}[SUCCESS] Task: {} | Reward: +{} Points{}".format(time_str, Fore.GREEN, quest_name, reward, Style.RESET_ALL))
                        elif status == 'already_completed':
                            print("[{}] {}[WARNING] Task: {} | Status: Already Completed{}".format(time_str, Fore.YELLOW, quest_name, Style.RESET_ALL))
                        elif status == 'failed':
                            print("[{}] {}[ERROR] Task: {} | Status: Failed{}".format(time_str, Fore.RED, quest_name, Style.RESET_ALL))
                        
                        time.sleep(0.5)
                    
                    self.random_delay(1, 2)
                    
                    points_info = bot.check_points()
                    if points_info and points_info.get('success'):
                        time_str = self.get_wib_time()
                        final_points = points_info.get('points', 0)
                        ref_points = points_info.get('ref_points', 0)
                        rank = points_info.get('rank', 'N/A')
                        referral_rank = points_info.get('referral_rank', 'N/A')
                        referrals_count = points_info.get('referrals_count', 0)
                        points_gained = final_points - initial_points
                        
                        print("[{}] {}[SUCCESS] Total Points: {:,} | Ref Points: {} | Rank: #{}{}".format(
                            time_str, Fore.GREEN, final_points, ref_points, rank, Style.RESET_ALL))
                        print("[{}] {}[SUCCESS] Referral Rank: #{} | Referrals: {} | Today Gained: +{}{}".format(
                            time_str, Fore.GREEN, referral_rank, referrals_count, points_gained, Style.RESET_ALL))
                    
                    success_count += 1
                
                except Exception as e:
                    self.log("Error processing account: {}".format(str(e)), "ERROR")
                
                if idx < total_accounts:
                    print("{}............................................................{}".format(Fore.WHITE, Style.RESET_ALL))
                    time.sleep(2)
            
            print("{}------------------------------------------------------------{}".format(Fore.CYAN, Style.RESET_ALL))
            self.log("Cycle #{} Complete | Success: {}/{}".format(cycle, success_count, total_accounts), "CYCLE")
            print("{}============================================================{}\n".format(Fore.CYAN, Style.RESET_ALL))
            
            cycle += 1
            
            wait_time = 24 * 60 * 60
            self.countdown(wait_time)

if __name__ == "__main__":
    bot_manager = BotManager()
    bot_manager.run()

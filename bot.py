import requests
import json
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
import time
import os
import sys
from datetime import datetime, timedelta, timezone
from colorama import Fore, Back, Style, init

# Inisialisasi Colorama (autoreset=True agar warna otomatis kembali normal)
init(autoreset=True)

# ==================== SETTINGAN TAMPILAN ====================
def get_wib_time():
    """Mendapatkan waktu WIB (UTC+7)"""
    utc_now = datetime.now(timezone.utc)
    wib_time = utc_now + timedelta(hours=7)
    return wib_time.strftime("%H:%M:%S")

def log(message, type="INFO"):
    """
    Fungsi custom logging dengan warna dan waktu WIB
    Type: INFO, SUCCESS, ERROR, WARNING, PROCESS
    """
    time_str = f"{Fore.CYAN}{Style.BRIGHT}[{get_wib_time()}]{Style.RESET_ALL}"
    
    if type == "INFO":
        print(f"{time_str} {Fore.WHITE}{Style.BRIGHT}ℹ️  {message}{Style.RESET_ALL}")
    elif type == "SUCCESS":
        print(f"{time_str} {Fore.GREEN}{Style.BRIGHT}✅ {message}{Style.RESET_ALL}")
    elif type == "ERROR":
        print(f"{time_str} {Fore.RED}{Style.BRIGHT}❌ {message}{Style.RESET_ALL}")
    elif type == "WARNING":
        print(f"{time_str} {Fore.YELLOW}{Style.BRIGHT}⚠️  {message}{Style.RESET_ALL}")
    elif type == "PROCESS":
        print(f"{time_str} {Fore.MAGENTA}{Style.BRIGHT}⏳ {message}{Style.RESET_ALL}")
    elif type == "HEADER":
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'═'*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{' '*58}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}║  {Fore.WHITE}{message.center(54)}{Fore.CYAN}  ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}║{' '*58}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*60}{Style.RESET_ALL}\n")
    elif type == "SUBHEADER":
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}┌{'─'*58}┐{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}│  {Fore.WHITE}🔸 {message}{' '*(53-len(message))}{Fore.YELLOW}│{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}└{'─'*58}┘{Style.RESET_ALL}")
    elif type == "CLAIMED":
        print(f"{time_str} {Fore.BLUE}{Style.BRIGHT}✔️  {message}{Style.RESET_ALL}")
    else:
        print(f"{time_str} {message}")

def print_banner():
    """Cetak banner aplikasi yang menarik"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          🚀  X1 ECOCHAIN AUTOMATION BOT  🚀              ║
    ║                                                           ║
    ║              {Fore.YELLOW}Advanced Multi-Account Manager{Fore.CYAN}               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.WHITE}{Style.DIM}    Version 2.0 | Developed with ❤️  | Enhanced UI Edition{Style.RESET_ALL}
"""
    print(banner)

# ==================== CLASS UTAMA ====================

class X1EcoChainBot:
    def __init__(self, private_key=None):
        """
        Inisialisasi bot dengan private key (opsional)
        """
        self.base_url = "https://tapi.kod.af"
        self.session = requests.Session()
        self.token = None
        self.wallet = None
        
        # Setup headers default
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
    
    def setup_wallet(self, private_key):
        """Setup wallet dari private key"""
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key
        
        try:
            self.wallet = Account.from_key(private_key)
            masked_addr = f"{self.wallet.address[:6]}...{self.wallet.address[-4:]}"
            log(f"Wallet: {Fore.YELLOW}{masked_addr}{Style.RESET_ALL}", "INFO")
        except Exception as e:
            log(f"Failed to load wallet: {e}", "ERROR")
    
    def create_signature(self, message):
        """Buat signature untuk message tertentu"""
        if not self.wallet:
            raise Exception("Wallet belum di-setup! Gunakan setup_wallet() terlebih dahulu.")
        
        encoded_msg = encode_defunct(text=message)
        signed = self.wallet.sign_message(encoded_msg)
        return signed.signature.hex()
    
    def get_signin_message(self):
        """Dapatkan message untuk sign in dari API"""
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
    
    def signin(self, signature=None, custom_message=None):
        """Login ke API menggunakan signature"""
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
                    log("Authentication successful!", "SUCCESS")
                    return data
                except json.JSONDecodeError as e:
                    log(f"JSON Decode Error: {str(e)}", "ERROR")
                    return None
            else:
                log(f"Authentication failed: {response.status_code}", "ERROR")
                return None
                
        except Exception as e:
            log(f"Error during authentication: {str(e)}", "ERROR")
            return None
    
    def make_request(self, method, endpoint, data=None, params=None):
        """Buat request ke API dengan token authentication"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        if self.token:
            headers['authorization'] = f"Bearer {self.token}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise Exception(f"HTTP method tidak didukung: {method}")
            return response
        except Exception as e:
            log(f"Request error: {str(e)}", "ERROR")
            return None
    
    def claim_faucet(self):
        """Claim faucet testnet token"""
        if not self.wallet:
            log("Wallet not configured!", "ERROR")
            return None
        
        if not self.token:
            log("Not authenticated! Please sign in first.", "ERROR")
            return None
        
        url = "https://nft-api.x1.one/testnet/faucet"
        
        headers = self.headers.copy()
        headers["authorization"] = self.token
        
        params = {"address": self.wallet.address}
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                log("Faucet claimed successfully! 💰", "SUCCESS")
                return data
            else:
                error_msg = response.text
                if "24 hours" in error_msg or "once every" in error_msg:
                    log("Faucet already claimed (24h cooldown) ⏰", "CLAIMED")
                else:
                    log(f"Faucet claim failed: {response.status_code}", "ERROR")
                return None
        except Exception as e:
            log(f"Faucet error: {str(e)}", "ERROR")
            return None
    
    def complete_quest(self, quest_id):
        """Complete quest dengan quest_id tertentu"""
        if not self.token:
            log("Not authenticated!", "ERROR")
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
                log(f"Quest completed! Reward: {Fore.YELLOW}{reward} points{Style.RESET_ALL} 🎉", "SUCCESS")
                return data
            else:
                error_msg = response.text.lower()
                if "already completed" in error_msg or "already claimed" in error_msg:
                    log("Quest already claimed ✔️", "CLAIMED")
                elif "invalid" in error_msg:
                    log("Quest unavailable or invalid", "WARNING")
                else:
                    log("Quest already claimed ✔️", "CLAIMED")
                return None
        except Exception as e:
            log(f"Quest error: {str(e)}", "ERROR")
            return None
    
    def get_quests(self):
        """Ambil daftar semua quest yang tersedia"""
        if not self.token:
            log("Not authenticated!", "ERROR")
            return None
        
        url = f"{self.base_url}/quests"
        headers = self.headers.copy()
        headers['authorization'] = self.token
        
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                log(f"Failed to fetch quests: {response.status_code}", "ERROR")
                return None
        except Exception as e:
            log(f"Quest fetch error: {str(e)}", "ERROR")
            return None
    
    def auto_complete_quests(self):
        """Otomatis complete semua quest yang tersedia"""
        quests = self.get_quests()
        if not quests:
            log("No quests available", "WARNING")
            return {}
        
        results = {}
        quest_list = []
        if isinstance(quests, dict):
            quest_list = quests.get('quests', []) or quests.get('data', [])
        elif isinstance(quests, list):
            quest_list = quests
        
        if not quest_list:
            log("No quests in response", "WARNING")
            return {}
        
        completed_count = sum(1 for q in quest_list if q.get('completed', False))
        pending_count = len(quest_list) - completed_count
        
        log(f"Found {Fore.CYAN}{len(quest_list)}{Style.RESET_ALL} quests | "
            f"{Fore.GREEN}{completed_count} completed{Style.RESET_ALL} | "
            f"{Fore.YELLOW}{pending_count} pending{Style.RESET_ALL}", "INFO")
        
        for idx, quest in enumerate(quest_list, 1):
            quest_id = quest.get('_id') or quest.get('id')
            quest_name = quest.get('name') or quest.get('title', 'Unknown Quest')
            is_completed = quest.get('completed', False)
            
            if is_completed:
                results[quest_id] = {'success': True, 'already_completed': True}
            else:
                log(f"[{idx}/{len(quest_list)}] Processing: {Fore.CYAN}{quest_name}{Style.RESET_ALL}", "PROCESS")
                time.sleep(2)
                result = self.complete_quest(quest_id)
                if result:
                    results[quest_id] = {'success': True, 'data': result}
                else:
                    results[quest_id] = {'success': False}
        return results


# ==================== FUNGSI HELPER ====================

def load_private_keys(filename="accounts.txt"):
    """Load private keys dari file"""
    if not os.path.exists(filename):
        log(f"File {filename} not found!", "ERROR")
        log(f"Creating sample file: {filename}", "INFO")
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
            else:
                log(f"Invalid private key (skipped): {line[:10]}...", "WARNING")
    return private_keys

def run_batch_signin(filename="accounts.txt", delay=2):
    private_keys = load_private_keys(filename)
    if not private_keys: return {}
    
    log(f"Batch Sign In - {len(private_keys)} accounts", "HEADER")
    results = {}
    
    for idx, private_key in enumerate(private_keys, 1):
        log(f"Processing Account {idx}/{len(private_keys)}", "SUBHEADER")
        bot = X1EcoChainBot(private_key=private_key)
        result = bot.signin()
        if result:
            results[bot.wallet.address] = {'success': True, 'data': result}
        else:
            results[f"account_{idx}"] = {'success': False}
        if idx < len(private_keys): time.sleep(delay)
    return results

def run_batch_faucet(filename="accounts.txt", delay=3):
    private_keys = load_private_keys(filename)
    if not private_keys: return {}
    
    log(f"Auto Claim Faucet - {len(private_keys)} accounts", "HEADER")
    results = {}
    
    for idx, private_key in enumerate(private_keys, 1):
        log(f"Account {idx}/{len(private_keys)}", "SUBHEADER")
        bot = X1EcoChainBot(private_key=private_key)
        if bot.signin():
            time.sleep(2)
            bot.claim_faucet()
        if idx < len(private_keys): time.sleep(delay)
    return results

def run_batch_quests(filename="accounts.txt", delay=3, quest_ids=None):
    private_keys = load_private_keys(filename)
    if not private_keys: return {}
    
    log(f"Auto Complete Quests - {len(private_keys)} accounts", "HEADER")
    
    for idx, private_key in enumerate(private_keys, 1):
        log(f"Account {idx}/{len(private_keys)}", "SUBHEADER")
        bot = X1EcoChainBot(private_key=private_key)
        if bot.signin():
            time.sleep(2)
            if quest_ids:
                for qid in quest_ids:
                    bot.complete_quest(qid)
                    time.sleep(1)
            else:
                bot.auto_complete_quests()
        if idx < len(private_keys): time.sleep(delay)

def run_full_auto(filename="accounts.txt", delay=3):
    """
    Jalankan semua tasks: sign in, claim faucet, dan complete quests
    """
    private_keys = load_private_keys(filename)
    if not private_keys: return {}
    
    log(f"🤖 X1 ECOCHAIN - FULL AUTOMATION MODE 🤖", "HEADER")
    log(f"Total Accounts: {Fore.YELLOW}{len(private_keys)}{Style.RESET_ALL}", "INFO")
    
    results = {}
    success_count = 0
    
    for idx, private_key in enumerate(private_keys, 1):
        log(f"ACCOUNT {idx} OF {len(private_keys)}", "SUBHEADER")
        
        try:
            # Init Bot
            bot = X1EcoChainBot(private_key=private_key)
            
            # 1. Sign In
            log("Step 1: Authentication", "PROCESS")
            if not bot.signin():
                log("Authentication failed, skipping account", "ERROR")
                continue
            
            time.sleep(1)
            
            # 2. Claim Faucet (silent mode)
            bot.claim_faucet()
            time.sleep(2)
            
            # 3. Complete Quests
            log("Step 2: Processing Quests", "PROCESS")
            bot.auto_complete_quests()
            
            success_count += 1
            log(f"Account {idx} completed successfully! ✨", "SUCCESS")
        
        except Exception as e:
            log(f"Critical error on account {idx}: {str(e)}", "ERROR")
        
        if idx < len(private_keys):
            log(f"Waiting {delay} seconds for next account...", "INFO")
            time.sleep(delay)
            
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'═'*60}{Style.RESET_ALL}")
    log(f"🎯 FINAL SUMMARY: {Fore.GREEN}{success_count}{Style.RESET_ALL}/{Fore.YELLOW}{len(private_keys)}{Style.RESET_ALL} Accounts Completed Successfully", "INFO")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'═'*60}{Style.RESET_ALL}\n")
    return results

def countdown_timer(seconds):
    """Tampilan countdown timer yang cantik"""
    while seconds > 0:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_format = f"{h:02d}:{m:02d}:{s:02d}"
        sys.stdout.write(f"\r{Fore.YELLOW}{Style.BRIGHT}⏰ Next cycle in: {Fore.CYAN}{time_format} {Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    sys.stdout.write("\r" + " "*60 + "\r")

# ==================== MAIN PROGRAM ====================

def main():
    print_banner()
    
    print(f"{Fore.CYAN}{Style.BRIGHT}┌─────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}│                    SELECT MODE                          │{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}└─────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
    
    print(f"  {Fore.WHITE}1.{Style.RESET_ALL} Sign In Only")
    print(f"  {Fore.WHITE}2.{Style.RESET_ALL} Claim Faucet Only")
    print(f"  {Fore.WHITE}3.{Style.RESET_ALL} Complete Quests Only")
    print(f"  {Fore.GREEN}{Style.BRIGHT}4. Full Auto (One Time) ⭐ RECOMMENDED{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}5.{Style.RESET_ALL} Complete Specific Quest (Manual ID)")
    print(f"  {Fore.YELLOW}{Style.BRIGHT}6. Full Auto (24 Hour Loop) 🔄{Style.RESET_ALL}\n")
    
    try:
        choice = input(f"{Fore.GREEN}{Style.BRIGHT}👉 Select option (1-6): {Style.RESET_ALL}").strip()
    except:
        choice = "4"
    
    if choice == "1":
        run_batch_signin()
    elif choice == "2":
        run_batch_faucet()
    elif choice == "3":
        run_batch_quests()
    elif choice == "4":
        run_full_auto()
    elif choice == "5":
        print(f"\n{Fore.CYAN}Enter Quest ID(s) separated by comma:{Style.RESET_ALL}")
        ids = input(f"{Fore.GREEN}Quest ID(s): {Style.RESET_ALL}").strip().split(',')
        clean_ids = [x.strip() for x in ids if x.strip()]
        if clean_ids:
            run_batch_quests(quest_ids=clean_ids)
        else:
            log("Invalid Quest ID", "ERROR")
    elif choice == "6":
        log("24-Hour Loop Mode Activated 🔄", "INFO")
        cycle = 1
        while True:
            log(f"CYCLE #{cycle} STARTED", "HEADER")
            run_full_auto()
            log(f"Cycle #{cycle} completed. Resting for 24 hours...", "WARNING")
            countdown_timer(24 * 60 * 60)
            cycle += 1
    else:
        log("Invalid option selected", "ERROR")

if __name__ == "__main__":
    main()

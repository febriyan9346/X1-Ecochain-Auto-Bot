# 🚀 X1 EcoChain Automation Bot

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

**Advanced Multi-Account Manager** for X1 EcoChain Testnet with beautiful interface and complete features.

![X1 EcoChain Bot Banner](https://via.placeholder.com/800x200/00d4ff/ffffff?text=X1+EcoChain+Automation+Bot)

## ✨ Key Features

- 🔐 **Multi-Account Support** - Manage multiple accounts simultaneously
- 💰 **Auto Claim Faucet** - Automatically claim testnet tokens
- 🎯 **Auto Complete Quests** - Complete all quests automatically
- 🔄 **24-Hour Loop Mode** - Run bot continuously
- 🎨 **Beautiful UI** - Colorful terminal interface with informative logging
- ⚡ **Fast & Efficient** - Optimized for best performance
- 🛡️ **Error Handling** - Robust error handling for maximum stability

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Ethereum wallet private key

## 🔧 Installation

### 1. Clone Repository

```bash
git clone https://github.com/febriyan9346/X1-Ecochain-Auto-Bot.git
cd X1-Ecochain-Auto-Bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install requests eth-account web3 colorama
```

### 3. Setup Accounts

Create `accounts.txt` file and add your private keys (one per line):

```
0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
# Add more private keys as needed
```

⚠️ **IMPORTANT**: Never share your private keys with anyone!

## 🚀 Usage

### Run the Bot

```bash
python bot.py
```

### Menu Options

The bot will display a menu with 6 options:

1. **Sign In Only** - Login all accounts
2. **Claim Faucet Only** - Claim faucet for all accounts
3. **Complete Quests Only** - Complete quests for all accounts
4. **Full Auto (One Time)** ⭐ *RECOMMENDED* - Run all features once
5. **Complete Specific Quest** - Complete quest with specific ID
6. **Full Auto (24 Hour Loop)** 🔄 - Run bot every 24 hours

### Example Output

```
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║          🚀  X1 ECOCHAIN AUTOMATION BOT  🚀          ║
    ║                                                       ║
    ║              Advanced Multi-Account Manager          ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝

[12:34:56] ℹ️  Wallet: 0x1234...5678
[12:34:57] ✅ Authentication successful!
[12:34:59] ✅ Faucet claimed successfully! 💰
[12:35:01] ⏳ Processing: Daily Check-in Quest
[12:35:03] ✅ Quest completed! Reward: 100 points 🎉
```

## 📁 File Structure

```
X1-Ecochain-Auto-Bot/
│
├── bot.py              # Main bot file
├── accounts.txt        # File containing private keys (create yourself)
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── LICENSE            # License file
└── .gitignore         # Git ignore file
```

## ⚙️ Configuration

### Change Delay Between Accounts

Edit the delay parameter in function calls, default is `delay=3` seconds:

```python
run_full_auto(filename="accounts.txt", delay=5)  # Change to 5 seconds
```

### Change Account File

If you want to use a different file instead of `accounts.txt`:

```python
run_full_auto(filename="my_accounts.txt")
```

## 🛡️ Security

- ✅ `accounts.txt` file is already in `.gitignore`
- ✅ Private keys are never sent to external servers
- ✅ Signatures are created locally
- ⚠️ Never commit files containing private keys
- ⚠️ Use testnet wallets only, not your main wallet

## 🐛 Troubleshooting

### Error: Module not found

```bash
pip install -r requirements.txt --upgrade
```

### Error: Invalid private key

Make sure your private key:
- Has 64 characters (without 0x) or 66 characters (with 0x)
- Valid hexadecimal format
- No spaces or extra characters

### Error: Authentication failed

- Check your internet connection
- Make sure API endpoint is still active
- Wait a moment and try again

## 📊 Upcoming Features

- [ ] Proxy support
- [ ] Web dashboard interface
- [ ] Telegram notifications
- [ ] Auto export results to CSV
- [ ] Multi-threading for multiple accounts

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is created for educational purposes and testing on testnet. Use on mainnet or for purposes that violate Terms of Service is at user's own risk.

**Use at your own risk!**

## 💬 Support

If you find bugs or have suggestions:

- 🐛 [Report Bug](https://github.com/febriyan9346/X1-Ecochain-Auto-Bot/issues)
- 💡 [Request Feature](https://github.com/febriyan9346/X1-Ecochain-Auto-Bot/issues)

## 👨‍💻 Author

**Febriyan**

- GitHub: [@febriyan9346](https://github.com/febriyan9346)

## 🌟 Star History

If this project helps you, give a ⭐ to this repository!

---

<div align="center">

Made with ❤️ by Febriyan

**Happy Botting! 🚀**

</div>

# 🚀 X1 EcoChain Automation Bot

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

**Advanced Multi-Account Manager** untuk X1 EcoChain Testnet dengan antarmuka yang cantik dan fitur lengkap.

![X1 EcoChain Bot Banner](https://via.placeholder.com/800x200/00d4ff/ffffff?text=X1+EcoChain+Automation+Bot)

## ✨ Fitur Utama

- 🔐 **Multi-Account Support** - Kelola banyak akun sekaligus
- 💰 **Auto Claim Faucet** - Klaim testnet token otomatis
- 🎯 **Auto Complete Quests** - Selesaikan semua quest secara otomatis
- 🔄 **24-Hour Loop Mode** - Jalankan bot secara continuous
- 🎨 **Beautiful UI** - Antarmuka terminal berwarna dengan logging yang informatif
- ⚡ **Fast & Efficient** - Optimized untuk performa terbaik
- 🛡️ **Error Handling** - Robust error handling untuk stabilitas maksimal

## 📋 Prasyarat

- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Private key wallet Ethereum

## 🔧 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/febriyan9346/X1-Ecochain-Auto-Bot.git
cd X1-Ecochain-Auto-Bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

atau manual:

```bash
pip install requests eth-account web3 colorama
```

### 3. Setup Akun

Buat file `accounts.txt` dan masukkan private key Anda (satu per baris):

```
0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
# Tambahkan lebih banyak private key jika perlu
```

⚠️ **PENTING**: Jangan pernah share private key Anda ke siapapun!

## 🚀 Cara Penggunaan

### Jalankan Bot

```bash
python bot.py
```

### Menu Pilihan

Bot akan menampilkan menu dengan 6 opsi:

1. **Sign In Only** - Login semua akun
2. **Claim Faucet Only** - Klaim faucet untuk semua akun
3. **Complete Quests Only** - Selesaikan quest untuk semua akun
4. **Full Auto (One Time)** ⭐ *RECOMMENDED* - Jalankan semua fitur sekali
5. **Complete Specific Quest** - Selesaikan quest dengan ID tertentu
6. **Full Auto (24 Hour Loop)** 🔄 - Jalankan bot setiap 24 jam

### Contoh Output

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

## 📁 Struktur File

```
X1-Ecochain-Auto-Bot/
│
├── bot.py              # File utama bot
├── accounts.txt        # File berisi private keys (buat sendiri)
├── requirements.txt    # Dependencies Python
├── README.md          # Dokumentasi
├── LICENSE            # License file
└── .gitignore         # Git ignore file
```

## ⚙️ Konfigurasi

### Mengubah Delay Antar Akun

Edit di dalam fungsi yang dipanggil, default `delay=3` detik:

```python
run_full_auto(filename="accounts.txt", delay=5)  # Ubah ke 5 detik
```

### Mengubah File Akun

Jika ingin menggunakan file lain selain `accounts.txt`:

```python
run_full_auto(filename="my_accounts.txt")
```

## 🛡️ Keamanan

- ✅ File `accounts.txt` sudah ada di `.gitignore`
- ✅ Private key tidak pernah dikirim ke server eksternal
- ✅ Signature dilakukan secara lokal
- ⚠️ Jangan pernah commit file yang berisi private key
- ⚠️ Gunakan wallet testnet saja, jangan wallet utama

## 🐛 Troubleshooting

### Error: Module not found

```bash
pip install -r requirements.txt --upgrade
```

### Error: Invalid private key

Pastikan private key Anda:
- Memiliki panjang 64 karakter (tanpa 0x) atau 66 karakter (dengan 0x)
- Format hexadecimal yang valid
- Tidak ada spasi atau karakter tambahan

### Error: Authentication failed

- Cek koneksi internet Anda
- Pastikan API endpoint masih aktif
- Tunggu beberapa saat dan coba lagi

## 📊 Fitur yang Akan Datang

- [ ] Support untuk proxy
- [ ] Dashboard web interface
- [ ] Notifikasi Telegram
- [ ] Auto export hasil ke CSV
- [ ] Multi-threading untuk akun banyak

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## ⚠️ Disclaimer

Bot ini dibuat untuk keperluan edukasi dan testing di testnet. Penggunaan di mainnet atau untuk tujuan yang melanggar Terms of Service adalah tanggung jawab pengguna.

**Use at your own risk!**

## 💬 Support

Jika Anda menemukan bug atau memiliki saran:

- 🐛 [Report Bug](https://github.com/febriyan9346/X1-Ecochain-Auto-Bot/issues)
- 💡 [Request Feature](https://github.com/febriyan9346/X1-Ecochain-Auto-Bot/issues)

## 👨‍💻 Author

**Febriyan**

- GitHub: [@febriyan9346](https://github.com/febriyan9346)

## 🌟 Star History

Jika project ini membantu Anda, berikan ⭐ untuk repository ini!

---

<div align="center">

Made with ❤️ by Febriyan

**Happy Botting! 🚀**

</div>

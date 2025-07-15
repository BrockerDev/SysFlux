# SysFlux — ⚡ Real-Time System Monitor for Linux Terminals ⚡

SysFlux is a powerful, lightweight, and visually appealing terminal-based system monitoring tool for Linux. Inspired by the legendary `htop` and CPU-Z, SysFlux provides real-time, comprehensive insights into your system's CPU, memory, and disk — all elegantly displayed with dynamic updates and intuitive keyboard controls.

---

## 🚀 Features

- **Real-time monitoring:** Continuously updates system metrics with minimal overhead. ⏱️  
- **CPU Details:** Frequencies, model name, architecture, etc. 🧠  
- **Memory Usage:** RAM and swap usage 💾  
- **Disk I/O:** Disk types and total disk usage 💿  
- **Clean UI:** Uses colors and bars for easy interpretation in terminal 🎨  
- **Dependency minimalism:** Written in Python with widely available libraries 🐍  
- **Easy installation:** Single Python script — no heavy dependencies ⚙️  
- **Cross-terminal compatibility:** Works flawlessly in most modern Linux terminal emulators 🖥️  

---

## 📥 Installation

1. **Requirements:**

   - Python 3.8+  
   - `psutil` (for system info)  
   - `py-cpuinfo` (for detailed CPU info)  
   - `blessings` (for terminal UI enhancements)  

2. **Install dependencies:**

```bash
pip install psutil py-cpuinfo blessings
```
> Tip: Use a virtual environment or user-local installation if you face permission issues.

3. **Download SysFlux script:**

```bash
wget https://github.com/BrockerDev/SysFlux/releases/latest/download/sysflux.py
chmod +x sysflux.py
```
4. **Run SysFlux:**

```bash
./sysflux.py
```

## 🎮 Usage

 - Run the script in your terminal.
 - The UI refreshes automatically every second.
 - To quit SysFlux - press `q` on your keyboard

## 💡 Why SysFlux?

*SysFlux is designed for developers, sysadmins, and power users who demand:*

 - Fast, responsive feedback on system health without leaving the terminal.
 - A visually appealing and customizable monitoring experience.
 - Minimal dependencies and easy portability across Linux distros.
 - Open source and extensible codebase for customization.

## 📜 License

This project is licensed under the MIT License.
Author: BrockerDev — passionate Linux enthusiast & developer

# SysFlux: Feel the ⚡flow⚡ of your system!

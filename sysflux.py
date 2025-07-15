import sys
import termios
import tty
import select
import time
import psutil
import cpuinfo
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.console import Group, Console
from rich.text import Text
from datetime import timedelta

console = Console()

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    brand = info.get("brand_raw", "Unknown CPU")
    arch = info.get("arch_string_raw", "Unknown Arch")
    bits = info.get("bits", "N/A")
    freq = psutil.cpu_freq()
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    flags = info.get("flags", [])
    return {
        "Brand": brand,
        "Architecture": arch,
        "Bits": bits,
        "Physical cores": cores,
        "Logical threads": threads,
        "Max Frequency": f"{freq.max:.2f} MHz" if freq else "N/A",
        "Current Frequency": f"{freq.current:.2f} MHz" if freq else "N/A",
        "Flags": flags,
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "Total RAM": f"{mem.total / (1024**3):.2f} GB",
        "Used RAM": f"{mem.used / (1024**3):.2f} GB ({mem.percent}%)",
        "Available RAM": f"{mem.available / (1024**3):.2f} GB",
        "Total Swap": f"{swap.total / (1024**3):.2f} GB",
        "Used Swap": f"{swap.used / (1024**3):.2f} GB ({swap.percent}%)",
    }

def get_disk_info():
    partitions = psutil.disk_partitions(all=False)
    disks = []
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disks.append({
                "Device": p.device,
                "Mountpoint": p.mountpoint,
                "Fstype": p.fstype,
                "Total": f"{usage.total / (1024**3):.2f} GB",
                "Used": f"{usage.used / (1024**3):.2f} GB",
                "Free": f"{usage.free / (1024**3):.2f} GB",
                "Percent": usage.percent,
            })
        except PermissionError:
            continue
    return disks

def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    return str(timedelta(seconds=int(uptime_seconds)))

def create_cpu_panel(cpu_info):
    table = Table.grid(padding=1)
    table.add_column(justify="right")
    table.add_column()
    for k, v in cpu_info.items():
        if k == "Flags":
            flags_text = ", ".join(v[:15])
            if len(v) > 15:
                flags_text += ", ..."
            table.add_row(k, flags_text)
        else:
            table.add_row(k, str(v))
    return Panel(table, title="🖥️ CPU Info", border_style="cyan")

def create_memory_panel(mem_info):
    table = Table.grid(padding=1)
    table.add_column(justify="right")
    table.add_column()
    for k, v in mem_info.items():
        table.add_row(k, v)
    return Panel(table, title="💾 Memory Info", border_style="magenta")

def create_disks_panel(disks):
    table = Table(title="📀 Disk Usage", show_lines=True, border_style="green")
    table.add_column("Device", justify="left")
    table.add_column("Mountpoint", justify="left")
    table.add_column("Type", justify="center")
    table.add_column("Total", justify="right")
    table.add_column("Used", justify="right")
    table.add_column("Free", justify="right")
    table.add_column("Usage", justify="right")
    for d in disks:
        usage_str = f"{d['Percent']}%"
        table.add_row(
            d["Device"],
            d["Mountpoint"],
            d["Fstype"],
            d["Total"],
            d["Used"],
            d["Free"],
            usage_str,
        )
    return table

def create_uptime_panel(uptime_str):
    return Panel(Text(uptime_str, style="bold green"), title="⏱️ System Uptime", border_style="yellow")

def is_key_pressed():
    dr,dw,de = select.select([sys.stdin], [], [], 0)
    return dr != []

def read_key():
    return sys.stdin.read(1) if is_key_pressed() else None

def main():
    # Налаштуємо термінал для неблокуючого зчитування
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                cpu_info = get_cpu_info()
                mem_info = get_memory_info()
                disks = get_disk_info()
                uptime_str = get_uptime()

                cpu_panel = create_cpu_panel(cpu_info)
                mem_panel = create_memory_panel(mem_info)
                disks_panel = create_disks_panel(disks)
                uptime_panel = create_uptime_panel(uptime_str)

                layout = Group(
                    cpu_panel,
                    mem_panel,
                    disks_panel,
                    uptime_panel
                )

                live.update(layout)

                # Перевірка клавіш
                if is_key_pressed():
                    c = read_key()
                    if c.lower() == 'q':
                        console.print("\nExiting... bye!")
                        break

                time.sleep(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()

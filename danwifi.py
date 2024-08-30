from scapy.all import *
from colorama import Fore, Style, init
import speedtest
import time

# Inisialisasi Colorama
init(autoreset=True)

# Teks besar dengan karakter ASCII
def print_large_text(text, color=Fore.GREEN):
    lines = [
        f" {color}______ _                 __   __ _             _        {Style.RESET_ALL}",
        f" {color}|  ____| |                \\ \\ / /| |           | |       {Style.RESET_ALL}",
        f" {color}| |__   | | ___   ___  ___  \\ V / | | ___   ___ | |_ ___  {Style.RESET_ALL}",
        f" {color}|  __|  | |/ _ \\ / _ \\/ _ \\  \\ /  | |/ _ \\ / _ \\| __/ _ \\ {Style.RESET_ALL}",
        f" {color}| |____ | | (_) |  __/  __/  | |   | | (_) | (_) | ||  __/ {Style.RESET_ALL}",
        f" {color}|______||_|\\___/ \\___|\\___|  |_|   |_|\\___/ \\___/ \\__\\___| {Style.RESET_ALL}",
        f" {color}                                                               {Style.RESET_ALL}",
        f" {color}                                                               {Style.RESET_ALL}",
    ]
    for line in lines:
        print(line)

# Fungsi untuk menangani paket Beacon Frame yang diterima
def packet_handler(packet):
    if packet.haslayer(Dot11Beacon):
        ssid = packet[Dot11Elt].info.decode('utf-8', 'ignore')
        bssid = packet[Dot11].addr2
        if ssid not in networks:
            networks[ssid] = bssid

# Daftar untuk menyimpan SSID dan BSSID yang terdeteksi
networks = {}

# Menangkap paket selama 10 detik
def scan_wifi(duration=10):
    print(f"Scanning for {duration} seconds...")
    sniff(prn=packet_handler, timeout=duration)

def test_internet_speed():
    print("Testing internet speed. Please wait...")
    st = speedtest.Speedtest()
    st.get_best_server()
    
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping
    
    print(f"\nDownload Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms")

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Wifi Detection")
        print("2. Test Kecepatan Jaringan")
        print("3. Quit")

        choice = input("Enter your choice (1, 2, or 3): ").strip()

        if choice == '1':
            print_large_text("Danvert")
            scan_wifi()
            print("\nDetected WiFi Networks:")
            for idx, (ssid, bssid) in enumerate(networks.items(), start=1):
                print(f"{idx}. SSID: {ssid}, BSSID: {bssid}")
            networks.clear()  # Clear networks list after displaying
        elif choice == '2':
            test_internet_speed()
        elif choice == '3':
            print("Keluar dari program")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

# Menjalankan menu utama
main_menu()

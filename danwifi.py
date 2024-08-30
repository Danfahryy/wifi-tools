from scapy.all import *
from colorama import Fore, Style, init
import speedtest
import subprocess

# Inisialisasi Colorama
init(autoreset=True)

# Fungsi untuk menangani paket Beacon Frame yang diterima
def packet_handler(packet):
    if packet.haslayer(Dot11Beacon):
        ssid = packet[Dot11Elt].info.decode('utf-8', 'ignore')
        bssid = packet[Dot11].addr2
        if ssid not in networks:
            networks[ssid] = bssid

# Daftar untuk menyimpan SSID dan BSSID yang terdeteksi
networks = {}
interface = 'wlan0'  # Nama interface jaringan

def start_monitor_mode():
    try:
        # Mengaktifkan mode monitor menggunakan airmon-ng
        subprocess.run(['sudo', 'airmon-ng', 'start', interface], check=True)
        print(f"Interface {interface} has been switched to monitor mode.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start monitor mode: {e}")

def stop_monitor_mode():
    try:
        # Menghentikan mode monitor dan mengembalikan ke mode normal
        subprocess.run(['sudo', 'airmon-ng', 'stop', interface + 'mon'], check=True)
        print(f"Monitor mode has been stopped and {interface} has been restored.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop monitor mode: {e}")

def scan_wifi(duration=10):
    try:
        print(f"Scanning for {duration} seconds on interface {interface}...")
        sniff(iface=interface, prn=packet_handler, timeout=duration)
    except PermissionError:
        print("Permission denied: Ensure you are running with administrative rights.")
    except Exception as e:
        print(f"An error occurred: {e}")

def test_wifi_speed():
    print("Testing WiFi speed. Please wait...")
    # Test speed logic here. Placeholder for demonstration.
    print("WiFi Speed Test functionality is not implemented yet.")

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
        print("\nDanvertt Wifi Tools")
        print("Menu:")
        print("1. Start Mode Monitor")
        print("2. Stop Mode Monitor")
        print("3. Wifi Detection")
        print("4. Test Wifi Speed")
        print("5. Test Internet Speed")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            start_monitor_mode()
        elif choice == '2':
            stop_monitor_mode()
        elif choice == '3':
            scan_wifi()
            print("\nDetected WiFi Networks:")
            for idx, (ssid, bssid) in enumerate(networks.items(), start=1):
                print(f"{idx}. SSID: {ssid}, BSSID: {bssid}")
            networks.clear()  # Clear networks list after displaying
        elif choice == '4':
            test_wifi_speed()
        elif choice == '5':
            test_internet_speed()
        elif choice == '6':
            print("Keluar dari program")
            break
        else:
            print("Invalid choice. Please select 1 through 6.")

# Menjalankan menu utama
main_menu()

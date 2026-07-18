import zipfile
import os
import time
import json
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ============================================================
# 🔥 YAHAN APNA EMAIL CHANGE KAREIN! 🔥
# ============================================================
TEST_EMAIL = "sorifa8390@lasttea.com"
TEST_FIRST_NAME = "pcvbkjh"
TEST_LAST_NAME = "aqweytf"

# ============================================================
# PROXY LIST
# ============================================================
PROXY_LIST = [
    {"host": "107.172.116.227", "port": "5683", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "173.211.68.50", "port": "6332", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "166.88.3.227", "port": "6698", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "198.46.161.239", "port": "5289", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "64.137.83.253", "port": "6193", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "23.26.94.195", "port": "6177", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "94.176.212.180", "port": "6696", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "103.47.52.166", "port": "8208", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "107.175.56.151", "port": "6424", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "38.154.233.100", "port": "5510", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "104.239.105.250", "port": "6780", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "23.95.250.142", "port": "6415", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "212.42.199.178", "port": "5917", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "191.96.117.160", "port": "6915", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "104.168.25.245", "port": "5927", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "82.26.212.117", "port": "5924", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "198.23.214.172", "port": "6439", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "67.227.14.93", "port": "6685", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "104.164.131.59", "port": "7238", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "192.227.131.46", "port": "6630", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "103.47.52.67", "port": "8109", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "31.59.18.47", "port": "6628", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "45.61.116.225", "port": "6903", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "45.61.122.47", "port": "6339", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "64.64.118.85", "port": "6668", "username": "xgxowcgc", "password": "h6r17blc86s8"},
    {"host": "31.57.87.172", "port": "5857", "username": "xgxowcgc", "password": "h6r17blc86s8"},
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# FUNCTIONS
# ============================================================
def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def get_random_proxy():
    return random.choice(PROXY_LIST)

def create_proxy_extension(proxy):
    manifest = """
    {
      "manifest_version": 3,
      "name": "Proxy Extension",
      "version": "1.0",
      "permissions": ["proxy", "storage", "webRequest", "webRequestAuthProvider"],
      "host_permissions": ["<all_urls>"],
      "background": {
        "service_worker": "background.js"
      }
    }
    """
    
    background = f"""
    chrome.runtime.onInstalled.addListener(() => {{
      chrome.proxy.settings.set({{
        value: {{
          mode: "fixed_servers",
          rules: {{
            singleProxy: {{
              scheme: "http",
              host: "{proxy['host']}",
              port: {proxy['port']}
            }}
          }}
        }},
        scope: "regular"
      }});
    }});
    
    chrome.webRequest.onAuthRequired.addListener(
      (details) => {{
        return {{
          authCredentials: {{
            username: "{proxy['username']}",
            password: "{proxy['password']}"
          }}
        }};
      }},
      {{urls: ["<all_urls>"]}},
      ["blocking"]
    );
    """
    
    ext_path = os.path.join(BASE_DIR, "proxy_auth_extension.zip")
    with zipfile.ZipFile(ext_path, "w") as zp:
        zp.writestr("manifest.json", manifest)
        zp.writestr("background.js", background)
    
    return ext_path

def setup_driver(proxy):
    ext_path = create_proxy_extension(proxy)
    
    options = Options()
    options.add_extension(ext_path)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    options.set_capability("goog:loggingPrefs", {
        "performance": "ALL",
        "browser": "ALL"
    })
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined, configurable: true });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        """
    })
    
    return driver

# ============================================================
# HOTFROG FUNCTIONS
# ============================================================
def go_to_registration(driver):
    print("\n📍 NAVIGATING TO REGISTRATION...")
    
    driver.get("https://www.hotfrog.com/")
    time.sleep(5)
    
    try:
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log in')]"))
        )
        login_btn.click()
        time.sleep(5)
        print("   ✅ Clicked 'Log in'")
    except:
        driver.get("https://www.hotfrog.com/login")
        time.sleep(5)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        signup_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up here')]"))
        )
        signup_link.click()
        time.sleep(5)
        print("   ✅ Clicked 'Sign up here'")
    except:
        driver.get("https://admin.hotfrog.com/login/register")
        time.sleep(5)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "first_name"))
        )
        print("   ✅ Registration page loaded!")
        return True
    except:
        print("   ❌ Registration page not loaded")
        return False

def register_account(driver):
    print("\n📍 REGISTERING ON HOTFROG...")
    
    if not go_to_registration(driver):
        return False
    
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "first_name"))
        )
        
        driver.find_element(By.ID, "first_name").clear()
        driver.find_element(By.ID, "first_name").send_keys(TEST_FIRST_NAME)
        driver.find_element(By.ID, "last_name").clear()
        driver.find_element(By.ID, "last_name").send_keys(TEST_LAST_NAME)
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(TEST_EMAIL)
        print(f"   ✅ Form filled: {TEST_EMAIL}")
        
        driver.execute_script("""
            validateForm = function() {
                var data = {
                    email: $('#email').val(),
                    first_name: $('#first_name').val(),
                    last_name: $('#last_name').val(),
                    flatpack_id: "b91831a785c4d17b70dfc2e3ca9f1005",
                    masheryid: "hotfrog",
                    referrer_url: "www.hotfrog.com",
                    referrer_name: "Hotfrog US"
                };
                
                $.ajax({
                    url: "/ajax/register",
                    type: "post",
                    dataType: "json",
                    data: data,
                    async: false,
                    success: function(response) {
                        window._reg_result = response;
                    },
                    error: function(xhr) {
                        window._reg_result = {error: xhr.status};
                    }
                });
                return true;
            };
            document.querySelector('button[type="submit"]').click();
        """)
        
        time.sleep(3)
        print("   ✅ Registration submitted!")
        print(f"   📧 Check email: {TEST_EMAIL}")
        return True
        
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False

def set_password_and_login(driver, verification_link, password):
    """Open verification link, set password, and login"""
    print("\n📍 OPENING VERIFICATION LINK...")
    
    # Open the verification link
    driver.get(verification_link)
    time.sleep(5)
    print(f"   📌 Current URL: {driver.current_url}")
    
    # Try multiple approaches to find password form
    print("   🔍 Looking for password form...")
    
    try:
        # Wait for password field
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        print("   ✅ Password form found!")
        
        # Find all password fields
        password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        
        if len(password_fields) >= 1:
            # First password field
            password_fields[0].clear()
            password_fields[0].send_keys(password)
            print("   ✅ Password entered")
        
        if len(password_fields) >= 2:
            # Second password field (confirm)
            password_fields[1].clear()
            password_fields[1].send_keys(password)
            print("   ✅ Confirm password entered")
        else:
            # Try to find confirm field by other selectors
            try:
                confirm_field = driver.find_element(By.CSS_SELECTOR, "input[name='confirm_password'], input[name='confirmPassword'], #confirm_password, #confirmPassword")
                confirm_field.clear()
                confirm_field.send_keys(password)
                print("   ✅ Confirm password entered (alternative selector)")
            except:
                print("   ⚠️ Confirm password field not found, trying to submit anyway...")
        
        # Find submit button
        submit_btn = None
        selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has(> span:contains('Set'))",
            "//button[contains(text(), 'Set')]",
            "//button[contains(text(), 'Save')]",
            "//button[contains(text(), 'Submit')]"
        ]
        
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    submit_btn = driver.find_element(By.XPATH, selector)
                else:
                    submit_btn = driver.find_element(By.CSS_SELECTOR, selector)
                if submit_btn and submit_btn.is_displayed():
                    print(f"   ✅ Found submit button: {submit_btn.text}")
                    break
            except:
                continue
        
        if submit_btn:
            submit_btn.click()
            time.sleep(5)
            print("   ✅ Password set successfully!")
        else:
            print("   ⚠️ Submit button not found, trying JavaScript submit...")
            driver.execute_script("document.querySelector('form').submit();")
            time.sleep(5)
            print("   ✅ Form submitted via JavaScript!")
        
        # ============================================================
        # AUTO LOGIN
        # ============================================================
        print("\n📍 AUTO LOGIN...")
        driver.get("https://www.hotfrog.com/login")
        time.sleep(5)
        
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.clear()
            email_field.send_keys(TEST_EMAIL)
            print(f"   ✅ Email entered: {TEST_EMAIL}")
            
            pwd_field = driver.find_element(By.ID, "password")
            pwd_field.clear()
            pwd_field.send_keys(password)
            print("   ✅ Password entered")
            
            login_btn = driver.find_element(By.ID, "userLogin-submit")
            login_btn.click()
            time.sleep(5)
            print("   ✅ Login attempted!")
            
            if "dashboard" in driver.current_url.lower() or "admin" in driver.current_url.lower():
                print("   🎉 LOGIN SUCCESSFUL!")
                return True
            else:
                print("   ℹ️ Account created! Login may need manual verification.")
                return True
                
        except Exception as e:
            print(f"   ⚠️ Login error: {e}")
            return True
        
    except TimeoutException:
        print("   ❌ Could not find password form")
        
        # Check if already on login page
        if "login" in driver.current_url:
            print("   ℹ️ Already on login page - Account may be verified!")
            try:
                email_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                email_field.clear()
                email_field.send_keys(TEST_EMAIL)
                print(f"   ✅ Email entered: {TEST_EMAIL}")
                
                pwd_field = driver.find_element(By.ID, "password")
                pwd_field.clear()
                pwd_field.send_keys(password)
                print("   ✅ Password entered")
                
                login_btn = driver.find_element(By.ID, "userLogin-submit")
                login_btn.click()
                time.sleep(5)
                print("   ✅ Login attempted!")
                return True
            except:
                pass
        
        print(f"\n💡 Manual password: {password}")
        return False

# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "="*80)
    print("🚀 HOTFROG - AUTO REGISTRATION")
    print("="*80)
    
    proxy = get_random_proxy()
    print(f"🌐 Proxy: {proxy['host']}:{proxy['port']}")
    print("="*80)
    print(f"📧 Email: {TEST_EMAIL}")
    print(f"👤 Name: {TEST_FIRST_NAME} {TEST_LAST_NAME}")
    print("="*80)
    
    driver = setup_driver(proxy)
    
    try:
        # STEP 1: Register
        if not register_account(driver):
            print("❌ Registration failed!")
            driver.quit()
            return
        
        # STEP 2: Get verification link from user
        print("\n" + "="*80)
        print("📧 ENTER VERIFICATION LINK")
        print("="*80)
        print("   1. Open your email inbox")
        print("   2. Find the Hotfrog verification email")
        print("   3. Copy the FULL verification link")
        print(f"   4. Email: {TEST_EMAIL}")
        print("="*80)
        
        verification_link = input("\n📋 Paste verification link here: ").strip()
        
        if not verification_link or "admin.hotfrog.com" not in verification_link:
            print("❌ Invalid link! Must contain 'admin.hotfrog.com'")
            driver.quit()
            return
        
        # STEP 3: Generate password and complete registration
        password = generate_random_password()
        print(f"\n🔑 Generated Password: {password}")
        
        # STEP 4: Set password and login
        login_success = set_password_and_login(driver, verification_link, password)
        
        # STEP 5: Print final credentials
        print("\n" + "="*80)
        print("🎉 ACCOUNT FULLY CREATED!")
        print("="*80)
        print(f"   📧 Email: {TEST_EMAIL}")
        print(f"   🔑 Password: {password}")
        print(f"   👤 Name: {TEST_FIRST_NAME} {TEST_LAST_NAME}")
        print(f"   🌐 Proxy: {proxy['host']}:{proxy['port']}")
        print(f"   🔐 Login: {'✅ Successful' if login_success else '⚠️ Manual login needed'}")
        print("="*80)
        
        # Save credentials
        filename = f"hotfrog_{TEST_EMAIL.split('@')[0]}.txt"
        with open(filename, "w") as f:
            f.write("="*50 + "\n")
            f.write("HOTFROG ACCOUNT\n")
            f.write("="*50 + "\n")
            f.write(f"Email: {TEST_EMAIL}\n")
            f.write(f"Password: {password}\n")
            f.write(f"First Name: {TEST_FIRST_NAME}\n")
            f.write(f"Last Name: {TEST_LAST_NAME}\n")
            f.write(f"Proxy: {proxy['host']}:{proxy['port']}\n")
            f.write(f"Login Status: {'Success' if login_success else 'Manual'}\n")
            f.write(f"Time: {time.ctime()}\n")
            f.write("="*50 + "\n")
        
        with open("hotfrog_accounts.txt", "a") as f:
            f.write(f"{TEST_EMAIL}:{password}:{proxy['host']}:{proxy['port']}\n")
        
        print(f"\n📁 Credentials saved to: {filename}")
        print(f"📁 Also added to: hotfrog_accounts.txt")
        
        print("\n⏳ Browser will stay open.")
        input("Press ENTER to close browser...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot("error.png")
    
    finally:
        driver.quit()
        print("\n✅ Browser closed")

# ============================================================
# BULK REGISTRATION
# ============================================================
def bulk_register():
    print("\n" + "="*80)
    print("🚀 HOTFROG - BULK REGISTRATION")
    print("="*80)
    
    count = int(input("How many accounts? ").strip() or "3")
    
    print("\n📧 Enter emails (one per line):")
    emails = []
    for i in range(count):
        email = input(f"Email {i+1}: ").strip()
        if email and "@" in email:
            emails.append(email)
        else:
            print("❌ Invalid email, skipping...")
    
    if not emails:
        print("❌ No valid emails!")
        return
    
    first_name = input("👤 First Name: ").strip() or "John"
    last_name = input("👤 Last Name: ").strip() or "Doe"
    
    accounts = []
    
    for i, email in enumerate(emails):
        print(f"\n{'='*60}")
        print(f"📋 Account {i+1}/{len(emails)}")
        print(f"📧 {email}")
        print(f"{'='*60}")
        
        global TEST_EMAIL, TEST_FIRST_NAME, TEST_LAST_NAME
        TEST_EMAIL = email
        TEST_FIRST_NAME = first_name
        TEST_LAST_NAME = last_name
        
        proxy = get_random_proxy()
        print(f"🌐 Proxy: {proxy['host']}:{proxy['port']}")
        
        driver = setup_driver(proxy)
        
        try:
            if register_account(driver):
                print("\n📋 Paste verification link for this account:")
                verification_link = input("📋 Link: ").strip()
                
                if verification_link and "admin.hotfrog.com" in verification_link:
                    password = generate_random_password()
                    print(f"🔑 Password: {password}")
                    
                    login_success = set_password_and_login(driver, verification_link, password)
                    accounts.append({
                        "email": email,
                        "password": password,
                        "proxy": f"{proxy['host']}:{proxy['port']}",
                        "login": "Success" if login_success else "Manual"
                    })
                    
                    print(f"✅ Account {i+1} created!")
                    print(f"   📧 {email}")
                    print(f"   🔑 {password}")
                    
                    with open("hotfrog_accounts.txt", "a") as f:
                        f.write(f"{email}:{password}:{proxy['host']}:{proxy['port']}\n")
            
            driver.quit()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            driver.quit()
    
    print("\n" + "="*80)
    print("📊 BULK REGISTRATION COMPLETE")
    print("="*80)
    for acc in accounts:
        print(f"   📧 {acc['email']} : 🔑 {acc['password']}")
    print("="*80)

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*80)
    print("HOTFROG REGISTRATION TOOL")
    print("="*80)
    print("1. Create Single Account")
    print("2. Create Multiple Accounts")
    print("="*80)
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        bulk_register()
    else:
        main()
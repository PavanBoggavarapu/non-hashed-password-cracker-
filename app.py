import streamlit as st
import itertools
import string
import os
import time
import requests

# Function to download rockyou.txt if not found
def download_wordlist(file_path):
    if not os.path.exists(file_path):
        st.warning(f"⚠️ Wordlist '{file_path}' not found. Downloading rockyou.txt...")

        url = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                st.success("✅ Wordlist downloaded successfully!")
            else:
                st.error("❌ Failed to download wordlist. Please upload it manually.")
        except Exception as e:
            st.error(f"❌ Error downloading wordlist: {e}")

# Function to load passwords from a wordlist file
def load_passwords(file_path):
    if not os.path.exists(file_path):
        st.error("❌ Error: Wordlist file not found.")
        return []
    
    try:
        with open(file_path, 'r', encoding="latin-1") as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return []

# Dictionary Attack
def dictionary_attack(target, wordlist):
    for password in wordlist:
        if password == target:
            return f"✅ Password found using Dictionary Attack: {password}"
    return "❌ Dictionary Attack failed."

# Brute-Force Attack
def brute_force_attack(target, max_length=6):
    chars = string.ascii_lowercase + string.digits  # Only lowercase & numbers for speed
    for length in range(1, max_length + 1):
        for attempt in itertools.product(chars, repeat=length):
            guess = ''.join(attempt)
            if guess == target:
                return f"✅ Password found using Brute-Force: {guess}"
    return "❌ Brute-Force Attack failed."

# Rule-Based Attack
def rule_based_attack(target, wordlist):
    for password in wordlist:
        variations = [password, password.upper(), password.lower(), password + "123", "!" + password, password + "!"]
        if target in variations:
            return f"✅ Password found using Rule-Based Attack: {password}"
    return "❌ Rule-Based Attack failed."

# Hybrid Attack (Dictionary + Brute-Force)
def hybrid_attack(target, wordlist):
    for word in wordlist:
        for numbers in itertools.product("0123456789", repeat=3):  # Appends 3-digit numbers
            guess = word + ''.join(numbers)
            if guess == target:
                return f"✅ Password found using Hybrid Attack: {guess}"
    return "❌ Hybrid Attack failed."

# Streamlit UI
st.title("🔐 Password Cracker")

# User input
wordlist_file = st.text_input("Enter wordlist file path (Default: rockyou.txt):", "rockyou.txt")
download_wordlist(wordlist_file)  # Ensure the wordlist is available

target_password = st.text_input("Enter the password to crack:", type="password")
attack_type = st.selectbox("Choose attack type:", ["Dictionary", "Brute-Force", "Hybrid", "Rule-Based"])

# Load the password list
password_list = load_passwords(wordlist_file)

if st.button("Start Attack"):
    start_time = time.time()
    
    if attack_type == "Dictionary":
        result = dictionary_attack(target_password, password_list)
    elif attack_type == "Brute-Force":
        result = brute_force_attack(target_password)
    elif attack_type == "Rule-Based":
        result = rule_based_attack(target_password, password_list)
    elif attack_type == "Hybrid":
        result = hybrid_attack(target_password, password_list)
    else:
        result = "❌ Invalid attack type."
    
    end_time = time.time()
    
    st.success(result)
    st.write(f"⏳ Execution Time: {end_time - start_time:.4f} seconds")
    
    # Log successful attempts
    if "✅" in result:
        cracked_password = result.split(": ")[-1]
        with open("cracked_passwords.txt", "a") as file:
            file.write(f"Password found: {cracked_password}\n")
        st.write(f"✅ Password saved: {cracked_password}")

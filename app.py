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

# Streamlit UI
st.title("🔐 Password Cracker")

wordlist_file = st.text_input("Enter wordlist file path (Default: rockyou.txt):", "rockyou.txt")
download_wordlist(wordlist_file)  # Ensure the wordlist is available

target_password = st.text_input("Enter the password to crack:", type="password")
attack_type = st.selectbox("Choose attack type:", ["Dictionary", "Brute-Force", "Hybrid", "Rule-Based"])

# Load the password list
password_list = load_passwords(wordlist_file)

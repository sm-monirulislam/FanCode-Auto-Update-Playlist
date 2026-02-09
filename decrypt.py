import pyzipper
import os

ZIP_FILE = "FanCode_sm.zip"
EXTRACT_FOLDER = "extracted"

def unzip_main():
    password = os.getenv("ZIP_PASSWORD")
    if not password:
        raise ValueError("ZIP_PASSWORD not found")

    pwd = password.encode("utf-8")

    print("🔐 Extracting ZIP...")

    os.makedirs(EXTRACT_FOLDER, exist_ok=True)

    with pyzipper.AESZipFile(ZIP_FILE) as zf:
        zf.pwd = pwd
        zf.extractall(EXTRACT_FOLDER)

    print("✅ Extracted inside:", EXTRACT_FOLDER)

if __name__ == "__main__":
    unzip_main()

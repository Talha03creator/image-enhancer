import requests
import os

BASE_URL = "http://127.0.0.1:8000"
TEST_ACCOUNT = {"email": "test_enhance@example.com", "password": "password123", "name": "Enhancer Test"}

def test_flow():
    session = requests.Session()
    
    # 1. Register (ignore if exists)
    print("1. Registering...")
    reg_res = session.post(f"{BASE_URL}/auth/register", json=TEST_ACCOUNT)
    print(f"   Register: {reg_res.status_code} {reg_res.text}")

    # 2. Login
    print("\n2. Logging in...")
    login_res = session.post(f"{BASE_URL}/auth/login", json={"email": TEST_ACCOUNT["email"], "password": TEST_ACCOUNT["password"]})
    if login_res.status_code != 200:
        print("   Login Failed!")
        return
    token = login_res.json()["access_token"]
    print("   Login Successful. Token received.")

    # 3. Create dummy image
    print("\n3. Creating dummy image...")
    img_path = "test_image.jpg"
    with open(img_path, "wb") as f:
        f.write(os.urandom(1024)) # Random bytes, might not be valid for cv2.imread if strict, let's make a tiny valid jpg if possible or rely on backend error handling.
    
    # Better: create a tiny real black image
    # We can't easily rely on PIL here if it's not in the environment running THIS script (though it should be).
    # Let's try to verify if backend handles invalid image gracefully or if we can send a simple text file renamed as jpg to see if it even reaches processing.
    # actually, backend uses cv2.imread. If we send random bytes, cv2.imread returns None.
    # backend main.py: if image is None: raise ValueError("Could not load image")
    # So we expect 500 or 400.
    # Let's try to upload a real file if one exists, or skip this if we can't create one easily.
    # CHECK: We have 'd:\AI Course\enhancer\static\style.css'. Not an image.
    
    # Let's create a minimal valid BMP (easier than JPG)
    # BMP Header (14 bytes) + DIB Header (40 bytes) + Pixel Data
    # 1x1 pixel white bmp
    bmp_data = b'BM\x3e\x00\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00'
    with open("test_image.bmp", "wb") as f:
        f.write(bmp_data)

    # 4. Enhance
    print("\n4. Uploading and Enhancing...")
    with open("test_image.bmp", "rb") as f:
        files = {"file": ("test_image.bmp", f, "image/bmp")}
        data = {"filter_type": "grayscale"}
        headers = {"Authorization": f"Bearer {token}"}
        
        # Note: main.py checks extensions: ["jpg", "jpeg", "png"]
        # So BMP might fail validation. Let's rename to .jpg (cv2 relies on content usually, but main.py relies on extension)
        # main.py line 71: if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]
        
    # Rename to jpg for extension validation
    with open("test_image.jpg", "wb") as f:
        f.write(bmp_data)
        
    with open("test_image.jpg", "rb") as f:
        files = {"file": ("test_image.jpg", f, "image/jpeg")}
        enhance_res = requests.post(f"{BASE_URL}/enhance", headers=headers, files=files, data=data)
    
    print(f"   Enhance Status: {enhance_res.status_code}")
    if enhance_res.status_code == 200:
        print("   SUCCESS! Image enhanced.")
        with open("enhanced_output.jpg", "wb") as f:
            f.write(enhance_res.content)
        print("   Saved to enhanced_output.jpg")
    else:
        print(f"   Failed: {enhance_res.text}")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Error: {e}")

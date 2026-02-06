
import requests

def test_enhance():
    url = "http://127.0.0.1:8000/enhance"
    
    # Login first to get token
    auth_url = "http://127.0.0.1:8000/auth/login"
    # We need a user. Register one if not exists or just use a known one.
    import uuid
    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    
    requests.post("http://127.0.0.1:8000/auth/register", json={"email": email, "name": "Tester", "password": password})
    
    # UserLogin schema expects 'email', not 'username'
    login_resp = requests.post(auth_url, json={"email": email, "password": password})
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        return

    # Create valid image
    from PIL import Image
    import io
    
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    valid_image_bytes = img_byte_arr.getvalue()
    
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Prepare file
    files = {'file': ('test_image.jpg', valid_image_bytes, 'image/jpeg')}
    data = {'filter_type': 'auto'}

    try:
        resp = requests.post(url, headers=headers, files=files, data=data)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_enhance()

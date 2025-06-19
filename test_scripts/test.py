import requests

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "test_user"
PASSWORD = "test_password"

def register_user():
    url = f"{BASE_URL}/register"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("[✔] 注册成功")
    elif response.status_code == 400:
        print("[!] 用户已存在")
    else:
        print("[✘] 注册失败:", response.text)

def login_user():
    url = f"{BASE_URL}/login"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("[✔] 登录成功，token:", token)
        return token
    else:
        print("[✘] 登录失败:", response.text)
        return None

def access_protected(token):
    url = f"{BASE_URL}/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("[✔] 成功访问 /me 接口:", response.json())
    else:
        print("[✘] 无法访问 /me:", response.status_code, response.text)

if __name__ == "__main__":
    print("=== 注册 ===")
    register_user()
    print("=== 登录 ===")
    token = login_user()
    if token:
        print("=== 使用 token 访问受保护接口 ===")
        access_protected(token)

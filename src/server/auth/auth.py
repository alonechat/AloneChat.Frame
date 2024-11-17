import hashlib
import os
import getpass

# 用于存储用户信息的文件
BASEDIR   = os.path.dirname(os.path.abspath(__file__))
USERSFILE = os.path.join(BASEDIR, '../../../resource/dynamic/', 'USERS.txt')

# 加载用户数据
def load_users():
    USERS = {}
    if not os.path.exists(USERSFILE):
        return USERS
    with open(USERSFILE, 'r') as file:
        for line in file:
            username, passwd, salt = line.strip().split(':')
            USERS[username] = {
                'hash': bytes.fromhex(passwd), 
                'salt': bytes.fromhex(salt)
            }
    return USERS

# 保存用户数据
def save_users(users):
    with open(USERSFILE, 'w') as file:
        for username, user_info in users.items():
            file.write(
                f'{username}:{user_info["hash"].hex()}:{user_info["salt"].hex()}\n'
            )

# 哈希密码
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = salt
    password = password.encode('utf-8')
    # salt = salt.encode('utf-8')
    hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    return hash, salt

# 注册新用户
def register(username, password):
    if username in USERS:
        print("Username already exists.")
        return False
    hashed_password, salt = hash_password(password)
    USERS[username] = {'hash': hashed_password, 'salt': salt}
    print("Registration successful.")
    return True

# 用户认证
def authenticate(username, password):
    if username not in USERS:
        info = "Username not found."
        return False, info
    user_info = USERS[username]
    hashed_password, salt = hash_password(password, user_info['salt'])
    if hashed_password == user_info['hash']:
        # print("Login successful!")
        return True, 'Successfully.'
    else:
        # print("Login failed.")
        return False, 'Failed.'

def getpasswd():
    try:
        passwd = getpass.getpass('Enter your password: ')
    except Exception as exp:
        pass

    return passwd

# 主函数
def main():
    global USERS
    USERS = load_users()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = getpasswd()
            register(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = getpasswd()
            if authenticate(username, password)[0]:
                print("Login successful!")
            else:
                print("Login failed.")
        elif choice == '3':
            save_users(USERS)
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
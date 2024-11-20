import hashlib
import os
import getpass

from _dns import _dns

# 用于存储用户信息的文件
BASEDIR = os.path.dirname(os.path.abspath(__file__))
USERSFILE = os.path.join(BASEDIR, '../../../resource/dynamic/', 'USERS.txt')

# 加载用户数据
def load_users():
    USERS = {}
    if not os.path.exists(USERSFILE):
        return USERS
    with open(USERSFILE, 'r') as file:
        for line in file:
            username, passwd, salt, groups = line.strip().split(':')
            # Banned users.
            if passwd == salt == '!login':
                continue

            USERS[username] = {
                'hash': bytes.fromhex(passwd), 
                'salt': bytes.fromhex(salt),
                'groups': groups.split(',')
            }
    
    os.remove(USERSFILE)
    return USERS

# 保存用户数据
def save_users(users):
    with open(USERSFILE, 'w') as file:
        # print(users)
        for username, user_info in users.items():
            # print(username, user_info)
            # if username in users and users[username]['hash'] != b'!login':
            groups = ','.join(user_info['groups'])
            file.write(
                f'{username}:{user_info["hash"].hex()}:{user_info["salt"].hex()}:{groups}\n'
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
def register(username, password, groups=None, ip='127.0.0.1'):
    if username in USERS:
        print("Username already exists.")
        return False
    hashed_password, salt = hash_password(password)
    if groups is None:
        groups = ['user']
    USERS[username] = {'hash': hashed_password, 'salt': salt, 'groups': groups}

    dns = _dns._DNS()
    dns.load()
    dns.add_user(username, ip)
    dns.save()
    print("Registration successful.")
    return True

# 用户认证
def authenticate(username, password, ip='127.0.0.1'):
    if username not in USERS:
        info = "Username not found."
        return False, info
    user_info = USERS[username]
    hashed_password, salt = hash_password(password, user_info['salt'])
    if hashed_password == user_info['hash']:
        dns = _dns._DNS()
        dns.load()
        dns.add_user(username, ip)
        dns.save()
        return True, 'Successfully.'
    else:
        return False, 'Failed.'

# 删除用户
def delete_user(username):
    if username in USERS:
        del USERS[username]
        print("User deleted successfully.")
        return True
    else:
        print("User not found.")
        return False

# 更改密码
def change_password(username, old_password, new_password):
    if username not in USERS:
        print("User not found.")
        return False
    user_info = USERS[username]
    hashed_password, salt = hash_password(old_password, user_info['salt'])
    if hashed_password != user_info['hash']:
        print("Incorrect old password.")
        return False
    new_hashed_password, new_salt = hash_password(new_password)
    USERS[username] = {'hash': new_hashed_password, 'salt': new_salt, 'groups': user_info['groups']}
    print("Password changed successfully.")
    return True

# Ban用户
def ban_user(username):
    if username not in USERS:
        print("User not found.")
        return False
    if 'admin' not in [group for group in USERS.get('current_user', {}).get('groups', [])]:
        print("Only admins can ban users.")
        return False
    USERS[username] = {'hash': b'!login', 'salt': b'!login', 'groups': USERS[username]['groups']}
    print("User banned successfully.")
    return True

# 更改用户组
def change_group(username, new_groups):
    if username not in USERS:
        print("User not found.")
        return False
    if 'admin' not in [group for group in USERS.get('current_user', {}).get('groups', [])]:
        print("Only admins can change user groups.")
        return False
    USERS[username]['groups'] = new_groups
    print(f"User '{username}' groups changed to {new_groups}.")
    return True

def getpasswd():
    try:
        passwd = getpass.getpass('Enter your password: ')
    except Warning as exp:
        pass
    return passwd

# 主函数
def main():
    global USERS
    USERS = load_users()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Delete User")
        print("4. Change Password")
        print("5. Ban User")
        print("6. Change User Groups")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = getpasswd()
            groups = input("Enter user groups (comma-separated): ").split(',')
            register(username, password, groups)
        elif choice == '2':
            username = input("Enter your username: ")
            password = getpasswd()
            auth, info = authenticate(username, password)
            if auth:
                print("Login successful!")
                USERS['current_user'] = USERS[username]
            else:
                print("Login failed.")
        elif choice == '3':
            username = input("Enter username to delete: ")
            delete_user(username)
        elif choice == '4':
            username = input("Enter your username: ")
            old_password = getpasswd()
            new_password = getpasswd()
            change_password(username, old_password, new_password)
        elif choice == '5':
            username = input("Enter username to ban: ")
            ban_user(username)
        elif choice == '6':
            username = input("Enter username to change groups: ")
            new_groups = input("Enter new groups (comma-separated): ").split(',')
            change_group(username, new_groups)
        elif choice == '7':
            save_users(USERS)
            if 'current_user' in USERS:
                del USERS['current_user']
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
import os
import json
import time
import socket
import requests
import threading

from cmd import Cmd


class Client(Cmd):
    """
    客户端
    """
    prompt = ''
    intro = """[Welcome] 简易聊天室客户端(Cli版) Tip: 输入help来获取帮助"""

    def __init__(self):
        """
        构造
        """
        super().__init__()
        self.__socket = socket.socket(
            socket.AF_INET6, 
            socket.SOCK_STREAM
        )
        self.__id = None
        self.__nickname = None
        self.__isLogin = False

        self.__messages_list = []

        self.server_ip = requests.requests('ip6.ipw.cn').text

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while self.__isLogin:
            # noinspection PyBroadException
            try:
                buffer = self.__socket.recv(1024).decode()
                obj = json.loads(buffer)
                thismsg = \
                    '[' + str(obj['sender_nickname']) + \
                    '(' + str(obj['sender_id']) + ')' + ']' + \
                    obj['message']
                self.__messages_list.append(thismsg)
                print(thismsg)

                # os.system('clear')

                # for msg in self.__messages_list:
                #     print(msg)

            except Exception:
                print('[Client] 无法从服务器获取数据')

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())

    def start(self):
        """
        启动客户端
        """
        self.__socket.connect((self.server_ip, 8888))
        self.cmdloop()

    def do_register(self, args):
        nickname = args.split(' ')[0]
        password = args.split(' ')[1]

        self.socket.send(json.dumps({
            'type': 'register',
            'nickname': str(nickname),
            'password': password,
            'ip' : self.ip
        }))

        try:
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)

            try:
                if obj['id']:
                    self.__nickname = nickname
                    self.__id = obj['id']
                    self.__isLogin = True
                    print('[Client] 成功登录到聊天室')

                    # 开启子线程用于接受数据
                    thread = threading.Thread(target=self.__receive_message_thread)
                    thread.setDaemon(True)
                    thread.start()
            except:
                print('[Client] 无法登录到聊天室')
        except Exception:
            print('[Client] 无法从服务器获取数据')

    def do_login(self, args):
        """
        登录聊天室
        :param args: 参数
        """
        nickname = args.split(' ')[0]
        password = args.split(' ')[1]

        # 将昵称发送给服务器，获取用户id
        self.__socket.send(json.dumps({
            'type': 'login',
            'nickname': nickname,
            'password': password,
            'ip': self.ip
        }).encode())
        # 尝试接受数据
        # noinspection PyBroadException
        try:
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            if obj['id']:
                self.__nickname = nickname
                self.__id = obj['id']
                self.__isLogin = True
                print('[Client] 成功登录到聊天室')

                # 开启子线程用于接受数据
                thread = threading.Thread(target=self.__receive_message_thread)
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Client] 无法登录到聊天室')
        except Exception:
            print('[Client] 无法从服务器获取数据')

    def do_send(self, args):
        """
        发送消息
        :param args: 参数
        """
        message = args
        # 显示自己发送的消息
        print(
            '[' + str(self.__nickname) + \
            '(' + str(self.__id) + ')' + ']', 
            message
        )
        # 开启子线程用于发送数据
        thread = threading.Thread(target=self.__send_message_thread, args=(message,))
        thread.setDaemon(True)
        thread.start()

        time.sleep(1)

    
    def do_logout(self, args=None):
        """
        登出
        :param args: 参数
        """
        self.__socket.send(json.dumps({
            'type': 'logout',
            'sender_id': self.__id
        }).encode())
        self.__isLogin = False
        return True

    def do_help(self, arg):
        """
        帮助
        :param arg: 参数
        """
        command = arg.split(' ')[0]
        if command == '':
            print(
                '[Help] login nickname - 登录到聊天室，nickname是你选择的昵称'
            )
            print(
                '[Help] send message   - 发送消息，message是你输入的消息'
            )
            print(
                '[Help] logout         - 退出聊天室'
            )
        elif command == 'login':
            print(
                '[Help] login nickname - 登录到聊天室，nickname是你选择的昵称'
            )
        elif command == 'send':
            print(
                '[Help] send message   - 发送消息，message是你输入的消息'
            )
        elif command == 'logout':
            print(
                '[Help] logout         - 退出聊天室'
            )
        else:
            print('[Help] 没有查询到你想要了解的指令')


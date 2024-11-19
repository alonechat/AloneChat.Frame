import os

# 用于存储用户信息的文件
BASEDIR   = os.path.dirname(os.path.abspath(__file__))
USERSFILE = os.path.join(BASEDIR, '../../../../resource/dynamic/', 'dns.pair')

class _DNSPair:
    def __init__(self, name, ip):
        self.__name = name
        self.__ip   = ip
    
    def get(self, option):
        if option in ['ip', 'address']:
            return self.__ip
        elif option in ['name', 'domain', 'user']:
            return self.__name
        else:
            raise IndexError('Error in arguments!')

class _DNS:
    def __init__(self, file = USERSFILE):
        self.__storage    = file
        self.__pool: dict = {'system':'127.0.0.1'}

    def load(self):
        with open(self.__storage, 'r') as file:
            for line in file:
                # 去除每行的首尾空白字符
                line = line.strip()
                # 每行的格式为 "domain:ip_address"
                parts = line.split(':')
                if len(parts) == 2:
                    domain, ip = parts
                    # print(domain, ip)
                    self.__pool[domain] = ip
    
    def save(self):
        with open(self.__storage, 'w') as output_file:
            for domain, ip in self.__pool.items():
                # 将每对DOMAIN-IP写入文件，中间用空格分隔
                output_file.write(f'{domain}:{ip}\n')

    def add_user(self, name, address):
        self.__pool[name] = address

    def get_user(self, name):
        return self.__pool # [name]
    
    '''
    def __del__(self):
        self.save()
        del self.__pool
        del self.__storage
        del self.load
        del self.save
    '''

DNS = _DNS()

DNS.add_user('zcy', '192.168.0.1')
DNS.save()
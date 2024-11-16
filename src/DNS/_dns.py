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
    def __init__(self, file = '../../resource/dynamic/dns.pair'):
        self.__storage    = file
        self.__pool: dict = {'system':'127.0.0.1'}

    def load(self):
        with open(self.__storage, 'r') as file:
            for line in file:
                # 去除每行的首尾空白字符
                line = line.strip()
                # 假设每行的格式为 "domain ip_address"
                parts = line.split()
                if len(parts) == 2:
                    domain, ip = parts
                    domain_ip_dict[domain] = ip
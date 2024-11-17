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
    
    def save(self):
        with open(self.__storage, 'w') as output_file:
            for domain, ip in self.__pool.items():
                # 将每对DOMAIN-IP写入文件，中间用空格分隔
                output_file.write(f'{domain} {ip}\n')
    
    def __del__(self):
        self.save()
        del self.__pool
        del self.__storage
        del self.load
        del self.save
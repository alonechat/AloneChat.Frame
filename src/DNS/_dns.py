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
        with open(self.__storage, 'w') as dns_pairs:
            temp_pool = dns_pairs.readlines
            for pairs in temp_pool:
                unipair = ' '.split(pairs)
                self.__pool[unipair[0]] = unipair[1]
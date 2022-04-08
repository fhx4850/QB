from QB.server import IpTcpServer

if __name__ == '__main__':
    serv = IpTcpServer('127.0.0.1', 8888)
    serv.run()
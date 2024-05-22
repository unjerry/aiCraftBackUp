import socket


ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]
print(ipv6)

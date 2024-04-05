import socket

print("sdf")
# 创建套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("sdf")
# 绑定端口
sock.bind(("localhost", 8000))

print("sdf")
# 监听连接
sock.listen(5)

print("sdf")
# 接受连接
conn, addr = sock.accept()
print("Connected by", addr)

print("sdf")
# 打开文件
with open("received_file.txt", "wb") as f:
    # 接收文件
    while True:
        data = conn.recv(1024)
        if not data:
            break
        f.write(data)

print("sdf")
# 关闭连接
conn.close()

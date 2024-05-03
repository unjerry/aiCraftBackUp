import socket
import time
import threading
import urllib.request
import re
import json


def addFriend(name, ip):
    friendList[name] = {}
    friendList[name]["key"] = None
    friendList[name]["IPv6"] = ip


def setListen(IP, Port):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind((IP, Port))
    s.listen(12)
    print("Listened on ", IP, Port)
    updateIp = re.compile("updateIp:(.*?)::::")
    sendMesspad = re.compile("sendMessage:(.*?):(.*?)::::")
    endupdateIp = re.compile("endupdateIp:(.*?)::::")
    while True:
        conn, addr = s.accept()
        print(time.ctime(), "Connected from ", addr)
        recvd = conn.recv(1024)
        if recvd:
            ss = updateIp.findall(recvd.decode())
            sr = sendMesspad.findall(recvd.decode())
            # print(ss)
            print(sr)
            if not sr == []:
                print(sr)
            if not ss == []:
                filename = ss[0]
            f = open("updateIpfile", "wb")
            while True:
                data = conn.recv(1024)
                if not data:
                    f.close()
                    break
                else:
                    f.write(data)
                    f.flush()

            conn.close()
            with open("updateIpfile", "r") as file:
                ippp = file.read()
            friendList[filename]["IPv6"] = ippp

    s.close()


def tellFriendMyIp(s, name):
    print("tellFriendMyIping ")
    s.sendall(f"updateIp:{name}::::".encode())
    f = open("myCurrentIpv6.out", "rb")
    while True:
        chunk = f.read(1024)
        if not chunk:
            f.close()
            print("%s Successfully Sent \n" % (time.ctime()))
            break
        s.sendall(chunk)
    time.sleep(1)
    s.close()


def sendMessage(it, message):
    iip = friendList[it]["IPv6"]
    print(iip)
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.connect((iip, 12345))
        print("sendMessageing ")
        s.sendall(f"sendMessage:{myName}:{message}::::".encode())
        s.close()
    except:
        print(f"friend:{it}:connectfail")


if __name__ == "__main__":
    # 获取本机的公网IP地址
    ip = urllib.request.urlopen("https://ident.me").read().decode("utf8")
    with open("myCurrentIpv6.out", "w") as file:
        file.write(f"{ip}")
    with open("friendList.json", "r") as file:
        List = json.load(file)
    friendList = List["friendList"]
    myName = List["myName"]
    print(friendList)
    print(myName)
    friendList[myName]["IPv6"] = ip
    t1 = threading.Thread(target=setListen, args=(ip, 12345))
    t1.daemon = True
    t1.start()
    with open("commandHelpFile", "r") as file:
        chf = file.read()
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    for it in friendList:
        iip = friendList[it]["IPv6"]
        print(iip)
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            s.connect((iip, 12345))
            tellFriendMyIp(s, it)
        except:
            print(f"friend:{it}:connectfail")
    while True:
        cmd = input(chf)
        if cmd == "q":
            with open("friendList.json", "w") as file:
                List["friendList"] = friendList
                List["myName"] = myName
                print(friendList, myName)
                json.dump(List, file)
            break
        if cmd == "addFriend":
            nameadf = input("input:name")
            ipaddf = input("input:ip")
            addFriend(nameadf, ipaddf)
        if cmd == "sendMessage":
            namsm = input("input:name")
            mess = input("inputmessage:")
            sendMessage(namsm, mess)

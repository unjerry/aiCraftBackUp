#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import socket, time, os, base64, re
import argparse


def main(IP, Port, log):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind((IP, Port))
    s.listen(12)
    print("Listened on ", IP, Port)
    reg = re.compile("filename:(.*?)::::")

    while True:
        conn, addr = s.accept()
        print(time.ctime(), "Connected from ", addr)
        recvd = conn.recv(1024)
        if recvd:
            ss = reg.findall(recvd.decode())
            print(ss)
            filename = ss[0]
            f = open(filename, "wb")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if data == b"EOF":
                    f.close()
                    log.write("%s Received %s\n" % (time.ctime(), filename))
                    log.flush()
                else:
                    f.write(data)
                    f.flush()
            conn.close()
    s.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manual to the script")
    parser.add_argument(
        "--host", type=str, default="localhost", help="input listening host"
    )
    parser.add_argument(
        "-p", type=int, required=True, help="input listening host's port"
    )
    args = parser.parse_args()
    print(type(args))
    print(args)
    IP = args.host
    Port = args.p
    print(IP)
    print(Port)
    log = open("log.txt", "w+")
    main(IP, Port, log)

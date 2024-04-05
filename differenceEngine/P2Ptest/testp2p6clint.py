#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import socket
import time, os, base64, os.path
import argparse


def SendFile(s, filename):
    print("Sending %s" % filename)
    s.sendall(f"filename:{filename}::::".encode())
    f = open(dirname + filename, "rb")
    while True:
        chunk = f.read(chunksize)
        if not chunk:
            f.close()
            print("%s Successfully Sent %s\n" % (time.ctime(), filename))
            break
        s.sendall(chunk)
    time.sleep(1)
    s.sendall(b"EOF")
    s.close()


def main(dirname, IP, Port, MB=16):
    print("main function is start!")
    for filename in os.listdir(dirname):
        if os.path.isfile(dirname + filename):
            print(filename)
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            s.connect((IP, Port))
            SendFile(s, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manual to the script")
    parser.add_argument("-d", type=str, default="test/", help="input directory")
    parser.add_argument(
        "--host", type=str, required=True, help="input connecting host's ip"
    )
    parser.add_argument("-p", type=int, required=True, help="input host port")
    args = parser.parse_args()
    dirname = args.d
    IP = args.host
    Port = args.p
    MB = 16
    chunksize = int(MB * 1024 * 1024)
    main(dirname, IP, Port, MB)

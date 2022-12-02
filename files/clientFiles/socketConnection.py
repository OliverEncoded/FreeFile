import socket
import os
import sendFile
import receiveFile
import FileName

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096 # send/receive 4096 bytes each time step



host = "server-ip"
port = 1020

def connect():
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    return s

def getFileName(code):
    if len(code) != 2:
        return -1
    if not code.isalpha():
        return -2

    s = connect()
    file_name = FileName.getName(s, code.upper())
    s.close()
    return file_name


def sndFile(filename, pb = -1, lb = -1):
    s = connect()
    code = sendFile.send(s, filename, pb, lb)
    s.close()
    return code


def rcvFile(code, path, file_name, pb = -1, lb = -1):
    s = connect()
    receiveFile.receive(s, code.upper(), path, file_name, pb, lb)
    s.close()


if __name__ == "__main__":
    file_name = ""
    s = socket.socket()
    while True:
        command = input("Command: ")
        if command == "quit" or command == "q" or command == "exit":
            s.close()
            break
        if command.split(" ")[0] == "send":
            print("Code:", sndFile(command.split(" ")[1]))
        if command.split(" ")[0] == "get":
            print("Requesting file")
            code = command.split(" ")[1]
            file_name = getFileName(code)
            if file_name != -1 and file_name != -2:
                path = input("Path or q: ")
                if path != "q":
                    rcvFile(code, path, file_name)




#! usr/bin/env python3.6
import socket, time

if __name__ == "__main__":
    s = None
    try:
        s = socket.socket()
        s.connect(("localhost", 9998))
        s.sendall(bytes("Message!", "utf-8"))
        s.shutdown(socket.SHUT_WR)
        time.sleep(5)
        d = s.recv(1024)
        if d == b"":
            print("Received b''")
        s.shutdown(socket.SHUT_RD)
    except Exception as e:
        print("{}. {}".format(type(e), e))
    finally:
        if s is not None:
            s.close()

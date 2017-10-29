#! usr/bin/env python3.6
import socket, select, threading

def createSockPair():
    try:
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3.bind(("localhost", 10555))
        s3.listen(1)
        s1.connect(("localhost", 10555))
        (s2, addr) = s3.accept()
        s1.setblocking(0)
        s2.setblocking(0)
    finally:
        s3.close()
    return s1, s2

def sendData(s, buff, n = 0):
    bsent = None
    try:
        if isinstance(s, socket.socket) and (n < len(buff)-1):
            l = [s]
            ct, bsent, maxtime = 0, 0, 60
            while True:
                rl, wl, el = select.select(l, l, l, 1)
                for q in wl:
                    bsent += q.send(buff[bsent:])
                for q in el:
                    print("Error from 'select'")
                ct+=1   #time keeper
                if not ct < maxtime:
                    print("maxtime exceeded")
                    break
                if bsent == len(buff):
                    break
    except Exception as e:
        print("{}. {}".format(type(e), e))
    finally:
        return bsent

def recvData(s):
    b = None
    try:
        l = [s]
        ct, maxtime, b = 0, 60, None
        while True:
            rl, wl, el = select.select(l, l, l, 1)
            # for q in rl:
            #     b = q.recv(1024)
            if s in rl:
                b = s.recv(1024)
                break
            ct += 1
            if not ct < maxtime:
                print("maxtime exceeded")
                break
            # if b:
            #     break
    except Exception as e:
        print("{}. {}".format(type(e), e))
    finally:
        return b

def sender(s, buff, n = 0):
    b = sendData(s, buff)
    print("{} bytes sent".format(b))

def recver(s):
    print("Data received: {}".format(str(recvData(s), 'utf-8')))

if __name__ == "__main__":
    a , b = None, None
    try:
        a, b = createSockPair()
        print("Socket pair created")
        ksend = {'s': a, 'buff': b'All aboard the train'}
        krecv = {'s': b}
        t1 = threading.Thread(target=sender, kwargs=ksend)
        t2 = threading.Thread(target=recver, args=(b,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    finally:
        if a is not None and b is not None:
            print("Closing sockets")
            a.close()
            b.close()

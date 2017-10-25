import threading, socket, sys, select, random

trdList = []
gMsg = '{} says "Hi happy server"'

def trdfunc(**kwargs):
    global gMsg
    msg = gMsg.format(threading.current_thread().name)
    HOST, PORT = "localhost", 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(msg, "utf-8"))
        recv = str(sock.recv(1024),"utf-8")
    print("Sent     : {}".format(msg))
    print("Received : {}".format(recv))

def testTrdEchoServer(**kwargs):
    HOST, PORT = "localhost", 9998
    msg = "Clever"
    byteMsg = bytes(msg, "utf-8")
    send_ct = 0
    data_in = ""
    inbuff = bytearray()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
        except Exception as e:
            print("{}. Message: {}".format(type(e), e))
            return
        sock.setblocking(0)
        s_list = [sock]
        send_ct += sock.send(byteMsg[send_ct:])
        while True:
            rlist, wlist, elist = select.select(s_list, s_list, s_list, 1)
            for s in wlist:
                if len(byteMsg) != send_ct:
                    send_ct += sock.send(byteMsg[send_ct:])
            for s in rlist:
                data_in = sock.recv(1024)
                inbuff.extend(data_in)
            for s in elist:
                print("{} Error".format(threading.current_thread().name))
                return
            if len(byteMsg)==len(data_in):
                break
    print("{} Sent     : {}".format(threading.current_thread().name, msg))
    print("{} Received : {}".format(threading.current_thread().name, str(inbuff, 'utf-8')))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            numOfTrds = int(sys.argv[1])
        except Exception as e:
            print("{}".format(type(e)))
    elif len(sys.argv) < 2:
        numOfTrds = 5   #default number of threads
    else:
        print("Usage: python assistant.py 8\n")
        exit()
    try:
        print("Spinning up {} threads".format(numOfTrds))
        for t in range(numOfTrds):
            trdList.append(threading.Thread(target=testTrdEchoServer))
        for t in trdList:
            t.start()
        for t in trdList:
            t.join()
    except Exception as e:
        print("{}".format(type(e)))
        print("Point 1")

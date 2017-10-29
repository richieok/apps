#! usr/bin/env python3.6
import threading, socket, socketserver, select

def reverse(data):
    out = ""
    for c in range(len(data)-1, -1, - 1):
        out = out+data[c]
    return out

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.setblocking(0)
        s_list = [self.request]
        data_in = None
        brecv_data = False
        outbuff = bytearray()
        send_ct = 0
        while True:
            rlist, wlist, elist = select.select(s_list, s_list, s_list, 1)
            for s in rlist:
                if not brecv_data:
                    data_in = str(s.recv(1024), 'utf-8')
                    data_in = reverse(data_in)
                    outbuff.extend(bytes(data_in, 'utf-8'))
                    brecv_data = True
            for s in wlist:
                if data_in:
                    if send_ct == len(outbuff):
                        break
                    else:
                        send_ct += s.send(outbuff[send_ct:])
            for s in elist:
                print("Error on connection")
                break
        self.request.shutdown(socket.SHUT_WR)
        self.request.close()

        #cur_thread = threading.current_thread()
        #response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        #response = bytes("{}".format(data), 'ascii')
        #self.request.sendall(response)

class TestSockHdlr(socketserver.BaseRequestHandler):
    def handle(self):
        s = self.request
        s_list = [self.request]
        s.setblocking(0)
        data_in = None
        inbuff = bytearray()
        try:
            while True:
                rlist, wlist, elist = select.select(s_list, s_list, s_list, 1)
                #using 'if' and not 'for' since the list contains only one socket
                if s in rlist:
                    r = None
                    r = s.recv(1024)
                    if r == b"":
                        print("received empty string")
                        s.shutdown(socket.SHUT_RD)
                        print("RD shutdown")
                        break
                    else:
                        inbuff.extend(r)
                        data_in = str(inbuff, "utf-8")
                        print("Received: {}".format(data_in))
                if s in wlist:
                    if data_in:
                        s.shutdown(socket.SHUT_WR)
                        data_in = None
                        print("WR shutdown")
                        #s.send(b"Rodeo")
                        #break
                if s in elist:
                    print("Error on thread {}".format(threading.current_thread().name))
                    break
        except Exception as e:
            print("{}. {}".format(type(e), e))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    try:
        with ThreadedTCPServer((HOST, PORT), TestSockHdlr) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass

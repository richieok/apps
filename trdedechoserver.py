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

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    try:
        with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass

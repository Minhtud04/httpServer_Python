import socket
from ReqRes.HttpReq import HttpRequest
from ReqRes.HttpRes import HttpResponse
import os
class HttpServer:
    def __init__(self, host, port: int, connectionLimit: int):
        self.host = host
        self.port = port
        self.connectionLimit = connectionLimit
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(self.connectionLimit)
        self.serverSocket.settimeout(5)
        print("Server is listening...")

    def fiveTupleConnection(self, serverSocket: socket, clientSocket: socket):
        protocol = 'TCP'  # default
        serverInfo = {
            'serverIP': serverSocket.getsockname()[0],
            'serverPort': serverSocket.getsockname()[1]
        }
        clientInfo = {
            'clientIP': clientSocket.getpeername()[0],
            'clientPort': clientSocket.getpeername()[1]
        }
        print("New connection from  has been established!")
        print(f"Protocol: {protocol}", f"Server: {serverInfo}", f"Client: {clientInfo}", '\n', sep='\n')

    def acceptConnection(self):
        while True:
            clientSocket, address = self.serverSocket.accept()
            self.fiveTupleConnection(self.serverSocket, clientSocket)

            # handling request-response of client
            while True:
                request = clientSocket.recv(4096).decode()
                print('request', request)
                # check complete request
                if request:
                    httpReq = HttpRequest.requestBuilderFromRequestStr(request)
                    requestHeader = httpReq.getRequestHeaders()
                #check receive full request
                    if 'Content-Length' in requestHeader:
                        while len(httpReq.body) < int(requestHeader['Content-Length']):
                            request += clientSocket.recv(4096).decode()
                            httpReq = HttpRequest.requestBuilderFromRequestStr(request)

                #parse request
                    response = self.parseRequest(httpReq)
                    clientSocket.send(str(response).encode())


    def parseRequest(self, httpRequest: HttpRequest) -> HttpResponse:
        #check method
        if httpRequest.method != 'GET':
            print('405', 'Method Not Allowed')
        #check content-type request:
        if 'Content-Type' not in httpRequest.otherHeaders or httpRequest.otherHeaders['Content-Type'] != 'text/html':
            print('400', 'Only Accept html/text content-type!')
            response = HttpResponse('400', '', '', '', '')
            #errorHandler().errorHandler('400', 'Only Accept html/text content-type!')
            return response

        # handle file search GET request
        getAddress = httpRequest.address
        if os.path.exists(f'./files/{getAddress}'):
            with open(f'../files{getAddress}', 'r') as file:
                body = file.read()
                response = HttpResponse('200', 'text/html', '', str(len(body)), body)
        else:
            response = HttpResponse('404', '', '', '', 'File not found')

        return response

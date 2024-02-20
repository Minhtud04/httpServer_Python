
import socket
import sys

from ReqRes.HttpReq import HttpRequest
from ReqRes.HttpRes import HttpResponse


class HttpClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)


    def createHTTPRequest(self, link:str) -> HttpRequest:
        # link = "http://host:port/address"
        if link[-1] == '/':
            link = link[:-1]
        destructurelize = link.split('/')
        method = "GET"
        address = "/" + "/".join(destructurelize[3:])

        host = destructurelize[2]
        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)

        otherHeaders = {}
        body = ""

        request = HttpRequest(method, address, host, port, otherHeaders, body)
        return request


    def socketConnect(self, request: HttpRequest) -> HttpResponse:
        try:
            self.socket.connect((request.host, request.port))
            res: HttpResponse = self.handleRequest(request, 0)
            self.socket.close()
            return res
        except Exception as e:
            print(e)
            sys.exit(1)

    def handleRequest(self, httpReq: HttpRequest, redirect: int):
        if redirect > 10:
            print('400', 'Redirected too many times')
            return HttpResponse('400', '', '', '', '')

        self.socket.send(str(httpReq).encode())
        responseStr = self.socket.recv(4096).decode()
        httpRes = HttpResponse.responseBuilder(responseStr)

        # Handle large file
        if httpRes.contentLength != '':
            while len(httpRes.body) < int(httpRes.contentLength):
                responseStr = self.socket.recv(4096).decode()
                httpRes.body += responseStr

        # Handle response Code
        if httpRes.code[0] == '3':
            redirect += 1
            print(f"Redirected to {httpRes.location} \nRedirect count: {redirect} \n")
            httpReq = self.createHTTPRequest(httpRes.location)
            return self.handleRequest(httpReq, redirect)

        # Handle error
        elif httpRes.code[0] == '4':
            # self.errorHandler(httpRes.headers['Code'], httpRes.body)
            print('Error')
            print(httpRes)
            return httpRes

        # Handle success
        elif httpRes.code[0] == '2':
            print('Success')
            print(httpRes)
            return httpRes


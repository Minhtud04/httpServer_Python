
class HttpRequest:
    def __init__(self, method, address, host, port, otherHeaders, body):
        self.method = method
        self.address = address
        self.port = port
        self.host = host
        self.otherHeaders: dict = otherHeaders
        self.body = body

    def __str__(self) -> str:
        requestHeader = f"{self.method} {self.address} HTTP/1.1\r\nHost: {self.host}:{self.port}\r\n"
        for key, value in self.otherHeaders.items():
            requestHeader += f"{key}: {value}\r\n"
        request = requestHeader + f"\r\n{self.body}"
        return request

    def requestBuilderFromRequestStr(requestStr: str):
        requestStr = requestStr.split('\r\n')
        requestLine = requestStr[0].split(' ')
        method = requestLine[0]
        address = requestLine[1]
        host = requestStr[1].split(' ')[1].split(':')[0]
        port = requestStr[1].split(' ')[1].split(':')[1]
        otherHeaders = {}
        for i in range(2, len(requestStr)):
            if requestStr[i] == '':
                body = requestStr[i + 1]
                break
            header = requestStr[i].split(': ')
            otherHeaders[header[0]] = header[1]
        body = requestStr[-1]
        return HttpRequest(method, address, host, port, otherHeaders, body)


    def getRequestHeaders(self) -> dict:
       return self.otherHeaders


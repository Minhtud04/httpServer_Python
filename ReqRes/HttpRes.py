class HttpResponse:
    def __init__(self, code, contentType, location, contentLength, body):
        self.code = code
        self.contentType = contentType
        self.contentLength = contentLength
        self.body = body
        self.location = location


    def getResponseBody(self) -> str:
        return self.body


    def getResponseHeader(self) -> str:
        responseHeader = f"HTTP/1.1 {self.code}\r\n"
        if self.contentType != '':
            responseHeader += f"Content-Type: {self.contentType}\r\n"
        if self.contentLength != '':
            responseHeader += f"Content-Length: {self.contentLength}\r\n"
        if self.location != '':
            responseHeader += f"Location: {self.location}\r\n"
        return responseHeader

    def responseBuilder(responseStr: str):
        resBody = responseStr.split('\r\n\r\n')[1]
        resHeaders = {
            'Code': "",
            'Location': "",
            'Content-Type': "",
            'Content-Length': ""
        }
        headers = responseStr.split('\r\n\r\n')[0]
        headers = headers.split('\r\n')  # List of headers
        for header in headers:
            if 'HTTP' in header:
                resHeaders['Code'] = header.split(' ')[1]
            if 'Location' in header:
                resHeaders['Location'] = header
            if 'Content-Type' in header:
                resHeaders['Content-Type'] = header.split(': ')[1]
            if 'Content-Length' in header:
                resHeaders['Content-Length'] = header.split(': ')[1]
        response = HttpResponse(resHeaders['Code'], resHeaders['Content-Type'], resHeaders['Location'], resHeaders['Content-Length'], resBody)
        return response

    def __str__(self) -> str:
        header = self.getResponseHeader()
        body = self.getResponseBody()
        return header + "\r\n" + body


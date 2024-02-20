from httpServer.HttpServer import HttpServer
from ReqRes.HttpReq import HttpRequest
import unittest


request = {
    'basic': HttpRequest('GET', '/basic.html', 'localhost', 4000, {'Content-Type': 'text/html'}, ''),
    'large': HttpRequest('GET', '/test.html', 'localhost', 4000, {'Content-Type': 'text/html'}, ''),
    'miss_content_type': HttpRequest('GET', '/test.html', 'localhost', 4000, {}, ''),
}

class TestServer(unittest.TestCase):
    server = HttpServer("localhost", 4000, 5)

    def test_createHTTPRequest(self):
        self.assertEqual(self.server.host, "localhost")
        self.assertEqual(self.server.port, 4000)

    def test_handleRequest(self):
        #self.assertEqual(self.server.parseRequest(request['basic']).code, "200")
        self.assertEqual(self.server.parseRequest(request['large']).code, "404")
        self.assertEqual(self.server.parseRequest(request['miss_content_type']).code, "400")

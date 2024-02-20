#test client with unittest

import unittest
from httpClient.HttpClient import HttpClient

test = {
    "error404": "http://cs.northwestern.edu/340",
    "redirect301": "http://airbedandbreakfast.com",
    "redirect302": "http://maps.google.com",
    "redirectInf": "http://insecure.stevetarzia.com/redirect-hell",
    "portCheck": "http://portquiz.net:8080/",

    "basic": "http://insecure.stevetarzia.com/basic.html/",
    "redirectBasic": "http://insecure.stevetarzia.com/redirect",
    "large": "http://insecure.stevetarzia.com/libc.html",

    "testServer": 'http://localhost:8080/',
}


class TestClient(unittest.TestCase):
    def test_createHTTPRequest(self, link = test['basic']):
        client = HttpClient()

        request = client.createHTTPRequest(link)
        print(request)
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.address, "/basic.html")
        self.assertEqual(request.host, "insecure.stevetarzia.com")
        self.assertEqual(request.port, 80)
        self.assertEqual(request.otherHeaders, {})
        self.assertEqual(request.body, "")

    def test_createHTTPRequest2(self, link = test['redirect301']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.address, "/")
        self.assertEqual(request.host, "airbedandbreakfast.com")
        self.assertEqual(request.port, 80)
        self.assertEqual(request.otherHeaders, {})
        self.assertEqual(request.body, "")

    def test_createHTTPRequest3(self, link = test['redirect302']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.address, "/")
        self.assertEqual(request.host, "maps.google.com")
        self.assertEqual(request.port, 80)
        self.assertEqual(request.otherHeaders, {})
        self.assertEqual(request.body, "")


class TestClient2(unittest.TestCase):
    def test_socketConnect(self, link = test['basic']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "200")
        self.assertEqual(response.contentType, "text/html")

    def test_socketConnect2(self, link = test['redirect301']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "400")

    def test_socketConnect3(self, link = test['redirect302']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "400")


    def test_socketConnect4(self, link = test['redirectInf']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "400")

    def test_socketConnect5(self, link = test['portCheck']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "200")

    def test_socketConnect6(self, link = test['error404']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "404")

    def test_socketConnect7(self, link = test['large']):
        client = HttpClient()
        request = client.createHTTPRequest(link)
        response = client.socketConnect(request)
        self.assertEqual(response.code, "200")



    # def test_socketConnect8(self, link = test['testServer']):
    #     client = HttpClient()
    #     request = client.createHTTPRequest(link)
    #     response = client.socketConnect(request)
    #     self.assertEqual(response.code, "200")

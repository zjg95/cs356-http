#!/usr/bin/env python3

# -------------------------------
# projects/collatz/TestCollatz.py
# Copyright (C) 2015
# Glenn P. Downing
# -------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from socket import *
import sys

serverName = 'localhost'
serverPort = 4444

def parseResponse (request) :
    # dictionary to hold values
    details = {}

    # list of lines in request
    lines = request.split('\r\n')
    # components of line
    parts = lines[0].split(' ')
    
    details['code'] = parts[1]

    return details

def getResponse (request) :
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    clientSocket.send(request.encode())
    modifiedSentence = clientSocket.recv(2048)

    response = modifiedSentence.decode()
    clientSocket.close()

    return parseResponse(response)

# ------------
# TestTastyTTP
# ------------

class TestTastyTTP (TestCase) :

    def test_code_200_1 (self) :

        request = "GET /testfiles/index.html HTTP/1.1"

        responseDict = getResponse(request)

        self.assertEqual('200', responseDict['code'])

    def test_code_404_1 (self) :

        request = "GET / HTTP/1.1"

        responseDict = getResponse(request)

        self.assertEqual('404', responseDict['code'])

    def test_code_404_2 (self) :

        request = "GET /NonexistentFile HTTP/1.1"

        responseDict = getResponse(request)

        self.assertEqual('404', responseDict['code'])

# ----
# main
# ----

if __name__ == "__main__" :
    main()

from socket import *
import sys

serverName = input("Server: ")
serverPort = int(input("Port: "))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = input('Input lowercase sentence: ')

clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(2048)

print('From Server: ' + modifiedSentence.decode())
clientSocket.close()
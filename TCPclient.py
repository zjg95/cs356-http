from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = input('Input lowercase sentence: ')

clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(2048)

print('From Server: ' + modifiedSentence.decode())
clientSocket.close()

#!/usr/bin/env python3

# -------------------------------
# cs356-http/httpServer.py
# Copyright (C) 2015
# Zachary J. Goodman
# -------------------------------

# -------
# imports
# -------

from socket	import *
from sys import argv, exit
import os
import time

# ----------------
# server meta data
# ----------------

path = os.path.dirname(os.path.abspath(__file__))
serverName = "TastyTTP"
serverVersion = "2.2"
listening = True
MAX_FILE_SIZE = 8192
endl = "\r\n"

# ----------
# HTTP codes
# ----------

codeDict = {
	200 : "200 OK",
	400 : "400 Bad Request",
	404 : "404 Not Found",
	405 : "405 Method Not Allowed",
	415 : "415 Unsupported Media Type",
	418 : "418 I'm a teapot",
	505 : "505 HTTP Version Not Supported"
}

# -----------------
# exception classes
# -----------------

class NonGetRequestException (Exception) :
    pass

class NotFoundException (Exception) :
	pass

class BadRequestException (Exception) :
	pass

class FileTypeNotSupportedException (Exception) :
	pass

class HTTPVersionNotSupportedException (Exception) :
	pass

class CoffeePotException (Exception) :
	pass

# ------------
# time methods
# ------------

def getCurrentTime () :
	return time.gmtime()

def getCurrentTimeString () :
	tnow = getCurrentTime()
	return time.strftime('%a, %d %b %Y %H:%M:%S GMT', tnow)

def getModifiedTime (fileName) :
	modtime = os.path.getmtime(fileName)
	return time.gmtime(modtime)

def getModifiedTimeString (fileName) :
	gmtime = getModifiedTime(fileName)
	return time.strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime)

# --------
# get port
# --------

def getPort () :
	if len(argv) != 2 :
		print("Usage requires exactly one command line argument! python3 httpServer <port>")
		exit()
	return int(argv[1])

# ---------------
# request methods
# ---------------

def getRequest (socket) :
	# receive the request
	request = socket.recv(MAX_FILE_SIZE)
	request = bytes.decode(request)
	print(request)
	return request

def parseRequest (request) :
	# dictionary to hold values
	details = {}
	try :

		# list of lines in request
		lines = request.split('\r\n')
		# components of line
		parts = lines[0].split(' ')
		details["method"] = parts[0].upper()
		if '/' == parts[1][0] :
			parts[1] = path + parts[1]
		else :
			parts[1] = path + '/' + parts[1]
		details["url"] = parts[1]
		details["version"] = parts[2].upper()
		if details["method"] == "BREW" :
			raise CoffeePotException
		if details["version"] != "HTTP/1.1" :
			raise HTTPVersionNotSupportedException
		if details["method"] != "GET" :
			raise NonGetRequestException

	except IndexError :
		raise BadRequestException

	return details

# ------------
# file methods
# ------------

def openFile (fileName, openType) :
	try:
		inputfile = open(fileName, openType)
	except IOError:
		raise NotFoundException
	return inputfile

def openBinaryFile (fileName) :
	# Supported files: JPEG (.jpg or .jpeg)
	inputFile = openFile(fileName, "rb")
	return inputFile.read()

def openTextFile (fileName) :
	# Supported files: HTML (.html or .htm), text (.txt)
	inputFile = openFile(fileName, "r")
	try :
		fileContents = inputFile.read()
	except UnicodeDecodeError :
		raise FileTypeNotSupportedException
	return fileContents

def getFileType (fileName) :
	parts = fileName.split('.')
	if len(parts) == 0 :
		raise NotFoundException
	if len(parts) == 1 :
		return "txt"
	return parts[len(parts) - 1].lower()

# ----------------
# response methods
# ----------------

def getResponse (details) :
	# check if we are sending an image
	image = (False, True)[details["content-type"] == "image/jpeg"]
	response  = ""
	response += details["version"] + " " + details["code"] + endl
	response += "Date: " + getCurrentTimeString() + endl
	response += "Server: " + serverName + "/" + serverVersion + " (" + os.name + ")" + endl
	if details["code"] == codeDict[200] :
		response += "Last-Modified: " + details["modified"] + endl
	response += "Content-Length: " + str(len(details["content"])) + endl
	response += "Content-Type: " + details["content-type"] + endl
	response += endl
	if image :
		# encode the response, excluding the content
		response = response.encode()
	# add the content
	response += details["content"]
	if not image :
		# encode the response, including the content
		response = response.encode()
	return response

def returnResponse (response, socket) :
	# return the result to the client
	socket.send(response)

# ------
# listen
# ------

def listen () :
	while listening:

		# accept the connection to a client
		clientSocket, addr = serverSocket.accept()

		# obtain the request through the wire
		rawRequest = getRequest(clientSocket)

		# dictionary to hold the server's response
		responseDict = {
			"version" : "HTTP/1.1",
			"content-type" : "text/html"
		}

		try :

			# dictionary to hold client's request
			requestDict = parseRequest(rawRequest)

			try :

				# extract the contents of the file
				fileName = requestDict["url"]
				fileType = getFileType(fileName)
				if fileType == "jpeg" or fileType == "jpg" :
					responseDict["content"] = openBinaryFile(fileName)
					responseDict["content-type"] = "image/" + fileType
				else :
					responseDict["content"] = openTextFile(fileName)
					responseDict["content-type"] = "text/" + fileType
				# exception thrown if unsuccessful
				print(codeDict[200])
				responseDict["code"] = codeDict[200]
				# obtain the time last modified
				responseDict["modified"] = getModifiedTimeString(requestDict["url"])

			except NotFoundException :
				# file not found
				print(codeDict[404])
				responseDict["content"] = responseDict["code"] = codeDict[404]

			except FileTypeNotSupportedException :
				# file not found
				print(codeDict[415])
				responseDict["content"] = responseDict["code"] = codeDict[415]

		except NonGetRequestException :
			# not a GET request
			print(codeDict[405])
			responseDict["content"] = responseDict["code"] = codeDict[405]

		except BadRequestException :
			# invalid syntax or nonsense request
			print(codeDict[400])
			responseDict["content"] = responseDict["code"] = codeDict[400]

		except HTTPVersionNotSupportedException :
			# unsupported version of HTTP
			print(codeDict[505])
			responseDict["content"] = responseDict["code"] = codeDict[505]

		except CoffeePotException :
			# BREW request
			print(codeDict[418])
			responseDict["content"] = responseDict["code"] = codeDict[418]

		# add the headers to the response
		rawResponse = getResponse(responseDict)

		# send the response over the wire
		returnResponse(rawResponse, clientSocket)

		#close the connection
		clientSocket.close()

# ----
# main
# ----

print("------------")
print(serverName + "/" + serverVersion)
print("------------")

# define port number and socket
port = getPort()
serverSocket = socket(AF_INET, SOCK_STREAM)

# activate socket
serverSocket.bind(('localhost', port))
serverSocket.listen(1)

listen()

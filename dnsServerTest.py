import socket
import sys
import binascii
from colorama import Fore, Back, Style

def parseOutQueryAddress(data):
	octetLenIndex = 24
	octetIndex = octetLenIndex + 2
	requestData = ""
	for i in range(0, 3):
		octetLen = int( data[octetLenIndex : octetLenIndex + 2], 16)
		octet = data[octetIndex : octetIndex + (octetLen * 2)]
		requestData += str(octet.decode("hex")) + "."

		octetLenIndex = octetLenIndex + (octetLen * 2) + 2
		octetIndex = octetIndex + (octetLen * 2) + 2
	return requestData

def startServer():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverAddr = '127.0.0.1'
	serverPort = 53
	print (("starting server at {address}:{port}").format(address=serverAddr, port=serverPort))
	print ("Waiting for requests....")
	sock.bind((serverAddr, serverPort))

	while True:
		data, address = sock.recvfrom(4096)
		print ("Recieved {bytes} from {address}".format(bytes=len(data), address=address))
		sent = sock.sendto(data, address)
		print ("Echoed request back to {address}".format(address=address))

		packetHex = binascii.b2a_hex(data)
		parsedData = parseOutQueryAddress(packetHex)

		print("	Requested Data: " + Style.BRIGHT + Fore.CYAN + parsedData)
		print(Style.RESET_ALL)

startServer()
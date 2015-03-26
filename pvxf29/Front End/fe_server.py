#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import pickle
import sys
from threading import *
import urllib.request
import json

#Contains array of valid ports for frontend server
fePortDb = pickle.load( open('fe_port_db.p','rb'))

#Contains array of servers
serverList = pickle.load( open('active_server_db.p','rb'))

#Creates a Frontend Server
def start_fe_server():
	#Create welcome sockets for clients at available valid ports
	serverSocket = socket(AF_INET, SOCK_STREAM)
	for i in range(len(fePortDb)):
		try:
			serverSocket.bind(('',fePortDb[i][1]))
			welcomePort = fePortDb[i][1]
			break
		except:
			print('> Failed')
			continue
	#Create welcome port listening for client/server as new thread
	Thread(None,listen_for_connection,None,tuple([serverSocket, welcomePort]),None).start()

#Listen for clients from open port
def listen_for_connection(serverSocket, welcomePort):
	while(1):
	    #Setup weclome port
	    print ('\nFrontend server is ready to receive client at port: '+str(welcomePort))
	    print ('Listening...')
	    serverSocket.listen(1) #Waits for client
	    connectionSocket, address = serverSocket.accept() #Client accepts
	    #Add to server list
	    print ('\nConnection established...')
	    #Starts thread so can accept new client
	    command = connectionSocket.recv(1024).decode('utf-8') #Received message form client
	    print ('> Command received -> ' + command)
	    Thread(None,methodList[command[:6]],None,tuple([connectionSocket, address, command[7:]]),None).start()
	    continue

#Adds/removes a server to list of active servers
def modify_server_list(serverSocket, address, request):
	serverList = pickle.load( open('active_server_db.p','rb'))
	print ('\nRequest -> ' + str(request))
	actualPort = request[4:]
	#Do requested edit
	if (request[:3] == 'ADD'): #Add server to valid list
		print ('Adding: ' + str(address[0]) + ', ' + str(actualPort))
		serverList.append([address[0],str(actualPort)]) #Add server
	elif (request[:3] == 'DEL'): #Remove server from valid list
		print ('Deleting: ' + str(address[0]) + ', ' + str(actualPort))
		serverList.remove([address[0],str(actualPort)]) #Remove/close server
		print ('Server list: ' + str(serverList))
		pickle.dump(serverList, open( "active_server_db.p", "wb" ))
		return
	else:
		serverSocket.send(('ERR').encode())
		serverSocket.close()
		return
	print ('Server list: ' + str(serverList))
	pickle.dump(serverList, open( "active_server_db.p", "wb" ))
	serverSocket.send(('YES').encode())
	serverSocket.close()
	return

#Waits for a request from client, to pass to replicas
def pass_client_input(clientSocket, address, clientRequest):
	#Sends response from all successfully queried dbs
	clientSocket.send(try_primary_server(clientRequest.encode('utf-8'), address)) #Try replicas and send responses to client
	clientSocket.close() #Closes connection with client
	return

#Connects to replica servers and sends client request
def try_primary_server(clientRequest, address):
	print ('Trying client request...')
    #Array of replica server responses (from all in turn)
	serverResponse = []
	while(1):
		#Find primary server
		serverList = pickle.load( open('active_server_db.p','rb'))
		print (str(serverList))
		try:
			primaryServer = serverList[0]
			print (str(primaryServer))
		except:
			return ('ERR').encode('utf-8') #No more valid primary servers
		
		primarySocket = create_socket(primaryServer[0],primaryServer[1])
		#try:
		print ('Sending command ->' + str(clientRequest))
		primarySocket.send(clientRequest)
		return (process_primary_response(primarySocket,primaryServer[0],primaryServer[1])).encode('utf-8')
		# except:
		# 	print('> Error: Failed to send request.\n')
		# 	continue
		# except:
		# 	print ('> Attempt failed: Port not open.\n> Removing server...')
		# 	modify_server_list(primarySocket, primaryServer, ('DEL_' + str(primaryServer[1]))) #Remove server as unavailable
		# 	print ('> Server removed.')
		# 	continue

#Processes response from server and takes requested further action
def process_primary_response(primarySocket, ip, address):
	print('Processing response...')
	response = (primarySocket.recv(1024)).decode('utf-8')
	print ('response ->' + str(response))
	if response[:3] == 'ERR': # Process completed -> Failed
		return response
	elif response[:3] == 'SER': #Server list requested
		print ('> Server list requested')
		serverList = pickle.load( open('active_server_db.p','rb'))
		#Reestablish connection
		primarySocket = create_socket(ip,address)
		newServerList = []
		for i in range(len(serverList)):
			newServerList.append(str(serverList[i][0] + '>' + serverList[i][1]))
		primarySocket.send(('_'.join(newServerList)).encode('utf-8'))
		return (primarySocket.recv(1024)).decode('utf-8')
	else:
		return response

#Create socket
def create_socket(ip, port):
    print ('Connecting to Server: '+ str(ip)+', Port: '+ str(port))
    primarySocket = socket(AF_INET, SOCK_STREAM)
    try:
	    primarySocket.connect((ip, int(port)))
	    return primarySocket
    except:
        print ('Error: Failed to connect at ' + str(ip)+', ' + str(port) + '\n')
        return None

start_fe_server()

methodList = {"SERVER": modify_server_list, "CLIENT": pass_client_input }
#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import pickle
import sys
from threading import *

#Contains array of valid ports for frontend server
fePortDb = pickle.load( open('fe_port_db.p','rb'))
#Contains array of valid ports to find replica servers at
replicaPortDb = pickle.load( open('replica_port_db.p','rb'))

#Creates a Front End Server
def start_fe_server():
	#Create welcomePorts for clients at all available ports
	serverSocket = socket(AF_INET, SOCK_STREAM)
	for i in range(len(fePortDb)):
		try:
			serverSocket.bind(('',fePortDb[i][1]))
			welcomePort = fePortDb[i][1]
			break
		except:
			continue
	#Create welcome port listening for client as new thread
	Thread(None,listen_for_client,None,tuple([serverSocket, welcomePort]),None).start()

#Listen for clients from open port
def listen_for_client(serverSocket, welcomePort):
	while(1):
	    #Setup weclome port
	    print ('The frontend server is ready to receive at port: '+str(welcomePort))
	    serverSocket.listen(1) #Waits for client
	    connectionSocket, addr = serverSocket.accept() #Client accepts
	    print ('Client established...')
	    #Starts thread so can accept new client
	    Thread(None,take_input,None,tuple([connectionSocket]),None).start()
	    continue

#Waits for a command from client
def take_input(connectionSocket):
	command = (connectionSocket.recv(1024)).decode('utf-8')
	print ('Command received > ' + command)
	#Sends response from all successfully queried dbs
	socket.send((try_replica_server(command)).encode())
	connectionSocket.close() #Closes socket with client
	return

#Tries to connect to replica servers
def try_replica_server(data):
    #Array of replica server responses (from all in turn)
	serverResponse = []

    #Try and find replica servers from list of valid ports
	for i in range(len(replicaPortDb)):
		serverPort = replicaPortDb[i]
		try:
			clientSocket = create_socket(serverPort[0],serverPort[1])
            #If port creation failed (no server at port)
			if clientSocket==None:
				print ('Port not open.')
			else: #if port exists
				try:
					clientSocket.send(data)
					print ('Sent: ' + data)
				except:
					print('\nError 1.\n')
					continue
				serverResponse.append((clientSocket.recv(1024)).decode('utf-8'))
		except:
			print ('Failed to connect to server at port ' + str(serverPort))
			continue
	return ('>'.join(serverResponse)) #String formatting needs handling correctly

#Create socket
def create_socket(name,port):
    print ('Connecting to Server: '+ str(name)+', Port: '+ str(port))
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((name,port))
        return clientSocket
    except:
        print ('Failed to make socket')
        return None

#Web Queries
#if all responses were errors (i.e. no movie info currently)
#Push data to replica servers
#try_replica_server(str('ADD' + name + '_' + url + '_' + info).encode())

start_fe_server()
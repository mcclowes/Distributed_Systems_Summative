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
#Contains array of valid ports to find replica servers at
replicaPortDb = pickle.load( open('replica_port_db.p','rb'))

#Creates a Front End Server
def start_fe_server():
	#Create welcome sockets for clients at available valid ports
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
	    print ('Frontend server is ready to receive at port: '+str(welcomePort))
	    serverSocket.listen(1) #Waits for client
	    connectionSocket, addr = serverSocket.accept() #Client accepts
	    print ('Client established...')
	    #Starts thread so can accept new client
	    Thread(None,take_input,None,tuple([connectionSocket]),None).start()
	    continue

#Waits for a command from client, to pass to replicas
def take_input(connectionSocket):
	command = connectionSocket.recv(1024) #Received message form client
	print ('> Command received -> ' + command.decode('utf-8'))
	#Sends response from all successfully queried dbs
	connectionSocket.send(try_replica_server(command)) #Try replicas and send responses to client
	connectionSocket.close() #Closes socket with client
	return

#Connects to replica servers and sends client command
def try_replica_server(data):
	print ('Trying client request...')
    #Array of replica server responses (from all in turn)
	serverResponse = []

    #Try and find replica servers from list of valid ports
	for i in range(len(replicaPortDb)):
		serverPort = replicaPortDb[i]
		feSocket = create_socket(serverPort[0],serverPort[1])
        #If port creation failed (no server at port)
		if feSocket==None:
			print ('> Attempt failed: Port not open.\n')
			continue
		else: #If replica server found
			print ('Socket established...')
			try:
				#print ('Sending command ->' + data)
				feSocket.send(data)
			except:
				print('> Error: Failed to send request.\n')
				continue
			#Add replica response to list of responses
			serverResponse.append((feSocket.recv(1024)).decode('utf-8'))
			print ('All responses -> ' + str(serverResponse))

	#Send all responses to client
	print (str(data.decode('utf-8')))
	print ('Len: ' + str(len(serverResponse)))
	print (str(serverResponse))
	if (data.decode('utf-8')[:3]=='GET'): #Was movie info requested?
		print ('Request was ' + str(data.decode('utf-8')[:3]))
		#Check if any responses are valid
		for item in serverResponse:
			if (item != 'ERR') or (item != 'YES'): #>1 valid response, so return
				break
		#Otherwise, no valid movie info returned
		print ('> No movie information found\nQuerying OMDb...')
		serverResponse.append(query_omdb(data.decode('utf-8')[4:]))

	print ('Sending ->' + str('>'.join(serverResponse)))
	return ('>'.join(serverResponse).encode('utf-8')) #String formatting needs handling correctly

#Create socket
def create_socket(name,port):
    print ('Connecting to Server: '+ str(name)+', Port: '+ str(port))
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((name,port))
        return clientSocket
    except:
        print ('Error: Failed to make socket at ' + str(port) + '\n')
        return None

#If all responses were errors (i.e. no movie info currently), retrieve
def query_omdb(name):
	name = name.replace(' ', '+').lower()
	omdbURL = str('http://www.omdbapi.com/?s=' + name + '&r=json')
	movieInfo = json.loads(urllib.request.urlopen(omdbURL).read().decode('utf-8'))
	try:
		return ((movieInfo['Search'][0]['Title']) + "_http://www.imdb.com/title/" + (movieInfo['Search'][0]['imdbID']) + "_" + (movieInfo['Search'][0]['Title']) + ' was released in ' + (movieInfo['Search'][0]['Year']))
	except:
		print ('> No movie information found online')
		return ('ERR')
# Propagate web query results to replicas

start_fe_server()
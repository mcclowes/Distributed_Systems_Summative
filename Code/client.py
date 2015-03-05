#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import sys
import pickle
from client_methods import *

feServerDb = pickle.load( open('fe_server_db.p','rb'))

#Print list of commands
def help():
    print ('\nCommand List:')
    print ('help: Prints this list\n')
    print ('Movie requests:')
    print ('get: Get information about a movie')
    print ('edit: Edit information about a movie')
    print ('add: Add a movie to the database')
    print ('all: Get list of all movies in database\n')
    print ('Server maintainance:')
    print ('addserver: Add a server to the list')
    print ('deleteserver: Delete a server from the list')
    print ('serverlist: Prints list of servers')

#Start client
def start_client():
    print('\nWelcome')
    while (1):
    	#Waits for user input
    	userInput = (input('\nWhat would you like to do?\n')).lower()
    	methodList[userInput]()
        # try:
        #     userInput = (input('\nWhat would you like to do?\n')).lower()
        #     methodList[userInput]()
        # except:
        #     print ('\nCommand not recognised.\n')
        #     help()
        #     continue

#Tries to connect to frontend server, called in information request methods
def try_server(data):
    #Array of front end servers
    serverResponse = []
      
    #Try and find frontend server from list of valid ports
    for i in range(len(feServerDb)): #Tries all valid frontends (Extra functionality)
        serverPort = feServerDb[i]
        try:
            clientSocket = create_socket(serverPort[0],serverPort[1])
            #If port creation failed (no server at port)
            if clientSocket==None:
                print ('Port not open.')
            else: #If port exists and server waiting
                try:
                    clientSocket.send(data)
                except:
                    print('\nError 1.\n')
                    continue
                serverResponse.append((clientSocket.recv(1024)).decode('utf-8'))
        except:
            continue
    return serverResponse

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

#Converts user input to method call
methodList = {"get":get_movie_info, "edit":edit_movie_info, "add":add_movie_info,\
              "all":get_movies,\
              "addserver":add_server, "deleteserver":delete_server, "serverlist":print_servers}

start_client()

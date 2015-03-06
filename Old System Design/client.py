#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import sys
import pickle

feServerDb = pickle.load( open('fe_server_db.p','rb'))

#Print list of valid user commands
def command_help():
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

#Client waits for user input
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
    feResponse = []
      
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
                feResponse.extend(((clientSocket.recv(1024)).decode('utf-8')).split('>'))
        except:
            continue
    return feResponse

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

#Retrieve information about a movie
def get_movie_info():
    name = input('\nRequested movie name:\n')
    name = (name.lower()).capitalize()
    data = ("GET_"+name).encode()
    movieData = try_server(data)
    for item in movieData:
        if item=='ERR':
            print ('\nThat movie was not found in the database\n')
        else:
            movieName, movieUrl, movieDesc = item.split('_')
            print ('\nName: {}\nURL: {}\nDescription: {}\n'.format(movieName, movieUrl, movieDesc))

#Edit a movie's saved information
def edit_movie_info():
    movieName = ((input('\nName:\n')).lower()).capitalize()
    movieUrl = (input('\nURL:\n')).lower()
    movieDesc = ((input('\nDescription:\n')).lower()).capitalize()
    data = ('_'.join('EDI', movieName, movieUrl, movieDesc)).encode()
    movieData = (try_server(data)).split('_')
    for item in movieData:
        if item=='ERR':
            print ('\nThat movie was not found in the database\n')
        else:
            print ('\nMovie entry updated.\n')

#Add a new movie
def add_movie_info():
    movieName = ((input('\nName:\n')).lower()).capitalize()
    movieUrl = (input('\nURL:\n')).lower()
    movieDesc = ((input('\nDescription:\n')).lower()).capitalize()
    data = ('_'.join('ADD', movieName, movieUrl, movieDesc)).encode()
    movieData = try_server(data)
    for item in movieData:
        if item=='ERR':
            print ('\nThat movie already exists in the database\n')
        else:
            print ('\nMovie entry added.\n')

#Gets a list of all movies
def get_movies():
    data = ('ALL').encode()
    movieData = try_server(data)
    for item in movieData:
        print (item)

#Adds a server to the list of servers a client will query
def add_server():
    print('\nAdding a server.')
    serverIP = input('IP:\n')
    serverPort = input('Port:\n')
    feServerDb.append([serverIP,serverPort])
    pickle.dump(feServerDb, open( "feServerDb.p", "wb" ) )
    print ('Server added.\n')

#Delete a server from a list
def delete_server():
    print_servers()
    try:
        #print ('a')
        del feServerDb[int(input('Select server to delete:'))]
        #print ('b')
        pickle.dump(feServerDb, open( "feServerDb.p", "wb" ) )
        print ('Server deleted.\n')
        feServerDb = pickle.load( open('feServerDb.p','rb'))
    except:
        print('\nInvalid choice of server.\n')
        delete_server()

#Prints a list of all servers       
def print_servers():
    print ('\nServer list:')
    for i in range(len(feServerDb)):
        print ('Server '+str(i)+') IP: '+str(feServerDb[i][0]) + ', Port: ' + str(feServerDb[i][1]))


#Converts user input to method call
methodList = {"get":get_movie_info, "edit":edit_movie_info, "add":add_movie_info, "all":get_movies,\
              "addserver":add_server, "deleteserver":delete_server, "serverlist":print_servers,\
              "help":command_help}

start_client()

#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import pickle
import sys
from threading import *
import urllib.request
import json

#Contains array of valid ports for server
serverdb = pickle.load( open('be_server_db.p','rb'))

#Contains array of valid ports for frontend server
feServerDb = pickle.load( open('fe_server_db.p','rb'))

#Creates a server
def start_server():
      #Find port
      serverSocket = socket(AF_INET, SOCK_STREAM)
      for i in range(len(serverdb)): #Tries to find valid port
            try:
                  serverSocket.bind(('',serverdb[i][1]))
                  welcomePort = serverdb[i][1]
                  print ('Server active at ' + str(welcomePort))
                  break
            except:
                  continue

      #Ping frontend
      for i in range(len(feServerDb)): #Tries all valid frontends (Extra functionality)
            feServerPort = feServerDb[i]
            print ('\n> Trying ' + str(feServerPort[0]) + ', ' + str(feServerPort[1]))
            feSocket = create_socket(feServerPort[0],feServerPort[1])
            #If port creation failed (no server at port)
            if feSocket == None:
                  print ('Port not open.')
            else: #If port exists and server waiting
                  #try:
                  feSocket.send(('SERVER_ADD_'+ str(welcomePort)).encode())

                  if (feSocket.recv(1024)).decode('utf-8') == 'YES':
                        print ('> Server accepted by frontend')
                  else:
                        print ('Huh')
                  #Await contact
                  while(1):
                        print ('\nThe server is ready to receive at port: '+str(welcomePort))
                        serverSocket.listen(1) #Waits for frontend request
                        feSocket, address = serverSocket.accept() #Front end connects
                        print ('Frontend connected...')
                        #Starts thread so can accept new connection from frontend
                        client_request(feSocket, serverdb[i], serverSocket)
                        continue
                  # except:
                  #       print('> Failed to add server.')
                  #       continue
            # except:
            #       print('> Failed at this address')
      #close server
      print('> No frontend server found.\nClosing server...')
      return

#Waits for a command from client via frontend
def client_request(feSocket, currentSocket, welcomeSocket):
      clientRequest = (feSocket.recv(1024)).decode('utf-8')
      print ('> Command received -> ' + clientRequest +'.')
      methodList[clientRequest[:3]](clientRequest[4:], feSocket, currentSocket, welcomeSocket)
      feSocket.close()
      return

#Looks up and sends requested movie information from database to client
def send_movie_info(name, feSocket, currentSocket, welcomeSocket):
      print('Looking up ' + name + '...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  movieInfo = moviedb[i]
                  print ('Sending ->' + str(movieInfo))
                  movieInfo = validate_entry(movieInfo, feSocket) #Validate information
                  feSocket.send(('_'.join(movieInfo)).encode('utf-8'))
                  return
      print ('> Error: Requested movie not found.')
      feSocket.send('_'.join(query_omdb(name)).encode('utf-8')) #Returns either ERR or movie info
      return

#Adds a movie and associated information to the database file
def add_movie_info(data, feSocket, currentSocket, welcomeSocket):
      data = data.split('_')
      name = data[0]
      print('Looking up ' + name+ '...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  print ('> Error: Movie to add exists already')
                  feSocket.send(('ERR').encode())
                  edit_movie_info(data, feSocket)
                  return
      moviedb.append(data)
      pickle.dump(moviedb, open( "movie_db.p", "wb" ) )
      propagate_movie_information(data, feSocket, currentSocket, welcomeSocket)
      feSocket.send(('YES').encode())
      return

#Edits URL and description of selected movie (if movie exists already)
def edit_movie_info(data,feSocket, currentSocket, welcomeSocket):
      data = data.split('_')
      name = data[0]
      print('Looking up ' + name + '...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  moviedb[i][1]=data[1]
                  moviedb[i][2]=data[2]
                  moviedb.append(data)
                  pickle.dump(moviedb, open( "movie_db.p", "wb" ) )
                  propagate_movie_information(data, feSocket, currentSocket)
                  feSocket.send(('YES').encode())
                  return
      #If movie doesn't exist already, add it
      print ('> Error: Requested movie not found.\nAdding movie')
      add_movie_info(data, feSocket)
      return

#Sends a list of all movie names in the database
def send_database(data,feSocket, currentSocket, welcomeSocket):
      print ('Sending database...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      movieInfo = []
      for i in range(len(moviedb)):
            movieInfo.append(moviedb[i][0])
      feSocket.send(('_'.join(movieInfo)).encode())
      return

#If all responses were errors (i.e. no movie info currently), retrieve
def query_omdb(name):
      name = name.replace(' ', '+').lower()
      omdbURL = str('http://www.omdbapi.com/?s=' + name + '&r=json')
      movieInfo = json.loads(urllib.request.urlopen(omdbURL).read().decode('utf-8'))
      try:
            return [(movieInfo['Search'][0]['Title']), ("http://www.imdb.com/title/" + \
                  (movieInfo['Search'][0]['imdbID'])), str((movieInfo['Search'][0]['Title']) + \
                  ' was released in ' + (movieInfo['Search'][0]['Year']))]
      except:
            print ('> No movie information found online')
            return ('ERR')

# Ensures that all fields are valid (protects against data loss)
def validate_entry(movieInfo, feSocket):
      imdbEntry = []
      for i in range(len(movieInfo)):
            if len(movieInfo[i]) == 0: # If any field is empty
                  if imdbEntry == []:
                        imdbEntry = query_omdb(movieInfo[0])
                  movieInfo[i] = imdbEntry[i]
      return movieInfo

# Propagate web query results to replicas
def propagate_movie_information(data, feSocket, currentSocket, welcomeSocket):
      print ('Propagating information...')
      serverList = get_server_list(feSocket, currentSocket, welcomeSocket)
      print (str(serverList[0]) + ' vs ' + str(currentSocket))
      if (serverList[0][1] == str(currentSocket[1])):
            for i in range(1,len(serverList)):
                  print ('here2')
                  if (serverList[i][1] != str(currentSocket[1])):
                        #try:
                        print('here3')
                        server = serverList[i]
                        serverSocket = create_socket(server[0],server[1])
                        print ('Updating movie info')
                        serverSocket.send(str('ADD_'+data).encode())
                        connectionSocket.recv(1024).decode('utf-8')
                        #except:
                              #continue

#Retrun the list of servers
def get_server_list(feSocket, currentSocket, welcomeSocket):
      print ('Getting server list...')
      feSocket.send(('SER').encode())
      print ('SER sent...')
      welcomeSocket.listen(1) #Waits for frontend response
      feSocket, address = welcomeSocket.accept()
      print (str(address[0]) + ', ' + str(address[1]))
      serverList = (feSocket.recv(1024)).decode('utf-8').split('_')
      finalServerList = []
      for i in range(len(serverList)):
            finalServerList.append(serverList[i].split('>'))
      print (str(finalServerList))
      return  finalServerList #Return server list

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

methodList = {"GET":send_movie_info, "EDI":edit_movie_info, "ADD":add_movie_info,\
              "ALL":send_database}

start_server()
#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import pickle
import sys
from threading import *

#Contains array of valid ports for replica server
serverdb = pickle.load( open('replica_port_db.p','rb'))

#Creates a server
def start_server():
      serverSocket = socket(AF_INET, SOCK_STREAM)
      for i in range(len(serverdb)): #Tries to find valid port
            try:
                  serverSocket.bind(('',serverdb[i][1]))
                  welcomePort = serverdb[i][1]
                  break
            except:
                  continue
      while(1):
            #Setup weclome socket
            print ('The server is ready to receive at port: '+str(welcomePort))
            serverSocket.listen(1) #Waits for client
            connectionSocket, addr = serverSocket.accept() #Client accepts
            print ('Client established...')
            #Starts thread so can accept new connection from frontend
            Thread(None,take_input,None,tuple([connectionSocket]),None).start()
            continue

#Waits for a command from client via frontend
def take_input(connectionSocket):
      command = (connectionSocket.recv(1024)).decode('utf-8')
      print ('> Command received -> ' + command +'.')
      methodList[command[:3]](command[4:],connectionSocket)
      connectionSocket.close()
      return
      # try:
      #       command = (connectionSocket.recv(1024)).decode('utf-8')
      #       print ('> Command received -> ' + command +'.')
      #       methodList[command[:3]](command[4:],connectionSocket)
      #       connectionSocket.close()
      #       return
      # except:
      #       print ('> Error: Invalid command/format.')
      #       connectionSocket.send(('ERR').encode())
      #       connectionSocket.close()
      #       return

#Looks up and sends requested movie information from database to client
def send_movie_info(name, socket):
      print('Looking up ' + name + '...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  movieInfo = moviedb[i]
                  print ('Sending ->' + str(movieInfo))
                  socket.send(('_'.join(movieInfo)).encode('utf-8'))
                  return
      print ('> Error: Requested movie not found.')
      socket.send(('ERR').encode())
      return

#Adds a movie and associated information to the database file
def add_movie_info(data, socket):
      data = data.split('_')
      name = data[0]
      print('Looking up ' + name+ '...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  print ('> Error: Movie to add exists already')
                  socket.send(('ERR').encode())
                  return
      moviedb.append(data)
      pickle.dump(moviedb, open( "movie_db.p", "wb" ) )
      socket.send(('YES').encode())
      return

#Edits URL and description of selected movie (if movie exists already)
def edit_movie_info(data,socket):
      data = data.split('_')
      name = data[0]
      print('Looking up ' + name + '...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  moviedb[i][1]=data[1]
                  moviedb[i][2]=data[2]
                  edb.append(data)
                  pickle.dump(moviedb, open( "movie_db.p", "wb" ) )
                  socket.send(('YES').encode())
                  return
      #If movie doesn't exist already, add it
      print ('> Error: Requested movie not found.\nAdding movie')
      add_movie_info(data, socket)
      return

#Sends a list of all movie names in the database
def send_database(data,socket):
      print ('Sending database...')
      moviedb = pickle.load( open('movie_db.p','rb'))
      movieInfo = []
      for i in range(len(moviedb)):
            movieInfo.append(moviedb[i][0])
      socket.send(('_'.join(movieInfo)).encode())
      return

methodList = {"GET":send_movie_info, "EDI":edit_movie_info, "ADD":add_movie_info,\
              "ALL":send_database}

start_server()

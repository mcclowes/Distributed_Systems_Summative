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
      for i in range(len(serverdb)):
            try:
                  serverSocket.bind(('',serverdb[i][1]))
                  welcomePort = serverdb[i][1]
                  break
            except:
                  continue
      while(1):
            #Setup weclome port
            print ('The server is ready to receive at port: '+str(welcomePort))
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
      methodList[command[:3]](command[4:],connectionSocket)
      connectionSocket.close()
      return

methodList = {"GET":send_movie_info, "EDI":edit_movie_info, "ADD":add_movie_info,\
              "ALL":send_database}

start_server()

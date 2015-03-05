#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import pickle
import sys
from threading import *

#Looks up and sends requested movie information from database to client
def send_movie_info(name, socket):
      print('Looking up '+name+'...')
      moviedb = pickle.load( open('moviedb.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  movieInfo = moviedb[i]
                  socket.send(('_'.join(movieInfo)).encode())
                  return
      socket.send(('ERR').encode())

#Adds a movie and associated information to the database file
def add_movie_info(data, socket):
      data = data.split('_')
      name = data[0]
      print('Looking up '+name+'...')
      moviedb = pickle.load( open('moviedb.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  print ('Movie exists already')
                  socket.send(('ERR').encode())
                  return
      moviedb.append(data)
      pickle.dump(moviedb, open( "moviedb.p", "wb" ) )
      socket.send(('YES').encode())

#Edits URL and description of selected movie (if movie exists already)
def edit_movie_info(data,socket):
      data = data.split('_')
      name = data[0]
      print('Looking up '+name)
      moviedb = pickle.load( open('moviedb.p','rb'))
      for i in range(len(moviedb)):
            if moviedb[i][0]==name:
                  moviedb[i][1]=data[1]
                  moviedb[i][2]=data[2]
                  edb.append(data)
                  pickle.dump(moviedb, open( "moviedb.p", "wb" ) )
                  socket.send(('YES').encode())
                  return
      socket.send(('ERR').encode())
      movi

#Sends a list of all movie names in the database
def send_database(data,socket):
      moviedb = pickle.load( open('moviedb.p','rb'))
      movieInfo = []
      for i in range(len(moviedb)):
            movieInfo.append(moviedb[i][0])
      socket.send(('_'.join(movieInfo)).encode())
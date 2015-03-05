#Maxi Clayton Clowes
#03/2015
#Python 3.4.2

from socket import *
import sys
import pickle

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
def add_server(feServerDb):
    print('\nAdding a server.')
    serverIP = input('IP:\n')
    serverPort = input('Port:\n')
    feServerDb.append([serverIP,serverPort])
    pickle.dump(feServerDb, open( "feServerDb.p", "wb" ) )
    print ('Server added.\n')

#Delete a server from a list
def delete_server(feServerDb):
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
def print_servers(feServerDb):
    print ('\nServer list:')
    for i in range(len(feServerDb)):
        print ('Server '+str(i)+') IP: '+str(feServerDb[i][0]) + ', Port: ' + str(feServerDb[i][1]))

# distributed-system-experiment
=========================

    TCP Server/Client Networking program in Python

##Using the code
_**Note:** Code is in Python version 3.4.2_
The code consists of three Python files, Client.py, FrontEnd.py and Replica.py. Each client must be run from a directory containing a server database (serverdb.p), which keeps a list of all servers that the client will attempt to query. Each server must be run from a directory containing a movie database (moviedb.p) and database of valid ports (portdb.p), which stores a list of permitted welcome ports that a server can use. These databases are implemented in the pickle Python module, which I opted for rather than simply including an array in the server file as it allows testing with differing database files, as well as saving/maintaining the database.

Upon starting, a client will print a list of commands with descriptions of their functionality. The client functionality is divided into two sections:
    
1. Movie requests:
    - Get movie information – “get” 
    - Edit movie information – “edit” 
    - Add movie to database – “add” 
    - Get list of all movies – “all”
2. Server maintenance:
    - Add new server to list – “addserver”
    - Delete server from list – “deleteserver”
    - Print list of all servers client currently accesses – “serverlist”

##The system

import pickle

# Save a dictionary into a pickle file.
#moviedb is a database of ports
moviedb = [['Moneyball', 'www.moneyball.com', 'Not a movie about the lottery, surprisingly'],\
           ['Casino', 'www.casino.com', 'Bit of a gamble really'],\
           ['Avatar','www.avatar.com','Smurfs + Pocahantas'],\
           ['The Hobbit','www.thehobbit.com','Dragons and dwarves'],\
           ['Rush','www.rush.co.uk','Fast cars, fast lives'],\
           ['Taken','www.taken.org','Are you Taken the piss'],\
           ['Spirited Away','www.spiritedaway.jp','That music'],\
           ['Bridge over the River Kawaiiii','www.bridge.com','A documentary about bridge making'],\
           ['Benjamin Button','www.bb.com','A film charting Brad Pitts plastic surgery'],\
           ['Noddy','www.noddy.com','Racist'],\
           ['Lock Stock and Two Smoking Barrels','www.lsatsb.com','Guv'],\
           ['Drive','www.drivefast.com','Maurice Drive has gotta go fast!'],\
           ['The Room','www.tommywiseau.com','Oh hai Mark'],\
           ['Month Python and the Holy Grail','www.monty.co.uk','Python']]
pickle.dump( moviedb, open( "movie_db.p", "wb" ) )

#Generate database of 
fe_server_db = [['localhost',11000],['localhost',11001],['localhost',11002]]
pickle.dump( fe_server_db, open( "fe_server_db.p", "wb" ) )

fe_port_db = [['localhost',11000],['localhost',11001],['localhost',11002]]
pickle.dump( fe_port_db, open( "fe_port_db.p", "wb" ) )

replica_port_db = [['localhost',12000],['localhost',12001],['localhost',12002],['localhost',12003],['localhost',12004]]
pickle.dump( replica_port_db, open( "replica_port_db.p", "wb" ) )

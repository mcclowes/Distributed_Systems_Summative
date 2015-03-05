import urllib.request
import json

movieInfo = json.loads(urllib.request.urlopen('http://www.omdbapi.com/?s=saw&r=json').read().decode('utf-8'))
print ((movieInfo['Search'][0]['Title']) + "_http://www.imdb.com/title/" + (movieInfo['Search'][0]['imdbID']) + "_" + (movieInfo['Search'][0]['Title']) + ' was released in ' + (movieInfo['Search'][0]['Year']))

movieInfo = json.loads(urllib.request.urlopen('http://www.omdbapi.com/?s=avatar&r=json').read().decode('utf-8'))
print ((movieInfo['Search'][0]['Title']) + "_http://www.imdb.com/title/" + (movieInfo['Search'][0]['imdbID']) + "_" + (movieInfo['Search'][0]['Title']) + ' was released in ' + (movieInfo['Search'][0]['Year']))
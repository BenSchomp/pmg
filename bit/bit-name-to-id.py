import requests
import json

import urllib.parse

base_url = 'https://rest.bandsintown.com/artists/'
app_id = 'a57827444d1abbf1271c242612782d91'

file = open( 'artist-names.txt' )
for line in file:
  line = line.strip()
  artist_name = urllib.parse.quote( line )
  url = base_url + artist_name + '/?app_id=' + app_id

  response = requests.get( url )
  pretty_json = json.loads(response.text)
  print (json.dumps(pretty_json, indent=2))
  data = response.json()
  print( data['id'] )
  exit()

file.close()


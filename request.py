import requests
import pprint
import os

Artsy_token = os.environ['ARTSY_API_TOKEN'].rstrip()

r = requests.get('https://api.artsy.net/api/artists/edvard-munch', headers={'X-Xapp-Token': Artsy_token})

genes_json = r.json()

print pprint.pprint(genes_json)


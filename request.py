import requests

import pprint

r = requests.get('https://api.artsy.net/api/artists/edvard-munch', headers={'X-Xapp-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6IiIsImV4cCI6MTQ5OTEwNDQzMCwiaWF0IjoxNDk4NDk5NjMwLCJhdWQiOiI1OTMwNjYxYWNkNTMwZTA3MWMzOWQzMWQiLCJpc3MiOiJHcmF2aXR5IiwianRpIjoiNTk1MTRhMmVjZDUzMGU0ZDU3MzJmMmI5In0.2xsxW8d3xUrpVcXyS6v3LnH5cJRwsE7zt_2lFEgfyCs'})

genes_json = r.json()

print pprint.pprint(genes_json)

print genes_json['_embedded']['artworks'][0]

from yaml import safe_load
from json import loads

with open('deploy.yml','r') as f:
    deploy = safe_load(f)['endpoint']
    
with open('package.json','r') as f:
    package = loads(f.read())
    package['foo'] ='bar'
    
with open('package.json','w') as f:
    f.write(package)
    


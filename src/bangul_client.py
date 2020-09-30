import json
import urllib.request
import urllib.parse
import ssl

context = ssl._create_unverified_context()
url = 'https://13.124.126.131'
port = 443

def giveserver(data) :

    #get형식으로 통신

    uri = url +'/home/trace?' 
    data = urllib.parse.urlencode(data)
    req=urllib.request
    d=req.urlopen(uri + data, context=context)
    result = json.loads(d.read().decode()) #{'object' : 'person', 'number' : 1} 이런식으로 올것    
    return result



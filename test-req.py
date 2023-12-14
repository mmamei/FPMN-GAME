import requests

r = requests.get('http://corriere.it')
r = r.text.split('<a class="has-text-black"')
for x in r[1:]:
    try:
        print('-',x.strip()[x.index('>'):x.index('</a')-1])
    except:
        ...
import requests


def Main(myfile, lang, apikey):
      with open(myfile) as words:
            for i in words:
                  n=0
                  while n < 250:
                  #The free API let you make 500 request per-day, we're gonna use two request per-word
                  
                        #here we clean the string from formatting and white space
                        s = i.lower()
                        s = s.lstrip()
                        s = s.rstrip()
                        s = s.replace(' ','%20')  #%20 is vital to perform a correct call whit simple sentences that have white spaces
                        s = s.replace('\n','')    #Replacing the escape character is important
                        
                        #let's make the first request
                        r = ForvoHttpRequest('word-pronunciations',s,lang,apikey)
                        
                        #now we download the mp3 files from forvo server if r is not-empty
                        if r:
                              #the second request
                              mp3 = requests.get(r)
                              with open(i.replace('\n','')+'.mp3',"wb") as out:
                                    out.write(mp3.content)
                                    out.close()
                        else:
                              with open('pronuonce_not_found.txt',"a") as out:
                                    out.write(s)
                                    out.close()
                        
                        n = n+1
                  
                  
        
def ForvoHttpRequest(act, word, lang, apikey):
      url = 'http://apifree.forvo.com/action/{0}/format/json/word/{1}/language/{2}/order/rate-desc/limit/1/key/{3}'.format(act, word, lang, apikey)

      r = requests.get(url)
      data = r.json()
      print data
      if data:
            path = data[0]
      
            if path:
                  mp3path = path.get('pathmp3',)
            else:
                  mp3path = ''
      else:
            mp3path = ''
            
      return mp3path
            

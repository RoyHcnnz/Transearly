import http.client
import Secrets
import json

class Translator:

    conn = http.client.HTTPSConnection(Secrets.TRANLATOR_HOST)
    headers = {
        'content-type': "application/json",
        'X-RapidAPI-Key': Secrets.TRANLATOR_API_KEY,
        'X-RapidAPI-Host': Secrets.TRANLATOR_HOST
    }

    def __init__(self):
        self.conn.request("GET", "/languages?api-version=3.0", headers=self.headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        self.lang = data["translation"]

    def translate(self, text: str, to = ['en']):
        payload = "[\r{\r\"Text\": \"" + text + "\"\r}\r]"
        toStr = ""
        for i in range(len(to)):
            lang = to[i]
            toStr += "to%5B" + str(i) + "%5D=" + lang + "&"
        body = "/translate?" + toStr + "%3CREQUIRED%3E&api-version=3.0&profanityAction=NoAction&textType=plain"
        
        self.conn.request("POST", 
                          body, 
                          payload.encode(), 
                          self.headers)

        res = self.conn.getresponse()
        data = json.loads(res.read())
        srcLang = data[0]["detectedLanguage"]["language"]
        result = data[0]["translations"]
        return {
            "srcLang": srcLang,
            "result": result
        }

    def getNameOfLangFromCode(self, code: str) -> str:
        return self.lang[code]["name"]
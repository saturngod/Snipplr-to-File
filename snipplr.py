from SnipplrPy import *
import os,json

def get_ext(language):
    
    if(language=="Objective C"):
        return ".m"
    elif(language=="PHP"):
        return ".php"
    elif(language=="Prel"):
        return ".py"
    elif(language=="JavaScript"):
        return ".js"
    elif(language=="Java"):
        return ".java"
    elif(language=="ASP"):
        return ".asp"
    elif(language=="jQuery"):
        return ".js"
    elif(language=="ActionScript"):
        return ".as"
    elif(language=="iPhone"):
        return ".m"
    elif(language=="Windows Registry"):
        return ".reg"
    elif(language=="Bash"):
        return ".sh"
    elif(language=="CSS"):
        return ".css"
    elif(language=="HTML"):
        return ".html"
    elif(language=="Python"):
        return ".py"
    else:
        return ".txt"

snipplr=SnipplrPy()
snipplr.setup("Your API Key")
for snippt in snipplr.list():
    #get file
    #json.dumps(d)
    
        
    result=snipplr.get(snippt['id'])
    if json.dumps(result)!="null":
        file_ext=get_ext(result['language'])

        source=result['source']

        if not os.path.exists("./output"):
            os.makedirs("output")

        write_file=open("output/"+result['title'].replace("/","_")+file_ext,"w")

        write_file.write(source.encode('utf-8').replace("&quot;",'"').replace("&lt;","<").replace("&gt;",">").replace("&amp;","&"))

        write_file.close()
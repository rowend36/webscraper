import re
from roles import roles
from roles import toSqlite
def wrap(t):
    return "("+t+")"
def uwrap(t):
    return "(?:"+t+")"
role="(?:"+"s*|".join(roles)[:-1]+")"
mrole = role+"(?:\s*&\s*(?:"+role+"))?"
word =r"(?:[\w\'\.][\w \.\-\']+|\"[\w\.\'][\w \.,\'\-]+\")"
brackets = "\(.*\)"
winnerlist = "(?:"+word+"(?:\s*\,\s*"+word+")*\s*&\s*"+word+"\ *)"
clause = "(?:"+winnerlist+"|"+word+")\ *(?:"+brackets+")*"
right = "("+clause+"\ *,?\ *"+uwrap(mrole)+"*(?:\s*(?:,|;)\s*"+clause+"\ *,?\ *"+uwrap(mrole)+")*)"

gright = re.compile(wrap(clause)+"\ *,?\ *"+wrap(mrole)+"*"+wrap("(?:\s*(?:,|;)\s*"+clause+"\ *,?\ *"+uwrap(mrole)+")*"))
gclause =  re.compile("(?:"+wrap(winnerlist)+"|"+wrap(word)+")\ *(?:"+wrap(brackets)+")*")
gword = wrap(word)
gwinnerlist = re.compile(gword+"((?:\s*\,\s*"+word+")*)\s*&\s*"+gword+"\ *")

bigword = "(.*)"#"("+word+"\s*(?:"+brackets+")*\ *"+word+"*)"
title_re = re.compile("^\s*\d+\.\s+"+gword+"\ *")
empty_line = r"^[A-Z\W]*\s*$"
result = bigword+" (?:by (.*)|\s*(\(Various Artists\)\s*.*))"
result2 = re.compile(bigword)
winner = re.compile("Winner:\s"+result)
winner2 = re.compile("Winner:\s"+bigword)
trackresult = re.compile("Track from: .*")
array = []
point = 0
rolled = False
def parseClause(text,role):
    results = re.match(gclause,text)
    rlist = results.group(1)
    rword = results.group(2)
    brackets = ""
    if results.group(3):
        brackets = re.sub("^\s*\[\s*|\s*\]\s*$","",results.group(3));
    ret = {}
    if rlist:
        ret["role"] =readList(rlist)
    elif rword:
        ret["role"] =rword
    if brackets:
        ret["by"] = readList(brackets)
        if not ret["by"]:
            ret["by"]=brackets
    else: ret['by']=None
    if(ret['role'] and not re.match(mrole,rlist or rword)):
        ret["role"],ret['by']=ret['by'],ret['role']
    if(role):
        ret["role"]=role
    return ret
def parseWinner(text):
    roles = []
    while True:
        results = re.match(gright,text)
        if not results:
            break
        roles.append(parseClause(results.group(1),results.group(2)))
        text = results.group(3)
        if text:
            text = re.sub("^\s*(,|;)\s*","",text);
        else:
            break
    return roles
def readTitle(text):
    results = re.match(title_re,text)
    if results:
        return results.group(1)
    else: return False
peep = 1
def readResult(text):
    global rolled, peep
    results = re.match(winner,text)
    if results:
        rolled = True
        peep = 1
        return {"result":results.group(1),"by":parseWinner(results.group(2) or results.group(3)),"winner":True}
    results = re.match(winner2,text)
    if results:
        return {"result":results.group(1),"winner":True}
    results = re.match(result,text)
    if results:
        rolled = True
        peep = 1
        return {'result':results.group(1),"by":parseWinner(results.group(2) or results.group(3)),"winner":False}
    results = re.match(trackresult,text)
    if results:
        peep = 0
        return {"result":text,"winner":False}
    results = re.match(result2,text)
    if results:
        if(re.search(role,text)):
            print("")
            if len(array)>0:
                a = array[len(array)-1].get('by')
                if not a:
                    if len(array)>1 and not array[len(array)-2].get('by'):
                        a = array[len(array)-2]['by']=[]
                        a.append({"by":array.pop()['result'],"role":None})
                        
                    else:          
                        a = array[len(array)-1]['by']=[]
                a.extend(parseWinner(results.group(1)))
                #array[len(array)-1]
        else:
            peep = 0
            return {"result":results.group(1),"winner":False}
    return False

def readList(text):
    results = re.match(gwinnerlist,text)
    if results:
        head = results.group(1)
        tail = results.group(3)
        mid = map(lambda s:s.strip(),list(filter(lambda x:x,results.group(2).split(","))))
        return (head,*mid,tail)
    return False
def brackets(line):
    return re.search("\(.*\)",line)
def main():
    global point,array,rolled
    values = {}
    lastKey = ""
    File = open("./2020.txt")
    #File3 = open("./2020.formatted")
    a = File.readline()
    i =  1
    while a:
        comment = ""
        res = False
        # if brackets(a):
        #     print(a)
        a = a.replace("->{",";")
        if re.match(empty_line,a):
            comment="empty"
        else:
            res = readTitle(a)
            if res:
                comment='title: '+res
                lastKey = res
                array = []
                values[lastKey] = array
                point=0
                rolled = False
            else:
                res=readResult(a)
                if res:
                   comment=res
                   array.append(res)
                   point+=1
                else:
                    comment="unknown"
        i+=1
        a = File.readline()
    toSqlite(values)
if __name__ == "__main__":
    main()
#print(parseWinner("Paul Thomas Anderson, video director; Paul Thomas Anderson, Erica Frauman & Sara Murphy, video producers;Paul Thomas Anderson, video director; Paul Thomas Anderson, Erica Frauman & Sara Murphy, video producers'"))
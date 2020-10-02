import re
import pandas as pd

def read_file(): 
    with open("literatur.xml", "r", encoding="utf8") as infile: 
        data = infile.read()
        return data


def get_keywords(data): 
    data = data.split("</Quelle>")
    allkeywords = []
    for item in data: 
        if "<Schlagworte>" in item and "..x.." not in item: 
            keywords = re.findall("<Schlagworte>(.*?)</Schlagworte>", item)[0]
            keywords = keywords.split(" ")
            #print(keywords)
            allkeywords.extend(keywords)
    allkeywords = sorted(list(set(allkeywords)))
    with open("keywords.txt", "w", encoding="utf8") as outfile: 
        outfile.write("\n".join(allkeywords))
    #print(len(allkeywords))
    #print(allkeywords)
    return allkeywords


def convert(data, keywords): 
    data = data.split("</Quelle>")
    converted = {}
    for item in data: 
        if "<Id>" in item and "..x.." not in item: 
            # CLEAN UP
            item = re.sub("\n", "##", item)
            #item = re.sub("</SEP>", "$$", item)
            # GET IDENTIFIER
            idno = re.findall("<Id>(.*?)</Id>", item)[0]
            converted[idno] = {}
            # GET METADATA
            try: 
                converted[idno]["author"] = re.findall("<Autor>(.*?)</Autor>", item)[0]
            except: 
                converted[idno]["author"] = "N/A"
            try: 
                converted[idno]["title"] = re.findall("<Titel>(.*?)</Titel>", item)[0]
            except: 
                converted[idno]["title"] = "N/A"
            try: 
                converted[idno]["pages"] = re.findall("<Untertitel>(.*?)</Untertitel>", item)[0]
            except: 
                converted[idno]["pages"] = "N/A"
            try: 
                converted[idno]["letter"] = re.findall("<Nummer>(.*?)</Nummer>", item)[0]
            except: 
                converted[idno]["letter"] = "N/A"
            try: 
                converted[idno]["year"] = re.findall("<Jahr>(.*?)</Jahr>", item)[0]
            except: 
                converted[idno]["year"] = "N/A"
            try: 
                converted[idno]["year"] = re.findall("<Jahr>(.*?)</Jahr>", item)[0]
            except: 
                converted[idno]["year"] = "N/A"
            # GET ALL KEYWORDS
            for k in keywords:
                try: 
                    keys = re.findall("<Schlagworte>(.*?)</Schlagworte>", item)[0]
                    if k in keys: 
                        converted[idno][k] = 1
                    else: 
                        converted[idno][k] = 0                
                except: 
                    converted[idno][k] = "N/A"
            # GET TEXT OF DESCRIPTION AND COMMENT
            try: 
                text = re.findall("<Text>(.*?)</Text>", item)[0]
                if "<SEP/>" in text: 
                    #print(text)                
                    text, comment = text.split("<SEP/>")
                    comment = re.sub("#", "", comment)
                    converted[idno]["comment"] = comment
                    text = re.sub("####", "", text)
                    if "litid" in text: 
                        litids = re.findall("litid.*?\d+  ", text)[0]
                        litids = re.sub("####", "", litids)
                        converted[idno]["litids"] = litids
                        text = re.sub("litid.*?\d+", "", text)
                        text = re.sub("####", "", text)
                        text = re.sub(" {2,20}", "", text)
                        text = re.sub("idid.\d+", "", text)
                        repeated = text[0:20]
                        text = re.sub("("+repeated+")(.*?)("+repeated+")", repeated, text)
                        converted[idno]["text"] = text
                    else: 
                        text = re.sub("####", "", text)
                        text = re.sub(" {2,20}", "", text)
                        text = re.sub("idid.\d+", "", text)
                        repeated = text[0:20]
                        text = re.sub("("+repeated+")(.*?)("+repeated+")", repeated, text)
                        converted[idno]["text"] = text
                        converted[idno]["litids"] = "N/A"
                else: 
                    if "litid" in text: 
                        litids = re.findall("litid.*?\d+  ", text)[0]
                        litids = re.sub("####", "", litids)
                        converted[idno]["litids"] = litids
                        text = re.sub("####", "", text)
                        text = re.sub(" {2,20}", "", text)
                        text = re.sub("idid.\d+", "", text)
                        text = re.sub("litid.*?\d+", "", text)
                        repeated = text[0:20]
                        text = re.sub("("+repeated+")(.*?)("+repeated+")", repeated, text)
                        converted[idno]["text"] = text
                    else: 
                        text = re.sub("####", "", text)
                        #print(text[0:120])
                        repeated = text[0:20]
                        text = re.sub("("+repeated+")(.*?)("+repeated+")", repeated, text)
                        #print(text[0:120], "\n")
                        converted[idno]["text"] = text
                        converted[idno]["litids"] = "N/A"
            except: 
                converted[idno]["text"] = "N/A"
                converted[idno]["comment"] = "N/A"
            #print(converted[idno])
    converted = pd.DataFrame(converted).T    
    print(converted.head())
    return converted



def save_converted(converted): 
    with open("converted.tsv", "w", encoding="utf8") as outfile: 
        converted.to_csv(outfile, sep="\t")
    
               
            
        




def main(): 
    data = read_file()
    keywords = get_keywords(data)
    converted = convert(data, keywords)
    save_converted(converted)


main()

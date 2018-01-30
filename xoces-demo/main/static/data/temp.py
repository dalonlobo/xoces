#Pre processing of phrases from ToC
def cleanTopicString(str1):
    #clean data

    lst = ["conclusion", "chapters", "chapter", "about the author", "bibliography", "preface", "table of contents", "contents", "copyright", "summary", "index", "acknowledgments", "acknowledgement",
           "notations", "notation", "references", "appendix", " who should read this book?"]

    string = str1.lower()
    string = re.sub(r"[0-9\.]", "", string)
    
    for ele in lst:
        string = string.replace(ele, " ")
        
    string = re.sub(r"\s{2,}", " ", string)
    
    if(string == "index") or (string == "introduction"):
        return None

    string = string.strip()
    if len(string) == 0:
        return None

    return string
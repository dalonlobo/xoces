import json
import re

#Pre processing of phrases from ToC
def cleanTopicString(str1):
    #clean data

    lst = ["conclusion", "chapters", "chapter", "about the author", "bibliography", "preface", "table of contents", "contents", "copyright", "summary", "index", "acknowledgments", "acknowledgement",
           "notations", "notation", "references", "appendix", " who should read this book?"]

    string = str1.lower()
    string = re.sub(r"[0-9\.]", "", string)

    if string.strip() == "index" or string.strip() == "introduction":
        return None
        
    for ele in lst:
        string = string.replace(ele, " ")
        
    string = re.sub(r"\s{2,}", " ", string)

    string = string.strip()
    if len(string) == 0:
        return None

    return string

def create_mapping_data(textbook_title):
    exclude = ["pattern recognition and machine learning", "website",\
               "- introduction"]
    
    with open(textbook_title + "_raw.json", "r") as f:
        data = json.load(f)
    
    hierarchy = ['course', 'topic', 'outcome']
    
    course = [{'id': 'c1', 'type': 'course', 'name': 'Machine Learning'}]
    
    topic = []
    outcome = []
    relationships = []
    topicIds = 1
    outcomeIds = 1
    relationshipIds = 1
    for index, item in enumerate(data):
        topicname = cleanTopicString(item['topicname'])
        if topicname in exclude or not item["keywordlist"]:
            continue
        if topicname:
            topic.append({'id':'t' + str(topicIds),
                          'type': 'topic',
                          'name': topicname
                          })
            for val in item["keywordlist"]:
                outcome.append({'id': 'o' + str(outcomeIds),
                                 'type': 'outcome',
                                 'name': val
                                 })
                relationships.append({'id':'r' + str(relationshipIds),
                                'type': 'belongs_to', 
                                'sourceId': 'o' + str(outcomeIds), 
                                'targetId': 't' + str(topicIds)
                                })
                relationshipIds += 1
                relationships.append({'id':'r' + str(relationshipIds),
                        'type': 'has_prerequisite_of', 
                        'sourceId': 'o' + str(outcomeIds), 
                        'targetId': 't' + str(topicIds)
                        })
                relationshipIds += 1
                outcomeIds += 1
            relationships.append({'id':'r' + str(relationshipIds),
                                    'type': 'belongs_to', 
                                    'sourceId': 't' + str(topicIds), 
                                    'targetId': 'c1'
                                    })
            relationshipIds += 1
            topicIds += 1
        if index == 50: break
        
    with open(textbook_title + "_mapped.json", "w") as f:
        mapping_data = {"hierarchy": hierarchy,
                   "course": course,
                   "topic": topic,
                   "outcome": outcome,
                   "relationships": relationships}
        json.dump(mapping_data, f)
        
create_mapping_data("murphy")
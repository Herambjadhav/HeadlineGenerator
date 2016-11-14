
import os
import csv
from bs4 import BeautifulSoup
from collections import defaultdict

if __name__ == "__main__":

    path = "/Users/garethdsouza/Git/csci544/DailyTrojan/files"

    i=0
    for root, dirs, files in os.walk(path):
        for f in files:
            # if(i == 10):
            #     break
            isArticle = True
            stringArticle = ''

            fullPathString = ('{}/{}'.format(root, f))
            file = open(fullPathString, "r", encoding="latin1")
            soup = BeautifulSoup(file.read(), 'html.parser')
            for articlesTag in soup.find_all('meta'):
                if(articlesTag.get('property') == "og:type"):
                    if(articlesTag.get('content') == "article"):
                        for articlesTag in soup.find_all('article'):
                            if "post-entry" in articlesTag.get('class'):
                                for articleContent in articlesTag.contents:
                                    if (hasattr(articleContent, 'attrs')):
                                        if ('headline' in articleContent.attrs.values()):
                                            # if(isArticle):
                                            #     isArticle = False
                                            stringArticle += (articleContent.text+"\n\n\n")
                                            for subTags in articlesTag.contents:
                                                if('entry-content-wrapper' in subTags.get('class')):
                                                    for eachP in subTags.contents:
                                                        if('entry-content' in eachP.get('class')):
                                                            for ptags in eachP.contents:
                                                                if(ptags.string is not None):
                                                                    stringArticle += (ptags.string)

            with open(f+'.txt', 'w') as f:
                f.write(stringArticle.strip())


                                    # if('http' in absURL[:4]):
                    #     if(absURL in mapdict.values()):
                    #         outgoingList.append(absURL)


            i+=1
            print(i)

    # with open('NYTimes2.txt','w',encoding="latin1") as f:
    #     for key,value in outGoingLinks.items():
    #         f.write('{} {}\n'.format(key," ".join(value)))



    print("HI")


# Python file for Text Rank
import sys
import nltk


def keyphrases(content):
    texttokens = nltk.word_tokenize(content)
    taggedtokens = nltk.pos_tag(texttokens)
    filteredtokens = [x for x in taggedtokens if x[1] in ['NN', 'JJ', 'NNP']]
    dotlesstokens = [(x[0].replace('.', ''), x[1]) for x in filteredtokens]
    print(dotlesstokens)


def sentences(content):
    print("Nothing to see here, move on! :P")


def main():
    filename = sys.argv[1]
    filecontent = open(filename, "r")
    content = filecontent.read()
    # print(content)
    keyphrases(content)
    sentences(content)

if __name__ == '__main__':
    main()

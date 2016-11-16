# Python file for Text Rank
import sys
import nltk
import itertools
import networkx


def weightcalculation(firsttoken, secondtoken):
    if len(firsttoken) > len(secondtoken):
        firsttoken, secondtoken = secondtoken, firsttoken
    distances = range(len(firsttoken) + 1)
    for index2, char2 in enumerate(secondtoken):
        newdistances = [index2 + 1]
        for index1, char1 in enumerate(firsttoken):
            if char1 == char2:
                newdistances.append(distances[index1])
            else:
                newdistances.append(1 + min(distances[index1], distances[index1 + 1], newdistances[-1]))
        distances = newdistances
    return distances[-1]


def makegraph(tokens):
    tokengraph = networkx.Graph()
    tokengraph.add_nodes_from(tokens)
    pairstokens = list(itertools.combinations(tokens, 2))
    for individualpairs in pairstokens:
        firsttoken = individualpairs[0]
        secondtoken = individualpairs[1]
        weightvalue = weightcalculation(firsttoken, secondtoken)
        tokengraph.add_edge(firsttoken, secondtoken, weight=weightvalue)
    return tokengraph


def keyphrases(content):
    uniquelist = list()
    texttokens = nltk.word_tokenize(content)
    taggedtokens = nltk.pos_tag(texttokens)
    tokenlist = [x[0] for x in taggedtokens]
    filteredtokens = [x for x in taggedtokens if x[1] in ['NN', 'JJ', 'NNP']]
    dotlesstokens = [(x[0].replace('.', ''), x[1]) for x in filteredtokens]
    uniquelist.append([x[0] for x in dotlesstokens if x[0] not in uniquelist])
    keyphrasesgraph = makegraph(uniquelist[0])
    tokenpagerank = networkx.pagerank(keyphrasesgraph, weight='weight')
    phrases = sorted(tokenpagerank, key=tokenpagerank.get, reverse=True)
    countthird = int(len(uniquelist[0]) / 3)
    phrases = phrases[0:countthird+1]
    keyphrasesset = set([])
    identifiedset = set([])
    i = 0
    j = 1
    while j < len(tokenlist):
        firsttoken = tokenlist[i]
        secondtoken = tokenlist[j]
        if firsttoken in phrases and secondtoken in phrases:
            phrase = firsttoken + ' ' + secondtoken
            keyphrasesset.add(phrase)
            identifiedset.add(firsttoken)
            identifiedset.add(secondtoken)
        else:
            if firsttoken in phrases and firsttoken not in identifiedset:
                keyphrasesset.add(firsttoken)
            if j == len(tokenlist)-1 and secondtoken in phrases and secondtoken not in identifiedset:
                keyphrasesset.add(secondtoken)
        i += 1
        j += 1
    print('Key phrases: ', keyphrasesset)


def sentences(content):
    sentencetokens = nltk.data.load('tokenizers/punkt/english.pickle').tokenize(content.strip())
    sentencesgraph = makegraph(sentencetokens)
    sentencepagerank = networkx.pagerank(sentencesgraph, weight='weight')
    allsentences = sorted(sentencepagerank, key=sentencepagerank.get, reverse=True)
    sentence = ' '.join(allsentences)
    tokensentences = sentence.split()[0:100]
    sentence = ' '.join(tokensentences)
    print('Summary sentence: ', sentence)


def main():
    filename = sys.argv[1]
    filecontent = open(filename, "r")
    content = filecontent.read()
    keyphrases(content)
    sentences(content)


if __name__ == '__main__':
    main()

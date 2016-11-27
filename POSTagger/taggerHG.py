import nltk
import sys
import random
import operator

from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pycorenlp import StanfordCoreNLP
from nltk.tokenize import sent_tokenize



def chunk_tagged_sents(tagged_sents):
    from nltk.chunk import regexp

    # define a chunk "grammar", i.e. chunking rules
    grammar = r"""
        NP: {<DT|PP\$>?<JJ>*<NN.*>+} # noun phrase
        PP: {<IN><NP>}               # prepositional phrase
        VP: {<MD>?<VB.*><NP|PP>}     # verb phrase
        CLAUSE: {<NP><VP>}           # full clause
	"""
    chunker = regexp.RegexpParser(grammar, loop=2)
    chunked_sents = [chunker.parse(tagged_sent) for tagged_sent in tagged_sents]

    return chunked_sents

def get_chunks(chunked_sents, chunk_type='NP'):
    all_chunks = []
    # chunked sentences are in the form of nested trees
    for tree in chunked_sents:
        chunks = []
        # iterate through subtrees / leaves to get individual chunks
        raw_chunks = [subtree.leaves() for subtree in tree.subtrees()
                      if subtree.node == chunk_type]
        for raw_chunk in raw_chunks:
            chunk = []
            for word_tag in raw_chunk:
                # drop POS tags, keep words
                chunk.append(word_tag[0])
            chunks.append(' '.join(chunk))
        all_chunks.append(chunks)

    return all_chunks

def readFile(filePath):
    with open(filePath, 'r', encoding="latin1") as f:
        # Open file and read Lines
        fileLines = f.read().splitlines()

        # Check if text file is not empty
        if(len(fileLines) > 0):
            # TO DO - confirm how many lines of the summarized text are to be considered?
            summarizedText = fileLines[0]
            return summarizedText
        else:
            return None


def dictToList(inputDict):
    outputList = list()
    listLength = len(inputDict)
    i = 0
    count = listLength
    while(count > 0):
        if(i in inputDict.keys()):
            count -= 1
            outputList.append((i,inputDict[i]))
        i += 1
    return outputList


# def printTreeSentences(sentenceTree):
    # for node in sentenceTree:
def makeSentences(dependecyGraph):

    k = None
    subject = list()
    object = list()
    verb = list()
    for eachSentence in dependecyGraph:

        dependencies = eachSentence['enhancedPlusPlusDependencies']
        k =dependencies
        for eachDependancy in dependencies:

            if(":" in eachDependancy['dep']):
                searchPOS = eachDependancy['dep'][:eachDependancy['dep'].index(":")]
            else:
                searchPOS = eachDependancy['dep']

            if(searchPOS == 'ROOT'):
                verb.append(eachDependancy)
            if(searchPOS == 'nsubj'):
                subject.append(eachDependancy)

            for eachObjectType in ['dobj','nmod','compound']:
                if (eachObjectType in searchPOS):
                    object.append(eachDependancy)


    rootIndex = verb[0]['dependent']

    connectedSubjects = list()
    connectedObjects = list()


    # Connected Subject
    for eachSubject in subject:
        if(eachSubject['governor'] == rootIndex):
            connectedSubjects.append(eachSubject)

    for eachObject in object:
        if (eachObject['governor'] == rootIndex):
            connectedObjects.append(eachObject)

    # Connected Object
    if(len(connectedObjects) > 0):
        blah = digInto(list(),k,connectedObjects[0])
        POS = nltk.pos_tag([eachResult['dependentGloss'] for eachResult in blah])
        for eachPOS in POS:
            if ('NN' in eachPOS[1]):
                if ('ing' not in eachPOS[0][-3:]):
                    connectedObjects.append(eachPOS[0])

    if (len(connectedSubjects) > 0):
        blah2 = digInto(list(),k,connectedSubjects[0])
        POS = nltk.pos_tag([eachResult['dependentGloss'] for eachResult in blah2])
        for eachPOS in POS:
            if ('NN' in eachPOS[1]):
                connectedSubjects.append(eachPOS[0])

    startPhrase = list()
    for eachDictItem in connectedSubjects:
        startPhrase.append(extractDependentGloss(eachDictItem))

    endPhrase = list()
    for eachDictItem in connectedObjects:
        endPhrase.append(extractDependentGloss(eachDictItem))


    sentenceBlocks = dict()
    sentenceBlocks['subject'] = startPhrase
    sentenceBlocks['verb'] = verb
    sentenceBlocks['object'] = endPhrase
    return sentenceBlocks

def extractDependentGloss(inputDict):
    if (isinstance(inputDict, dict)):
        return inputDict['dependentGloss']
    else:
        return inputDict




def digInto(stack,k,entry):
    for eachItem in k:
        if(eachItem['governor'] == entry['dependent']):
            stack.append(eachItem)
            digInto(stack,k,eachItem)

    return stack

def possibleHeadlines(orderedSet):

    orderedList = dictToList(orderedSet)
    sentenceTree = defaultdict(list)
    rowIndex = 0
    prev = orderedList[0][1][0]


    for eachNode in orderedList:

        pos = eachNode[1][0]

        if ("N" in prev and "V" in pos):
            rowIndex += 1
        if("V" in prev and "N" in pos):
            rowIndex += 1

        sentenceTree[rowIndex].append(eachNode)
        prev = pos


def getMainVerb(verbPhrase):
    verbs = []
    for eachnode in verbPhrase:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "V"):
                verbs.append(eachnode[0])
                return verbs
    return None

def getNPNodes(nodeList):
    NPNodeList = list()

    for eachnode in nodeList:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "NP"):
                NPNodeList.append(eachnode)

    return (NPNodeList)

def getSingleNNPNode(nodeList):
    NPNodeList = list()

    for eachnode in nodeList:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "NP"):
                for nodes in eachnode:
                    if(nodes[1] == 'NNP' or nodes[1] == 'NNPS'):
                        NPNodeList.append(eachnode)
                        return (NPNodeList)
    return None

def getSingleNNNode(nodeList):
    NPNodeList = list()

    for eachnode in nodeList:
        if(hasattr(eachnode,"_label")):
            if(eachnode._label == "NP"):
                for nodes in eachnode:
                    if(nodes[1] == 'NN'):
                        NPNodeList.append(eachnode)
                        return (NPNodeList)
    return None



def getSentenceTree(posTree):

    for eachnode in posTree:
        # If the node is a tree
        if(hasattr(eachnode,"_label")):
            print("TREE")
        else:
            print("LEAF")


def makePossibleHeadlines(result):

    orderedSubset = dict()

    NNPList = []
    NNList = []

    ignoreIndex = []



    # Remove preposed adjuncts based on commas
    treeLength = len(result)
    for nodeIndex in range(0,treeLength):
        # Check if its not a sub tree
        if(not hasattr(result[nodeIndex],"_label")):
            if(result[nodeIndex][0] == ','):
                nodeList = [result[nodeIndex - 1],result[nodeIndex + 1]]
                NNPNodes = getNNPNode(nodeList)
                if(NNPNodes):
                    orderedSubset[nodeIndex] = ('NP',NNPNodes)
                    NNPList += NNPNodes

    # Complex NP not found pick up simple NP
    if(len(NNPList) == 0):
        for nodeIndex in range(0, treeLength):
            if (hasattr(result[nodeIndex], "_label")):
                NNPNodes = getSingleNNPNode([result[nodeIndex]])
                if(NNPNodes):
                    orderedSubset[nodeIndex] = ('NP', NNPNodes)
                    NNPList += NNPNodes



    #Pick up simple NP with NN
    for nodeIndex in range(0,treeLength):
        if(hasattr(result[nodeIndex],"_label")):
            NNNodes = getSingleNNNode([result[nodeIndex]])
            if(NNNodes):
                orderedSubset[nodeIndex] = ('NP', NNNodes)
                NNList += NNPNodes

    #Get the verb (Predicates) that join Subject and Object
    for nodeIndex in range(0, treeLength):
        if(hasattr(result[nodeIndex],"_label")):
            if(result[nodeIndex]._label == 'VP'):
                mainverbs = getMainVerb(result[nodeIndex])
                orderedSubset[nodeIndex] = ('V',mainverbs)





    return orderedSubset

def TreeToList(inputTree):
    returnList = list()
    for eachNode in inputTree[0]:
        returnList.append(eachNode[0])
    return returnList

def filterNounPhrases(nounWords,nounPhrases):
    probableNounPhrases = list()
    returnNounPhrases = list()

    maxScore = 0
    for nounWord in nounWords:
        score = 0
        for nounPhrase in nounPhrases:
            for treeNode in nounWord:
                if(nounPhrase in treeNode[0]):
                    score += 1
        if(score > 0):
            if(score > maxScore):
                maxScore = score
            probableNounPhrases.append([nounWord,score])

    probableNounPhrases.sort(key=operator.itemgetter(1),reverse=True)
    for eachNounPhrase in probableNounPhrases:
        # if(eachNounPhrase[1] >= maxScore):
        returnNounPhrases.append(TreeToList(eachNounPhrase))
        # else:
        #     break

    return (returnNounPhrases)


def getDescribersCommas(tokens):
    commaList= list()
    commaIndex = 0
    for eachtoken in tokens:
        if("," in eachtoken):
            # Check if the comma is used to describe
            # and not used as a punctuation to list a set of things
            # eg red, green and blue

            commaIndex += 1

def initTagger(summarizedText):
    if(summarizedText):
        # split the input text into sentences extract the 1st one
        sent_tokenize_list = sent_tokenize(summarizedText)

        tokens = nltk.word_tokenize(sent_tokenize_list[0], language='english')
        # perform POS Tagging on the tokens

        posTokens = nltk.pos_tag(tokens)


        # p = Parser()
        # linkages = p.parse_sent("This is a simple sentence.")
        nlp = StanfordCoreNLP('http://localhost:9000')

        output = nlp.annotate(summarizedText, properties={
            'annotators': 'tokenize,ssplit,pos,depparse,parse',
            'outputFormat': 'json'
        })

        sentenceBlocks = makeSentences(output['sentences'])

        # pattern to recognize noun phrases
        # create chunk parser
        # NPChunker = nltk.RegexpParser(patternNP)
        NPChunker = nltk.RegexpParser('''
                        NP: {<DT>? <JJ>* <NN>* <NNP>* <NNS>* <NP>*} # NP modified
                         # P: {<IN>}           # Preposition
                         # V: {<V.*>}          # Verb
                         # PP: {<P>}      # PP -> P NP
                         # VP: {<V> <NP|PP>*}  # VP -> V (NP|PP)*
                        ''')


        resultNP = NPChunker.parse(posTokens)

        NPNodes = getNPNodes(resultNP)


        subjects = filterNounPhrases(NPNodes,sentenceBlocks['subject'])
        verb = sentenceBlocks['verb'][0]['dependentGloss']
        objects = filterNounPhrases(NPNodes, sentenceBlocks['object'])


        porter_stemmer = PorterStemmer()
        verb = porter_stemmer.stem(verb)
        lmtzr = WordNetLemmatizer()
        verb = lmtzr.lemmatize(verb, 'v')+'s'

        keyParts = dict()
        keyParts['subject'] = subjects
        keyParts['verb'] = [verb]
        keyParts['object'] = objects

        return keyParts

    else:
        return "No text in input file"







if __name__ == "__main__":
    # Get the file path from command line
    # requires sys package
    # Sanity check for input filename
    # filePath = "Data/sum_test1.txt"

    if(len(sys.argv)>1):
        filePath = sys.argv[1]
        # filePath = "Data/sum_test1.txt"
    else:
        # print("Error file not found. Please check that the file exists\n")
        # print("File path to be specified as input command line argument\n")
        exit(1)

    # filePath = "Data/sum_test3.txt"
    summarizedText = readFile(filePath)

    # print(summarizedText)

    # print("-------")

    try:
        possibleHeadlies = list()
        dictionaryParts = initTagger(summarizedText)

        for eachSubject in dictionaryParts['subject']:
            for eachVerb in dictionaryParts['verb']:
                if(dictionaryParts['object']):
                    for eachObject in dictionaryParts['object']:
                        # print(POSTagger.ginger.gingerCheck(' '.join(eachSubject)+" "+eachVerb+" "+' '.join(eachObject)))
                        possibleHeadlies.append(' '.join(eachSubject) + " " + eachVerb + " " + ' '.join(eachObject))
                else:
                    # print(POSTagger.ginger.gingerCheck(' '.join(eachSubject)+" "+eachVerb))
                    possibleHeadlies.append(' '.join(eachSubject) + " " + eachVerb)

        with open('headline.txt', 'w', encoding="latin1") as f:
            headlineString = random.choice(possibleHeadlies)
            f.write(headlineString+".")
        f.close()

    except:
        exit(1)

    # print("-------")

    # filePath = "Data/sum_test2.txt"
    # initTagger(filePath)

    # filePath = "Data/sum_test3.txt"
    # initTagger(filePath)





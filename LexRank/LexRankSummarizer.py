import sys
from nltk.tokenize import sent_tokenize, word_tokenize
from fuzzywuzzy import fuzz
import math

threshold = 30

def pageRank(matrix, sentences):
    eigen = [1 for x in range(len(sentences))]

    for h in range(0,10):
        w = [0 for x in range(len(sentences))]

        for i in range(0, len(sentences)):
            for j in range(0 , len(sentences)):
                w[i] += (matrix[i][j] * eigen[j])

        eigen = normalizeMatrix(w)

    eigenCounts = []

    for i in range(0, len(sentences)):
        obj = {}
        obj['weight'] = eigen[i]
        obj['sentence'] = sentences[i]
        obj['index'] = i
        eigenCounts.append(obj)

    eigenCounts = sorted(eigenCounts, key=lambda k: k['weight'], reverse = True )
    return eigenCounts

def normalizeMatrix(array):
    distance = 0;

    for val in array:
        distance += (val * val)

    distance = math.sqrt(distance)

    index = 0
    for val in array:
        if val != 0:
            array[index] = (val/distance)
        index += 1

    return array

def constructMatrix(sentences):
    matrix = [[0 for x in range(len(sentences))] for y in range(len(sentences))]
    i = 0
    for sentenceA in sentences:
        j = 0
        for sentenceB in sentences:
            value = fuzz.ratio(sentenceA, sentenceB)
            if(value < threshold):
                value = 0
            matrix[i][j] = value
            j += 1
        matrix[i] = normalizeMatrix(matrix[i])
        i += 1

    return matrix

def summarize(textContent, summaryLines):
    sentences = sent_tokenize(textContent)
    words = []
    for sentence in sentences:
        words.append(word_tokenize(sentence.lower()))

    matrix = constructMatrix(sentences)
    sortedSentences = pageRank(matrix, sentences)

    print(sortedSentences)
    topLines = sortedSentences[0:min(summaryLines, len(sortedSentences))]

    summary = ''
    for line in topLines:
        summary += line['sentence'] + " "

    return summary

print ('Argument count : ', len(sys.argv))
#exit if file name is not provided as command line argument
if len(sys.argv) != 3:
    print ('Please send file name as command line argument')
    exit(0)

fileName = sys.argv[1]
summaryLines = int(sys.argv[2])
print ('File name : ', fileName, ' SummaryLines : ', summaryLines)

#read all lines of file
fileHandler = open(fileName,"r", encoding="latin1")
content = fileHandler.read()
fileHandler.close()

summary = summarize(content, summaryLines)
print(summary)

#write output to file
fileHandler = open("summary.txt","w", encoding="latin1")
fileHandler.write(summary)
fileHandler.close()
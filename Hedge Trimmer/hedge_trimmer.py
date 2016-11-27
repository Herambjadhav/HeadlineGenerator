import os, nltk, sys
from nltk.parse import stanford
from nltk.tree import  Tree
from nltk.tree import ParentedTree as p
# os.environ['STANFORD_PARSER'] = 'C:\\Users\\RJ\\stanford-parser-full-2015-12-09\\stanford-parser.jar'
# os.environ['STANFORD_MODELS'] = 'C:\\Users\\RJ\\stanford-parser-full-2015-12-09\\stanford-parser-3.6.0-models.jar'
java_path = "C:\\Program Files\\Java\\jre1.8.0_111\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path
# sentences1 = Tree.fromstring("An international relief agency announced Wednesday that it is withdrawing from North Korea.")
parser = stanford.StanfordParser(model_path="C:\\Users\\RJ\\stanford-parser-full-2015-12-09\\edu\\stanford\\nlp\\models\\lexparser\\englishPCFG.ser.gz")
# sentences = parser.raw_parse("IN AN election that left Republicans in charge of the presidency, Congress, and many state governments, California shines like a ray of hope for Democrats")
# sentences = parser.raw_parse("Kurdish guerilla forces moving with lightning speed poured into Kirkuk today immediately after Iraqi troops, fleeing relentless U.S. airstrikes, abandoned the hub of Iraqs rich northern oil fields.")
# sentences= parser.raw_parse("Rebels agree to talks with government officials said tuesday")
# sentences = parser.raw_parse("An international relief agency announced Wednesday that it is withdrawing from North Korea.")
# sentences = parser.raw_parse("A fire killed a firefighter who was fatally injured as he searched the house")
# sentences = parser.raw_parse("According to a now finalized blueprint described by U.S. officials and other sources, the Bush administration plans to take complete, unilateral control of a post-Saddam Hussein Iraq")
# sentences = parser.raw_parse("A suspect fled from police after engaging in lewd behavior in Doheny Memorial Library Saturday afternoon, prompting the building’s evacuation and a two hour attempt to apprehend the suspect inside. ")
# sentences = parser.raw_parse("USC students Brian Zatulove, Zach Wise, Jordan Wise and Shaun Edalati quickly seized on the opportunity, launching a startup named Reefer that acts as a marketing suite for cannabis dispensaries.")

time_expressions = ['one','two','three','four','five','six','seven','eight','nine','ten','twenty','thirty',
                    'forty','fifty','sixty','seventy','eighty','ninety','hundred','thousand',
                    'monday','tuesday','wednesday','th,ursday','friday','saturday','sunday',
                    'january','february','march','april','may','june','july','august','september','october','november','december','year','day','week','month',
                    'today','yesterday','tomorrow','tonight','tonite','before','after','earlier','later','ago',
                    'afternoon','evening', 'morning']

verb_time = ['said', 'next', 'coming', 'this', 'previous']

summarized_file = sys.argv[1]

# with open(summarized_file, "r", encoding="latin1") as fp:
#     file_contents = fp.read().splitlines()
#     for sentence in file_contents:
#         sentences = parser.raw_parse(sentence)
        # print(sentences)

# for s in sentences:
#     # print(s)
#     str1 = str(s)




# nltk_tree = Tree.fromstring(str1)
# # ptree = p.fromstring(str1)

# print(ptree)
#     if i.label() == 'S':
#         head += traverse(i)
#         break
#     # print(i, i.label(),i.leaves())
# print(head)

word = ''
head = []
threshold = 10
ignore_labels = ['DT', 'PP']
overlap_flag = False
l = []


def traverse_tree(tree, label, parent_label, flag):

    # print("tree:", tree)
    # print("label:", label)
    # global overlap_flag

    if label != 'ROOT' and  label != 'S':
        if parent_label == tree.label():
            flag = True
            return tree.leaves()

    # Length of tree gives the number of child nodes it has.
    n = len(tree)
    # print(n)

    for i, subtree in enumerate(tree):

        temp = []
        parent = tree.label()

        if type(subtree) == nltk.tree.Tree:
            #  Ignoring low content nodes
            if subtree.label() == "SBAR":
                break

            # Ignoring overlap contents
            curr_label =subtree.label()
            if curr_label == parent and parent == 'S' and ( curr_label == 'VP' or curr_label == 'NP') :
                break
            # if len(head) >= 12:
            #         break

            word = traverse_tree(subtree, subtree.label(), parent, flag)

            # Ignoring low content nodes like time expressions.
            if word is not None:
                # for item in word:
                j = 0
                while j != len(word):
                    if word[j].lower() in time_expressions:
                        word.remove(word[j])
                        j -= 1
                        if head[-1].lower() in verb_time:
                            head.remove(head[-1])
                    j += 1
                head.extend(word)
            if overlap_flag:
                break
            # print(word)

        # Ignoring Determiners
        elif label not in ignore_labels:
            temp.append(subtree)

        if i + 1 == n:
            return temp


parent_label = 'S'


def generate_headline(parsed_tree):

    np_flag = False
    for tree in parsed_tree:
        if tree.label() == 'S':

            for subtree in tree:
                overlap_flag = False
                if subtree.label() == tree.label():
                    overlap_flag = True
                tag = subtree.label()
                if tag == 'NP' or tag == 'VP' or tag == 'S':
                    # if tag == 'NP':
                    #     np_flag = True
                    h = traverse_tree(subtree, tree.label(), parent_label,overlap_flag)
                else:
                    continue


head = []

output_file  = open("headline.txt","w")
with open(summarized_file, "r") as fp:
    file_contents = fp.read().splitlines()
    for sentence in file_contents:

        head = []
        sentences = parser.raw_parse(str(sentence))
        # print(sentences)

        for s in sentences:
            # print(s)
            str1 = str(s)
            # print(str1)
        nltk_tree = Tree.fromstring(str1)

        generate_headline(nltk_tree)
        headline = " ".join(head)
        output_file.write(headline + "\n")
fp.close()
output_file.close()

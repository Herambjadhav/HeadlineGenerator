import os, nltk, sys
from string import punctuation
from nltk.parse import stanford
from nltk.tree import Tree

# java_path = "C:\\Program Files\\Java\\jre1.8.0_111\\bin\\java.exe"
# os.environ['JAVAHOME'] = java_path

parser = stanford.StanfordParser(model_path="C:\\Users\\RJ\\stanford-parser-full-2015-12-09\\edu\\stanford\\nlp\\models\\lexparser\\englishPCFG.ser.gz")

time_expressions = ['one','two','three','four','five','six','seven','eight','nine','ten','twenty','thirty',
                    'forty','fifty','sixty','seventy','eighty','ninety','hundred','thousand',
                    'monday','tuesday','wednesday','th,ursday','friday','saturday','sunday',
                    'january','february','march','april','may','june','july','august','september','october','november','december','year','day','week','month',
                    'today','yesterday','tomorrow','tonight','tonite','before','after','earlier','later','ago',
                    'afternoon','evening', 'morning']

verb_time = ['said', 'next', 'coming', 'this', 'previous']

spec_chars = ['$', '-', ':']
summarized_file = sys.argv[1]


word = ''
head = []
threshold = 10
ignore_labels = ['DT', 'PP']
overlap_flag = False


# pp_index = {}
# pp_words = []
# pcount = 0


def traverse_tree(tree, label, parent_label, flag):

    # print("tree:", tree)
    # print("label:", label)
    # global overlap_flag
    global pp_words
    global pp_index
    global  pcount
    if label != 'ROOT' and  label != 'S':
        if parent_label == tree.label():
            flag = True
            temp = []
            for sub in tree:
                if (len(head) + len (temp)) < threshold:
                    temp.extend(sub.leaves())
            return temp
            # return tree.leaves()

    # Length of tree gives the number of child nodes it has.
    n = len(tree)
    # print(n)
    parent = tree.label()
    # if parent == 'PP':
    #     pp_words = []
    #     index = 0
    #     pcount = 0
    for i, subtree in enumerate(tree):

        temp = []

        if parent == 'PP':
            pcount += 1
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
                if word in spec_chars:
                    return
                j = 0
                while j != len(word):
                    if word[j].lower() in time_expressions and (parent != 'NP' or parent != 'VP'):
                        word.remove(word[j])
                        j -= 1
                        if len(head) > 1:
                            if head[-1].lower() in verb_time:
                                head.remove(head[-1])
                    j += 1
                head.extend(word)
                # if parent == 'PP':
                #     pp_words.extend(word)
                #     if word:
                #         index = 0
                #         if len(pp_words) == 1:
                #             index = head.index(word[0])
                #         pp_index[index] = pcount

            if overlap_flag:
                break
            # print(word)

        # Ignoring Determiners
        elif label not in ignore_labels:
            temp.append(subtree)

        if i + 1 == n:
            return temp

        # pp_index[index] = pp_words
        # print(pp_index)
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


# head = []
# pp_count = 0
# def cal_pp(tree):
#     global pp_count
#
#     for i, subtree in enumerate(tree):
#
#         temp = []
#         parent = tree.label()
#
#         if type(subtree) == nltk.tree.Tree:
#             #  Ignoring low content nodes
#             if subtree.label() == "PP":
#                 pp_count += 1
#             cal_pp(subtree)


output_file  = open("headline.txt","w")
with open(summarized_file, "r") as fp:
    file_contents = fp.read().splitlines()
    for sentence in file_contents:
        sen_list = sentence.split()

        head = []
        sentences = parser.raw_parse(str(sentence))
        # print(sentences)

        for s in sentences:
            # print(s)
            str1 = str(s)
            # print(str1)
        nltk_tree = Tree.fromstring(str1)
        # cal_pp(nltk_tree)
        # print(pp_count)
        generate_headline(nltk_tree)
        ori_sen = " ".join(sen_list)
        headline = (' '.join(word for word in head if word not in punctuation) + ".").capitalize()

        # print(head)

        # print(len(head), len(sen_list))
        # print(len(head)/len(sen_list))
        head_length = len(head)
        # if head_length/len(sen_list) > 0.75:
            # remove trailing PP
        # headline = unrefined_headline.translate(string.maketrans("",""), string.punctuation)

        print("Orignal: ", ori_sen)
        print("Generated: ", headline)
        print("\n")
        output_file.write(headline + "\n")
fp.close()
output_file.close()
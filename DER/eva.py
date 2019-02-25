import py2neo
import math
from py2neo import Graph,Node,Relationship,size, order
test_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="123"
)

def calculate(nodelist1,nodelist2):
#    intersection = [v for v in nodelist1 if v in nodelist2]
    intersection = list(set(nodelist1).intersection(set(nodelist2)))
    if(len(intersection)>0):
        re1 = (math.log(max(len(nodelist1),len(nodelist2))) - math.log(len(intersection)))
        re2 = math.log(5598596) - math.log(min(len(nodelist1),len(nodelist2)))
        return 1 - re1/re2
    else:
        return 0

def C_n_2(n):
    return math.factorial(n)/(2 * math.factorial(n - 2))

def cal_mw(name1, name2):

    find_code_1 = test_graph.find_one(
      label="Page",
      property_key="title",
      property_value=name1
    )
    #print find_code_1['title']

    find_code_2 = test_graph.find_one(
      label="Page",
      property_key="title",
      property_value=name2
    )
    #print find_code_2['title']
    match_relation1  = test_graph.match(start_node=find_code_1,bidirectional=False)
    nodelist1 = []
    for i in match_relation1:
        nodelist1.append(i.end_node())

    match_relation2  = test_graph.match(start_node=find_code_2,bidirectional=False)
    nodelist2 = []
    for j in match_relation2:
        nodelist2.append(j.end_node())

    #print len(nodelist1)
    #print len(nodelist2)
    mw = calculate(nodelist1,nodelist2)
    #if mw == 0:
    #    mw = 0.0
    print(name1 + '\t' + name2 + '\t' + str(mw))
    return mw

inputfile = open('./Orig/CE30_pruned.txt')
outfile = open('./Orig/Result_ce_outx2_top5.txt', 'w')
Allscore = 0
for line in inputfile:
    strs = line.strip().split('\t')
    q = strs[0]
    le = 6
    si = min(le, len(strs))
    ents = strs[1:si]
    itera = []
    for ent in ents:
        mw_score = cal_mw(q, ent)
        itera.append([ent, mw_score])
    print itera
    all_score = 0
    for i in range(0, len(itera)):
        pair_a = itera[i]
        for j in range(i+1, len(itera)):
            pair_b = itera[j]
            ## CAL
            word_a, score_a = pair_a[0], pair_a[1]
            word_b, score_b = pair_b[0], pair_b[1]
            sim = cal_mw(word_a, word_b)
            #print(word_a + '\t' + word_b + '\t' + str(sim))
            all_score += score_a * score_b * math.exp(-2 * sim)
    #print C_n_2(len(itera))
    print all_score/C_n_2(len(itera))
    Allscore += all_score/C_n_2(len(itera))
    outfile.write(str(all_score/C_n_2(len(itera))) + '\n')
    outfile.flush()
outfile.write(str(Allscore/float(15)) + '\n')


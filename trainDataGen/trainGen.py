import functions

input = open('./query_anno/Query_shorten_100.txt')
output = open('./query_anno/100_top200/Query_top200.txt', 'w')
input1 = open('./query_anno/Query_shorten_100.txt')
counter = 0
word_frequency = dict()
for line in input:
    parts = line.strip().split('\t')
    # count the query in
    for i in range(0, len(parts)):
        for w in parts[i].split(' '):
            if w !='':
                try:
                    word_frequency[w] += 1
                except:
                    word_frequency[w] = 1
print (len(word_frequency))

ratio = dict()
he = sum(word_frequency.values())
for item in word_frequency:
    ratio[item] = float(word_frequency[item])/float(he)

for nline in input1:
    counter += 1
    print(counter)
    parts = nline.strip().split('\t')
    docs = []
    for i in range(1, len(parts)):
        docs.append(parts[i])
    flag = True
    # all words in the query should be in the dic
    # for qw in parts[0].split(' '):
    #    if qw not in word_frequency:
    #        flag = False
    if flag:
        word2prob = functions.word2prob(parts[0], docs, ratio)
        prob_string = ''
        for w in word2prob:
            prob_string = prob_string + w[0] + '*' + str(w[1]) + ' '
        prob_string = prob_string[:-1]
        output.write(parts[0] + '\t' + str(len(word2prob)) + '\t' + prob_string)
        output.write('\n')
        output.flush()
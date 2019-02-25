def count_winD (w, D): # efficiency could be improved by represeting each document as a dictionary of frequency
    counter = 0        # tf(w,D)
    D_words = D.split(' ')
    for D_word in D_words:
        if w == D_word:
            counter += 1
    return float(counter)

def w_in_M(w, rele_Doc, lamda, ratio, flag): # P(w|M_D)= lamda*tf(w,D)/sum_v{tf(w,D)} + (1-lamda)*P(w|G)
                         # sum_v{tf(w,D)} = len(D)
    try:
        value = lamda*count_winD(w,rele_Doc)/len(rele_Doc.split(' ')) + (1-lamda)*ratio[w]
    except:
        value = lamda*count_winD(w,rele_Doc)/len(rele_Doc.split(' '))
    if value == 0:
        if flag:
            value = 0.0000000000000001
    return value

def p_w(w, retre_Docs, lamda, ratio):    # P(w) = sum_mD{P(w|M_D) * P(M_D)}
    P_w = 0
    for rele_Doc in retre_Docs:
        P_w += w_in_M(w, rele_Doc, lamda, ratio, False) * 1/float(len(retre_Docs))
    return P_w

def get_joint_prob(w, query, retre_Docs,lamda, ratio): #p(w,Q) = p(w) * product(sum)
    query_words = query.split(' ')
    product = 1
    pw = p_w(w, retre_Docs,lamda, ratio)
    for q in query_words:
        sum = 0
        for doc in retre_Docs:
            # p(q|M) * p(M|w)
            sum += w_in_M(q, doc, lamda, ratio, True) * w_in_M(w, doc, lamda, ratio, False)* pw / float(len(retre_Docs))
        product *= sum
    return pw*product


def word2prob(query, docs, ratio):
    uniquewords = []
    for i in range(0, len(docs)):
        # unique words
        for w in docs[i].split(' '):
            #if w not in uniquewords:
            uniquewords.append(w)
    uniquewords = set(uniquewords)
    if '' in uniquewords:
        uniquewords.remove('')
    ### remove the query words
    query_words = query.split(' ')
    uniquewords = list(set(uniquewords).difference(set(query_words)))
    final_distri = {}
    lamda = 0.6
    p_Q = 0
    for w in uniquewords:
        p_Q += get_joint_prob(w, query, docs, lamda, ratio)
    for w in uniquewords:
        final_distri[w] = get_joint_prob(w, query, docs,lamda, ratio)/p_Q # p(w,Q)/p(Q) = p(w|Q)
    dis_sort = sorted(final_distri.items(), key= lambda item:item[1], reverse= True)
    #print (dis_sort[:10])
    ##########################change
    if len(dis_sort)>200:
        return dis_sort[:200]
    else:
        return dis_sort

def test():
    input = open('./reproduction/toy_toy_rm.txt')
    for line in input:
        parts = line.strip().split('\t')
        #print(len(parts))
        docs = []
        word_frequency = dict()
        for i in range(1, len(parts)):
            docs.append(parts[i])
            for w in parts[i].split(' '):
                try:
                    word_frequency[w] += 1
                except:
                    word_frequency[w] = 1

        #for item in word_frequency:
        #    word_frequency[item] = 1
        #print word_frequency
        word2prob(parts[0], docs, word_frequency)

    #test()
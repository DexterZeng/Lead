from sklearn.metrics.pairwise import cosine_similarity
import numpy
import math

def cosine_sim(v1, v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy/ math.sqrt(sumxx * sumyy)

# load embeddings
#f = open('/home/weixin/PycharmProjects/embedding/1000/trans_cE.txt')
#f=open('/home/weixin/Downloads/skip-gram-pytorch-master/entity/embed_en_120w_128.txt',)
f=open('/home/weixin/Downloads/skip-gram-pytorch-master/entity/RPM/embed_20_b2048_top50_100w.txt',)
f.readline()
all_embeddings=[]
all_words=[]
word2id=dict()
for i,line in enumerate(f):
    print (i)
    if i == 0: continue
    line=line.strip().split('\t')
    word = line[0]
    embedding=[float(x) for x in line[1].split(' ')]
    if len(embedding)==100:
        all_embeddings.append(embedding)
        all_words.append(word)
        word2id[word]=i
    else:
        print ('no')
all_embeddings=numpy.array(all_embeddings)

# load datasets and generate top-related entities!
infile = open('./Orig/Query.txt')
outfile = open('./Orig/ce30.txt', 'w')
for line in infile:
    query = line.strip()
    #if query == '/wiki/aries%20%28constellation%29':
    print(query)
    try:
        wid = word2id[query]
    except:
        print('Cannot find this word')
        continue
    embedding = all_embeddings[wid - 1:wid]
    # print(embedding)
    d = cosine_similarity(embedding, all_embeddings)[0]
    d = zip(all_words, d)
    d = sorted(d, key=lambda x: x[1], reverse=True)
    #top20 = d[0:31]

    #####################
    top = d[1:1001] # in the form of ('/wiki/...', 0.9)
    top20 = []
    top20score = []
    for ite in top:
        if ite[1] not in top20score and ite[1] <= 0.99:
            top20.append(ite)
            top20score.append(ite[1])
        if len(top20) >= 30:
            break

    print(top20)

    outfile.write(query.split('/')[-1] + '\t')
    for item in top20:
        outfile.write(item[0].split('/')[-1] + '\t')
    outfile.write('\n')
    outfile.flush()
    
    
    '''
    all_score = 0
    for i in range(0, len(top5)):
        pair_a = top5[i]
        for j in range(i+1, len(top5)):
            pair_b = top5[j]
            ## CAL
            word_a, score_a = pair_a[0], pair_a[1]
            word_b, score_b = pair_b[0], pair_b[1]
            wid_a = word2id[word_a]
            wid_b = word2id[word_b]
            embed_a = all_embeddings[wid_a - 1, :].tolist()
            embed_b = all_embeddings[wid_b - 1, :].tolist()
            sim = cosine_sim(embed_a, embed_b)
            print(word_a + '\t' + word_b + '\t' + str(sim))
            all_score += score_a * score_b * math.exp(-sim)
    '''



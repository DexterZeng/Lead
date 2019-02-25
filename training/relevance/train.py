import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as Func
from torch.optim.lr_scheduler import StepLR
import time

from inputdata_opt import Options, scorefunction
from model import skipgram



class word2vec:
  def __init__(self, inputfile, vocabulary_size=1200000, embedding_dim=300, epoch_num=20, batch_size=2048, windows_size=5,neg_sample_num=5):
    self.op = Options(inputfile, vocabulary_size)
    self.embedding_dim = embedding_dim
    self.windows_size = windows_size
    self.vocabulary_size = vocabulary_size
    self.batch_size = batch_size
    self.epoch_num = epoch_num
    self.neg_sample_num = neg_sample_num


  def train(self):
    model = skipgram(self.vocabulary_size, self.embedding_dim)
    if torch.cuda.is_available():
      print("CUDA available")
      model.cuda()
    else:
      print("CUDA NOT available")
    controler = 0
    optimizer = optim.SGD(model.parameters(),lr=0.2)
    #for epoch in range(self.epoch_num):
    for epoch in range(self.epoch_num):
      start = time.time()     
      self.op.process = True
      batch_num = 0
      batch_new = 0

      while self.op.process:
        batch_data, neg_v = self.op.generate_batch(self.batch_size, self.neg_sample_num)
        pos_u = [pair[0] for pair in batch_data]
        pos_v = [pair[1] for pair in batch_data]

        length = []
        for i in map(len,pos_u):
            length.append(i)
        length = torch.LongTensor(length)
        data_tensor = Variable(torch.zeros((len(pos_u), length.max()))).long()
        for idx, (seq, datalen) in enumerate(zip(pos_u, length)):
            data_tensor[idx, :datalen] = torch.LongTensor(seq)

        pos_u = data_tensor
        pos_v = Variable(torch.LongTensor(pos_v))
        neg_v = Variable(torch.LongTensor(neg_v))

        length = length.expand(self.embedding_dim,self.batch_size).transpose(0,1)
        length = Variable(length).float()


        if torch.cuda.is_available():
          pos_u = pos_u.cuda()
          pos_v = pos_v.cuda()
          neg_v = neg_v.cuda()
          length = length.cuda()

        optimizer.zero_grad()
        loss = model.forward(pos_u, pos_v, neg_v, length, self.embedding_dim)

        loss.backward()
   
        optimizer.step()

        if batch_num%2000 == 0:
          end = time.time()
          word_embeddings = model.input_embeddings()
          sp1, sp2, num = scorefunction(word_embeddings)
          print('eporch,batch=%2d %5d: sp=%1.3f %1.3f %3d pair/sec = %4.2f loss=%4.3f\r'%(epoch, batch_num, sp1, sp2, num, (batch_num-batch_new)*self.batch_size/(end-start),loss.data[0])
                , end="")
          batch_new = batch_num
          start = time.time()
        batch_num = batch_num + 1 
      print()
      if epoch == 10: model.save_embedding('embed_10_b2048_top50t3_120w.txt', self.op.id2word)
    print("Optimization Finished!")
    model.save_embedding('embed_20_b2048_top50t3_120w.txt', self.op.id2word)

  
#if __name__ == '__main__':
  #wc= word2vec('/home/weixin/Downloads/word2vec_pytorch-master/Wiki_ent_m.txt')
#wc= word2vec('/home/weixin/Downloads/word2vec_pytorch-master/relevance/query_anno/100_top200/top100.txt')
wc= word2vec('C2top50_t315.txt')
wc.train()
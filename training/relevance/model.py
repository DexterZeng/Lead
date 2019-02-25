import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from inputdata import Options, scorefunction

class skipgram(nn.Module):
  def __init__(self, vocab_size, embedding_dim):
    super(skipgram, self).__init__()
    self.u_embeddings = nn.Embedding(vocab_size, embedding_dim, padding_idx=0,sparse=True)
    self.v_embeddings = nn.Embedding(vocab_size, embedding_dim, sparse=True) 
    self.embedding_dim = embedding_dim
    self.init_emb()
  def init_emb(self):
    initrange = 0.5 / self.embedding_dim
    self.v_embeddings.weight.data.uniform_(-initrange, initrange)
    #self.u_embeddings.weight.data.uniform_(-0, 0)
  def forward(self, pos_u, pos_v, neg_v, length, embedding_dim):

    emb_u = self.u_embeddings(pos_u)
    emb_u = torch.sum(emb_u,1).squeeze()
    emb_u = torch.div(emb_u, length)
    emb_v = self.v_embeddings(pos_v)

    score = torch.mul(emb_u, emb_v)
    score = torch.sum(score, dim=1)
    score = F.logsigmoid(score)
    
    neg_emb_v = self.v_embeddings(neg_v)
    neg_score = torch.bmm(neg_emb_v, emb_u.unsqueeze(2)).squeeze()
    neg_score = F.logsigmoid(-1 * neg_score).squeeze()

    return -1*(torch.sum(score)+torch.sum(neg_score))/embedding_dim # batch_size

  def input_embeddings(self):
    return self.v_embeddings.weight.data.cpu().numpy()

  def save_embedding(self, file_name, id2word):
    embeds = self.v_embeddings.weight.data
    fo = open(file_name, 'w')
    for idx in range(len(id2word)):
      word = id2word[idx]
      embedding = embeds[idx]
      embed =''
      for em in embedding:
        embed = embed + str(em) + ' '
      embed = embed[:-1]
      fo.write(word+'\t'+embed+'\n')
    fo.close()
# Lead
This is the source code for [1].

Directory trainDataGen includes the code of generating training dataset for relevance-based entity embedding. The queries are AOL user query, while the documents are from Wikipedia dump. The documents are both indexed and retrieved by Lucene. By using relDocDen.java, the relevant documents for each query can be obtained. Only entities will be kept. Then by feeding the queries and their relevant document entities to trainGen.py, the training set can thus be obtained.

Directory training includes the codes for generating relevance-based entity embeddings and also w2v-based entity embeddings. 

Directory DER includes the codes/data for evaluation via Diversified Entity Recommendation (DER). relEntGen.py aims to generate related entities for target entity according to entity embedding similarity. eva.py generates quality score for the top-related entities.

[1]	Weixin Zeng, Xiang Zhao, Jiuyang Tang, Jinzhi Liao, Chang-Dong Wang: Relevance-based Entity Embedding. To appear in 24th International Conference on Database Systems for Advanced Applications (DASFAA), 2019.

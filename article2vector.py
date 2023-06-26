#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### 提取文档为特定特征向量


# In[ ]:


import torch
import pandas as pd
import chardet
from transformers import BertTokenizer, BertModel


# In[ ]:


# Load the BERT model and tokenizer
model_name = 'bert-base-uncased'  # You can use different BERT variants based on your requirements
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Load the articles from the CSV file
csv_file = '/home/asiancary/Desktop/nlp/all_original_uk.csv'  # Replace with the path to your CSV file

# Detect the encoding of the CSV file using chardet
with open(csv_file, 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']

df = pd.read_csv(csv_file,encoding=encoding)

# Extract the article texts from the DataFrame
articles = df['article'].tolist()

# Tokenize and encode the articles
encoded_articles = tokenizer.batch_encode_plus(
    articles,
    padding=True,
    truncation=True,
    max_length=512,  # Specify the maximum length of the encoded sequences
    return_tensors='pt'
)

# Pass the encoded sequences through BERT to get the feature vectors
with torch.no_grad():
    model_outputs = model(
        input_ids=encoded_articles['input_ids'],
        attention_mask=encoded_articles['attention_mask']
    )

# Extract the feature vectors for each article
feature_vectors = model_outputs[0][:, 0, :].numpy()  # Take the first token's representation (CLS token) as the feature vector

# Save the feature vectors in a new column in the DataFrame
df['feature_vector'] = feature_vectors.tolist()

# Save the updated DataFrame to a new CSV file
output_csv_file = '/home/asiancary/Desktop/nlp/articles_with_features.csv'  # Replace with the desired output file path
df.to_csv(output_csv_file, index=False)


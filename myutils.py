# -*- coding: utf-8 -*-


import urllib3
import os
import re
import string
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from io import BytesIO
from zipfile import ZipFile
from nltk.corpus import stopwords


def clean_doc(doc):
    stop_words = set(stopwords.words('english'))
    
    # Lowercase
    doc = doc.lower()
    # Remove numbers
    #doc = re.sub(r"[0-9]+", "", doc)
    # Split in tokens
    tokens = doc.split()
    # Remove Stopwords
    tokens = [w for w in tokens if not w in stop_words]
    # Remove punctuation
    tokens = [w.translate(str.maketrans('', '', string.punctuation)) for w in tokens]
    # Tokens with less then two characters will be ignored
    #tokens = [word for word in tokens if len(word) > 1]
    return ' '.join(tokens)

def clean_doc_HAN(doc):

    stop_words = set(stopwords.words('english'))
    
    # Lowercase
    doc = doc.lower()
    # Remove numbers
    #doc = re.sub(r"[0-9]+", "", doc)
    # Split in tokens
    sentences = doc.split('.')
    senten=[]
    
    # Remove Stopwords
    for s in sentences:
        sentence = ''
        now_sen = s.strip().split()
        for w in now_sen:
            if w not in stop_words:
                temp = w.translate(str.maketrans('', '', string.punctuation)).replace('br','').strip()
                #print(temp)
                if temp!='':
                    sentence+=temp+' '
        sentence=sentence.strip()
        if sentence!='':
            senten.append(sentence)

    
    #tokens = [w for w in sentences if not w in stop_words]
    # Remove punctuation
    #tokens = [w.translate(str.maketrans('', '', string.punctuation)) for w in tokens]
    # Tokens with less then two characters will be ignored
    #tokens = [word for word in tokens if len(word) > 1]
    return senten




def create_glove_embeddings(embedding_dim, max_num_words, max_seq_length, tokenizer):
    """
    Load and create GloVe embeddings.

    Arguments:
        embedding_dim : Dimension of embeddings (e.g. 50,100,200,300)
        max_num_words : Maximum count of words in vocabulary
        max_seq_length: Maximum length of vector
        tokenizer     : Tokenizer for converting words to integer

    Returns:
        tf.keras.layers.Embedding : Glove embeddings initialized in Keras Embedding-Layer
    """
    
    print("Pretrained GloVe embedding is loading...")
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/glove"):
        print("No previous embeddings found. Will be download required files...")
        os.makedirs("data/glove")
        http = urllib3.PoolManager()
        response = http.request(
            url     = "http://downloads.cs.stanford.edu/nlp/data/glove.6B.zip",
            method  = "GET",
            retries = False
        )

        with ZipFile(BytesIO(response.data)) as myzip:
            for f in myzip.infolist():
                with open(f"data/glove/{f.filename}", "wb") as outfile:
                    outfile.write(myzip.open(f.filename).read())
                    
        print("Download of GloVe embeddings finished.")

    embeddings_index = {}
    f = open(f"data/glove/glove.6B.{embedding_dim}d.txt",encoding='utf8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    
    print(f"Found {len(embeddings_index)} word vectors in GloVe embedding\n")

    embedding_matrix = np.zeros((max_num_words, embedding_dim))

    for word, i in tokenizer.word_index.items():
        if i >= max_num_words:
            continue
        
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return tf.keras.layers.Embedding(
        input_dim    = max_num_words,
        output_dim   = embedding_dim,
        input_length = max_seq_length,
        weights      = [embedding_matrix],
        trainable    = True,
        name         = "word_embedding"
    )


def create_glove_embeddings_HAN(embedding_dim):
    """
    Load and create GloVe embeddings.

    Arguments:
        embedding_dim : Dimension of embeddings (e.g. 50,100,200,300)

    Returns:
        tf.keras.layers.Embedding : Glove embeddings initialized in Keras Embedding-Layer
    """
    
    print("Pretrained GloVe embedding is loading...")
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("data/glove"):
        print("No previous embeddings found. Will be download required files...")
        os.makedirs("data/glove")
        http = urllib3.PoolManager()
        response = http.request(
            url     = "http://downloads.cs.stanford.edu/nlp/data/glove.6B.zip",
            method  = "GET",
            retries = False
        )

        with ZipFile(BytesIO(response.data)) as myzip:
            for f in myzip.infolist():
                with open(f"data/glove/{f.filename}", "wb") as outfile:
                    outfile.write(myzip.open(f.filename).read())
                    
        print("Download of GloVe embeddings finished.")

    embeddings_index = {}
    f = open(f"data/glove/glove.6B.{embedding_dim}d.txt",encoding='utf8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    
    print(f"Found {len(embeddings_index)} word vectors in GloVe embedding\n")


    return embeddings_index


def rule_based_classification(dataset,class_result):
    posi_list=['good','excellent','brillant','interesting','exiciting']
    negative = ['awful','bad','worse','boring','worst','terrible','shit']
    result = []
    acc = 0
    for i,da in enumerate(dataset):
        for j in da.split():
            if da in posi_list:
                if class_result[i]!=1:
                    result.append(False)
                    acc += 1
                else:
                    result.append(True)           
            elif da in negative:
                if class_result[i]!=0:
                    result.append(False)
                    acc += 1
                else:
                    result.append(True)
                
    rr = acc/len(dataset)
    return rr


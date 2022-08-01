from typing import List, Any
from random import random
import math
# preprocessing: lowering and splitting
def preprocessing(text):
    text = text.lower()
    k = 0
    j = 0
    while k != 1:
        if (not(text[j].isalnum()) and (text[j] != ' ')):
            b = list(text)
            b.insert(j, ' ')
            b.insert(j+2, ' ')
            text = (''.join(map(str, b)))
            j += 2
        j +=1
        if (j == len(text)):
            break  
    return text

#tokenization: getting stuff together
def tokenization(text):
    q = []
    b = list(text)
    b.insert(0, ' ')
    text = (''.join(map(str, b)))
    for i in range(len(text)):
        if (text[i] == ' '):
            j = i
            w = []
            while (j < len(text)) and (text[j] == ' '):
                j += 1
            while (j < len(text)) and (text[j] != ' '):
                w.append(text[j])
                j +=1
            q.append(''.join(map(str, w)))
    if (q == []):
        q.append(text)
    text = q 
    return text

# dictionaries: counting words in all textes
def count_words(a):
    q = {}
    w = {}
    for i in range(len(a)):
        q.update(w.fromkeys(a[i], 0))
    for i in q:
        for j in range(len(a)):
            if(i in a[j]):
                q[i] += 1
    return q

# probability of the all word in the vocabulary 
def probability(text, d, amount, cl_p):
    p = 0
    for i in range(len(text)):
        if(text[i] in d):
            p += math.log((d[text[i]]+1)/(amount+amount))
        else:
            p += math.log(1/(amount+amount))
    p += math.log(cl_p)
    return p

# add functions have finished
    
def count_labels(labels: List):
    return {
        unique_label: sum(1 for label in labels if label == unique_label)
        for unique_label in set(labels)
    }

def train(
        train_texts: List[str],
        train_labels: List[str],
        pretrain_params: Any = None) -> Any:
    """
    Trains classifier on the given train set represented as parallel lists of texts and corresponding labels.
    :param train_texts: a list of texts (str objects), one str per example
    :param train_labels: a list of labels, one label per example
    :param pretrain_params: parameters that were learned at the pretrain step
    :return: learnt parameters, or any object you like (it will be passed to the classify function)
    """

    train_texts_neg = []
    train_texts_pos = []

    text_update_1 = []
    print(1) #proverka
    # 1st run:
    for i in range(len(train_texts)):
        # splitting numbers and letters from other symbols + get lowercase
        text_update_1 = preprocessing(train_texts[i]) 
        text_update_1 = tokenization(text_update_1)
        # separating 'neg' and 'pos'
        if (train_labels[i] == 'neg'):
            train_texts_neg.append(text_update_1)
            #train_texts_neg_split.append(text_update_1)
        else:
            train_texts_pos.append(text_update_1) 
            #train_texts_pos_split.append(text_update_1)
    print(2) #proverka                
    pos_amount = len(train_texts_pos) # amount of documents in positive class
    neg_amount = len(train_texts_neg) # amount of documents in negative class
    doc_amount = len(train_texts) # amount of documents in train sample
    
    pos_probability = pos_amount / doc_amount # probability of positive class
    neg_probability = neg_amount / doc_amount # probability of negative class

    print(3) #proverka
    #time for dictionaries 
    dictionary_pos = count_words(train_texts_pos)
    print(4) #proverka
    dictionary_neg = count_words(train_texts_neg)

    return {
        'pos_probability' : pos_probability, 'neg_probability' : neg_probability, 
        'pos_dict' :dictionary_pos, 'neg_dict' :dictionary_neg, 'pos_amount' :pos_amount,
        'neg_amount' : neg_amount
    }
    
            
def pretrain(texts_list: List[List[str]]) -> Any:
    """
    Pretrain classifier on unlabeled texts. If your classifier cannot train on unlabeled data, skip this.
    :param texts_list: a list of list of texts (str objects), one str per example.
        It might be several sets of texts, for example, train and unlabeled sets.
    :return: learnt parameters, or any object you like (it will be passed to the train function)
    """
    # ############################ PUT YOUR CODE HERE #######################################
    return None


def classify(texts: List[str], params: Any) -> List[str]:
    """
    Classify texts given previously learnt parameters.
    :param texts: texts to classify
    :param params: parameters received from train function
    :return: list of labels corresponding to the given list of texts
    """
    print(5) #proverka   
    pos_probability = params['pos_probability']
    neg_probability = params['neg_probability']
    dictionary_pos = params['pos_dict']
    dictionary_neg = params['neg_dict']
    pos_amount = params['pos_amount']   
    neg_amount = params['neg_amount']  
    texts_labels = []
    for i in range(len(texts)):
        text_i = preprocessing(texts[i])
        text_i = tokenization(text_i)
        s_pos = probability(text_i, dictionary_pos, pos_amount, pos_probability)
        s_neg = probability(text_i, dictionary_neg, neg_amount, neg_probability)
        if (s_pos >= s_neg):
            texts_labels.append('pos')
        else:
            texts_labels.append('neg')
    return texts_labels

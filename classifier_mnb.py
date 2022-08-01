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
    t = 0
    j_n = 0
    j_k = len(a)
    i = 0
    while t != 1:
        q[a[i]] = a.count(a[i])
        j_n += a.count(a[i])
        k = 0
        copy = a[i]
        while k != 1:
            try:
                a.remove(copy)
            except:
                k = 1
        if (j_n == j_k):
            t = 1    
    return q

#amount of words in each class
def word_sum(d):
    t = 0
    for i in d:
        t += d[i]
    return t

#counting amount of unic words in training sample
def dict_addition(d1, d2):
    s = len(d1)
    for i in d2:
        if (not(i in d1)): s += 1
    return s  
   
# probability of the all word in the vocabulary 
def probability(text, d, amount, voc, class_prob):
    prob = 0
    for i in range(len(text)):
        if (text[i] in d):
            kol = d[text[i]]
        else:
            kol = 0
        prob += math.log((1+kol)/(voc+amount))
        
    prob += math.log(class_prob)
    return prob

# added functions have finished
    
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
    
    # 1st run:
    for i in range(len(train_texts)):
        # splitting numbers and letters from other symbols + get lowercase
        text_update_1 = preprocessing(train_texts[i]) 
        # separating 'neg' and 'pos'
        if (train_labels[i] == 'neg'):
            train_texts_neg.append(text_update_1)
        else:
            train_texts_pos.append(text_update_1) 
                    
    pos_amount = len(train_texts_pos) # amount of documents in positive class
    neg_amount = len(train_texts_neg) # amount of documents in negative class
    doc_amount = len(train_texts) # amount of documents in train sample
    
    pos_probability = pos_amount / doc_amount # probability of positive class
    neg_probability = neg_amount / doc_amount # probability of negative class
    
    # making two big lists - join responses
    train_texts_neg = list(' '.join(map(str, train_texts_neg)))
    train_texts_pos = list(' '.join(map(str, train_texts_pos)))
    
    # tokenization of positive responses:          
    train_texts_pos = tokenization(train_texts_pos)
    # tokenization of negative responses:          
    train_texts_neg = tokenization(train_texts_neg)    
    
    #time for dictionaries 
    dictionary_pos = count_words(train_texts_pos)
    dictionary_neg = count_words(train_texts_neg)
    
    #counting size of vocabulary
    vocab = dict_addition(dictionary_pos, dictionary_neg)
    
    #counting amount of words in each class
    word_amount_pos = word_sum(dictionary_pos)
    word_amount_neg = word_sum(dictionary_neg)
    '''
    # counting the probability of each word in each class
    dictionary_pos_text = probability(dictionary_pos_text, word_amount_pos, vocab)
    dictionary_neg_text = probability(dictionary_neg_text, word_amount_neg, vocab)
    '''  
    return {
        'pos_probability' : pos_probability, 'neg_probability' : neg_probability, 
        'pos_dict' :dictionary_pos, 'neg_dict' :dictionary_neg, 
        'word_a_p': word_amount_pos, 'word_a_n': word_amount_neg, 'voc' : vocab
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
       
    pos_probability = params['pos_probability']
    neg_probability = params['neg_probability']
    dictionary_pos = params['pos_dict_p']
    dictionary_neg = params['neg_dict_p']
    word_a_p = params['word_a_p']
    word_a_n = perams['word_a_n']
    voc_amount = params['voc']
    s_pos = 0
    s_neg = 0
    texts_labels = []
    for i in range(len(texts)):
        text_i = preprocessing(texts[i])
        text_i = tokenization(text_i)
        s_pos = probability(text_i, dictionary_pos, word_a_p, voc_amount, pos_probability)
        s_neg = probability(text_i, dictionary_neg, word_a_n, voc_amount, neg_probability)
        if (s_pos >= s_neg):
            texts_labels[i] = 'pos'
        else:
            texts_labels[i] = 'neg'
    return texts_labels
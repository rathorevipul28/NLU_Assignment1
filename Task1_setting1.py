
# coding: utf-8

# In[1]:


import nltk
import re
import numpy as np
from nltk.corpus import brown

N_grams = 2

def NGram_model(data):
    params = []

    values = list(data.split())
    i = 1
    while i <= N_grams:
        index = 0
        for value in values[:len(values)-(i-1)]:
            params.append(tuple(values[index:index+i]))
            index = index+1
        i = i+1
    return params

def get_token_count():
    count = {}
    length = {}
    for key in brown.categories():
        sentence_vector = brown.sents(categories = key)
        length[key] =  len(sentence_vector)
        for sentence in sentence_vector[:int(length[key] * 0.9)]:
            text = " <s> " + ' '.join(re.compile(r"\w+").findall(' '.join(sentence))).lower() +" </s> "
            params = NGram_model(text)
            for i in params:
                line = ' '.join(i)
                cnt = len(re.findall(" "+line+" ", text))
                if (i not in count) and (cnt <> 0):
                    count[i] = 0
                if cnt <> 0:
                    count[i] += cnt
    return [count, length]

def perplexity(count, length):
    prob = 0.0
    N = 0
    for key in length:
        sentence_vector = brown.sents(categories = key)
        for sentence in sentence_vector[int(length[key] * 0.9):]: #length[key]:int(length[key] + length[key]*0.1)

            text = "<s> " + ' '.join(re.compile(r"\w+").findall(' '.join(sentence))).lower() +" </s>" #[a-zA-Z]
            N += len(text.split()) - 1
            params = NGram_model(text)
            for i in params:
                p = probability(i, count)
                if p > 0:
                    prob += np.log2(p)

    prob = -prob/float(N)
    pp = 2**(prob)
    return pp



def probability(i, count):

    if i in count:
        prob =  count[i]/float(count[i[:(N_grams-1)]])
    else:
        j = 1
        while j < N_grams:
            if j == N_grams-1:
                cnt = 0
                for key in count.iterkeys():
                    if len(key) == 1:
                        cnt += count[key]
                if i[j:] in count:
                    prob = count[i[j:]]/float(cnt)
                else:
                    prob = 1/float(cnt)

            else:
                if i[j:] in count:
                    prob = count[i[j:]]/float(count[i[j:N_grams-1]])
                    break
            j = j + 1
        return prob

def main():
    count, length = get_token_count()
    perplexity_measure = perplexity(count, length)
    print(" The value of perplexity is - ")
    print perplexity_measure

main()


# In[ ]:








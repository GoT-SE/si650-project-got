from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
stopwords = stopwords.words('english')

with open('summary.dat', 'r') as f:
    docs = f.read().split('\n\n')

def clean_text(texts):
  import re
  res = []
  for text in texts:
    text = text.lower()
        
    text = re.sub("\'ve", " have ", text)
    text = re.sub("\'re", " are ", text)
    text = re.sub("n't", " not ", text)
    text = re.sub("\'ll", " will ", text)
    
    text = re.sub("[^A-Za-z0-9\n]", " ", text)
    text = re.sub("\n", " ", text)
    text = text.replace('&', ' and')
    text = text.replace('$', ' dollar')

    text = ' '.join([t for t in text.split(" ") if t not in stopwords])
    
    res.append(text)
  return res

docs = clean_text(docs)

docs

text_vector = TfidfVectorizer(sublinear_tf=True, max_features=50, ngram_range=(1,3), analyzer='word', stop_words='english')
docs_vec = text_vector.fit_transform(docs)
print(text_vector.get_feature_names())

import numpy as np
feature_names = text_vector.get_feature_names()
new_doc = ['Arya, knowing that Nymeria will be punished for injuring the prince, forces the direwolf to flee by throwing a rock at her. She is then taken before the King, who is angered that a minor fracas has become a major incident, with his wife and new Hand blaming one another\'s children. Joffrey offers a false account of the incident, and asks Sansa to confirm it. Put in an impossible position, Sansa refuses to contradict him, enraging Arya. The King decides to let Ned discipline Arya while he will do the same to Joffrey, but Cersei demands that the direwolf be executed. When Nymeria cannot be found, Cersei spitefully requests that Sansa\'s direwolf Lady be killed instead, and Robert acquiesces, upsetting Sansa and further angering Arya. Furious, Eddard attends to the matter himself, passing the Hound arriving with Mycah\'s bloodied corpse. Eddard is shocked and disgusted, and when he asks if the Hound ran Mycah down, the Hound responds "He ran, but not very fast." Eddard kills Lady with a dagger, and hundreds of miles away, Bran awakens.',
           'However, Daenerys seems not to notice it and appears to be unharmed. Drogo-arrives Drogo arrives in Pentos and approves of Daenerys.']
responses = text_vector.transform(new_doc)

features_by_gram = dict()
for f, w in zip(text_vector.get_feature_names(), text_vector.idf_):
    n = len(f.split(' '))
    if n not in features_by_gram:
      features_by_gram[n] = []
    features_by_gram[len(f.split(' '))].append((f, w)) # n-gram

top_n = 6

for gram, features in features_by_gram.items():
    top_features = sorted(features, key=lambda x: x[1], reverse=True)[:top_n]
    top_features = [f[0] for f in top_features]
    print('{}-gram top:'.format(gram), top_features)


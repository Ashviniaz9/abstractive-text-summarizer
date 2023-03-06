import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
text = """Written collaboratively by largely anonymous volunteers, anyone with Internet access and not blocked, can write and make changes to Wikipedia articles (except in limited cases where editing is restricted to prevent disruption or vandalism). Since its creation on January 15, 2001, Wikipedia has grown into the world's largest reference website, attracting over a billion visitors monthly. It currently has more than sixty million articles in more than 300 languages, including 6,626,358 articles in English with 128,978 active contributors in the past month.

The fundamental principles of Wikipedia are summarized in its five pillars. The Wikipedia community has developed many policies and guidelines, but you do not need to be familiar with every one of them before contributing.

Anyone can edit Wikipedia's text, references, and images. What is written is more important than who writes it. The content must conform with Wikipedia's policies, including being verifiable by published sources. Editors' opinions, beliefs, personal experiences, unreviewed research, libelous material, and copyright violations will not remain. Wikipedia's software allows easy reversal of errors, and experienced editors watch and patrol bad edits."""

def summarizer(rawdocs):
    stopwords= list(STOP_WORDS)
    #print(stopwords)
    nlp =spacy.load('en_core_web_sm')
    doc= nlp(rawdocs)
    #print(doc)
    tokens = [token.text for token in doc]
    #print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower()not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] =1
            else:
                word_freq[word.text]+= 1
    #print(word_freq)
    max_freq=max(word_freq.values())
    if word_freq:
     max_freq = max(word_freq.values())
    else:
     max_freq = 0

    #print(max_freq)
    for word in word_freq.keys():
        word_freq[word]= word_freq[word]/max_freq
    # print(word_freq)
    
    sent_tokens = [sent for sent in doc.sents]
    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] =word_freq[word.text]
                else:
                    sent_scores[sent]+= word_freq[word.text]
                    
    select_len = int(len(sent_tokens) * 0.3)

    summary = nlargest(select_len , 
                    sent_scores, key=sent_scores.get) # type: ignore
    #print(summary)
    final_summary =[word.text for word in summary]

    summary = ' ' .join(final_summary)
    #print(text)
    #print(summary)
    #print ( " Length of original text" , len(text.split(' ')))
    #print ( " Length of summary text" , len(summary.split(' ')))
    return summary, doc , len(rawdocs.split(' ')), len(summary.split(' '))  


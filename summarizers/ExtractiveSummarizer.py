from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import pandas as pd
from sentence_transformers import SentenceTransformer


class ExtractiveSummarizer:
    def __init__(self, language = "english"):
        self.language = language
        self.vectorizer = TfidfVectorizer()
        self.stop_words = set(stopwords.words(self.language))
        self.lemmatizer = WordNetLemmatizer()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_wordnet_pos(self, treebank_tag):
        '''
        This function convert Treebank POS tag to WordNet POS tag, in order to perform lemmatization
        '''
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
    
    def lemmatize_sentence(self, sentence):
        '''
        This function return lemmatized sentence, and also remove stopwords
        '''
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)
        lemmatized = [
            self.lemmatizer.lemmatize(word, self.get_wordnet_pos(pos))
            for word, pos in tagged
            if word.lower() not in self.stop_words
        ]
        return ' '.join(lemmatized)
    
    def preprocessing_text(self, sentence, lemmatization = True):
        '''
        This function removes special characters, extra spaces, perform lemmatization (optional), and return lowercase
        '''
        sentence = sentence.lower()
        sentence = re.sub(r'\W+', ' ', sentence)
        sentence = re.sub(r'\s+', ' ', sentence)
        if lemmatization:
            sentence = self.lemmatize_sentence(sentence)
        return sentence

    def summarize_TFIDF_TextRank(self, text, volume='short'):
        '''
        This function preprocessing text, convert sentences to vectors using TF-IDF, compute similarity matrix, use TextRank to find top k sentences.
        param volume = ['short', 'medium', 'long'] correspond to 15%, 25%, and 35% number of orignial sentences
        '''
        assert volume in ['short', 'medium', 'long']
        sentences = sent_tokenize(text)
        top_k_ratio = {
            'short': 0.1,
            'medium': 0.25,
            'long': 0.35
        }
        top_k = max(1, round(len(sentences) * top_k_ratio[volume])) # find number of top k to decide the length of summary

        processed_sentences = [self.preprocessing_text(sentence, lemmatization=True) for sentence in sentences]

        # TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(processed_sentences)

        # Similarity matrix
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # Build graph
        graph = nx.from_numpy_array(similarity_matrix)

        # PageRank
        scores = nx.pagerank(graph)

        ranked_sentences = sorted(((scores[i], i) for i in range(len(sentences))), reverse=True)
        top_sentence_indices = sorted([idx for (_, idx) in ranked_sentences[:top_k]])

        summary = ' '.join([sentences[i] for i in top_sentence_indices])
        print(top_k)
        return summary
            
    def summarize_sentence_embedding(self, text, volume='short'):
        assert volume in ['short', 'medium', 'long']
        sentences = sent_tokenize(text)
        top_k_ratio = {
            'short': 0.1,
            'medium': 0.25,
            'long': 0.5
        }
        top_k = max(1, round(len(sentences) * top_k_ratio[volume]))

        embeddings = self.embedding_model.encode(sentences)
        similarity_matrix = cosine_similarity(embeddings)
        graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(graph)
        ranked_sentences = sorted(((scores[i], i) for i in range(len(sentences))), reverse=True)
        top_sentence_indices = sorted([idx for (_, idx) in ranked_sentences[:top_k]])
        summary = ' '.join([sentences[i] for i in top_sentence_indices])

        return summary

# text = '''
# Artificial Intelligence (AI) is transforming industries. 
# From healthcare to finance, AI tools are being deployed at scale. 
# The future of work is rapidly evolving. 
# AI can automate tasks, but also augment human intelligence. 
# Ethical concerns remain important in AI development. 
# Education systems need to adapt to AI-driven demands.AI can automate tasks, but also augment human intelligence. 
# Ethical concerns remain important in AI development. 
# Education systems need to adapt to AI-driven demands.AI can automate tasks, but also augment human intelligence. 
# Ethical concerns remain important in AI development. 
# Education systems need to adapt to AI-driven demands.
# '''

# t = ExtractiveSummarizer()
# print(t.summarize_TFIDF_TextRank(text, volume='long'))
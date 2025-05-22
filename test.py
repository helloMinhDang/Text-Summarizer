import nltk
from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):
    """
    Convert Treebank POS tags to WordNet POS tags:
    - NLTK’s default pos_tag → Penn Treebank tags
    - WordNetLemmatizer expects wordnet.ADV, .NOUN, .VERB, .ADJ
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        # default to noun if unknown
        return wordnet.NOUN
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def lemmatize_sentence(sentence):
    # 1. Tokenize
    tokens = word_tokenize(sentence)
    # 2. POS-tag
    tagged = pos_tag(tokens)
    print(f'tagged: {tagged}')
    # 3. Lemmatize each token with its WordNet POS
    lemmas = [
        lemmatizer.lemmatize(tok, pos=get_wordnet_pos(tag))
        for tok, tag in tagged
    ]
    return lemmas

# Example
sent = "The striped bats are hanging on their feet and are amazingly beautiful."
print(lemmatize_sentence(sent))
# → ['The', 'striped', 'bat', 'be', 'hang', 'on', 'their', 'foot', 'and', 'be', 'amazingly', 'beautiful', '.']

import torch
import numpy as np
import re
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import py_vncorenlp


# This class also includes POS and NER tagging for both Vietnamese and English texts.
class ExtractiveSummarizer:
    # Load the VnCoreNLP model for word segmentation
    # and the PhoBERT model for sentence embeddings
    def __init__(self, vncorenlp_path: str = 'E:/VnCoreNLP-master'):
        self.rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=vncorenlp_path)
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
        self.model = AutoModel.from_pretrained("vinai/phobert-base-v2", add_pooling_layer=False)
    
    def _segment_sentences(self, raw_text):
        return self.rdrsegmenter.word_segment(raw_text)  # list of segmented sentences

    def _encode_sentence(self, sentence):
        input_ids = torch.tensor([self.tokenizer.encode(sentence, truncation=True, max_length=256)])
        with torch.no_grad():
            outputs = self.model(input_ids)[0]  # last_hidden_state
        embedding = outputs.mean(dim=1)  # [1, hidden_size]
        return embedding.squeeze(0).numpy()  # [hidden_size]

    def _build_similarity_matrix(self, sentence_vectors):
        n = len(sentence_vectors)
        sim_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    sim_matrix[i][j] = cosine_similarity(
                        sentence_vectors[i].reshape(1, -1),
                        sentence_vectors[j].reshape(1, -1)
                    )[0, 0]
        return sim_matrix

    def _clean_segmented_sentence(self, sentence):
        # Clean the segmented sentence to remove _ and extra spaces
        sentence = sentence.replace("_", " ")
        sentence = re.sub(r"\s+([.,!?;:])", r"\1", sentence)
        sentence = re.sub(r'\(\s*([^\(\)]+?)\s*\)', r'(\1)', sentence)
        return sentence

    def summarize(self, raw_text, top_n):
        sentences = self._segment_sentences(raw_text) 
        if len(sentences) == 0:
            return ""

        sentence_vectors = [self._encode_sentence(sent) for sent in sentences]
        sim_matrix = self._build_similarity_matrix(sentence_vectors)

        # PageRank
        nx_graph = nx.from_numpy_array(sim_matrix)
        scores = nx.pagerank(nx_graph)

        # Lấy index gốc của các câu được chọn
        top_sentence_indices = [i for i, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]]

        # Sắp xếp lại theo thứ tự xuất hiện trong văn bản
        top_sentence_indices.sort()
        # Lấy lại câu gốc theo thứ tự đó
        summary_sentences = [sentences[i] for i in top_sentence_indices]

        cleaned_summary = [self._clean_segmented_sentence(s) for s in summary_sentences]
        print(top_n)
        return "\n".join(cleaned_summary)

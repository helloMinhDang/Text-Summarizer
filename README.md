# Text Summarization Project

This is a personal project implementing both **extractive** and **abstractive** text summarization methods.

## Features

- **Extractive Summarization**  
  - Uses **TF-IDF + TextRank** to rank and select the most important sentences.  
  - Uses **Sentence Embedding + TextRank** with embeddings from the pre-trained `all-MiniLM-L6-v2` model for semantic similarity and sentence ranking.

- **Abstractive Summarization**  
  - Uses the pre-trained **BART** model for generating concise and fluent summaries by paraphrasing and compressing the input text.
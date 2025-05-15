from flask import Flask, render_template, request
from langdetect import detect
import docx
import os
from summarizers.AbstractiveSummarizer import AbstractiveSummarizer
from summarizers.ExtractiveSummarizer import ExtractiveSummarizer

# Initialize summarizers
abstractive_summarizer = AbstractiveSummarizer()
extractive_summarizer = ExtractiveSummarizer()

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def detect_language(text):
    lang = detect(text)
    return 'English' if lang == 'en' else 'Vietnamese'

import re

def get_summary_params(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if s]
    sent_count = len(sentences)

    min_ratio, max_ratio = 0.15, 0.30
    min_top_n = max(1, int(sent_count * min_ratio))
    max_top_n = max(min_top_n, int(sent_count * max_ratio))

    word_count = len(re.findall(r'\w+', text))
    avg_sentence_len = word_count / sent_count if sent_count else 20

    min_len = int(min_top_n * avg_sentence_len)
    max_len = int(max_top_n * avg_sentence_len)
    return max_top_n, min_len, max_len

def summarize_text(text, lang):
    top_n, min_len, max_len = get_summary_params(text)

    summaries = {}

    if lang == 'English':
        summaries['abstractive'] = abstractive_summarizer.summarize(
            text, max_length=max_len, min_length=min_len
        )
        summaries['extractive'] = extractive_summarizer.summarize(text, top_n=top_n)
    elif lang == 'Vietnamese':
        summaries['extractive'] = extractive_summarizer.summarize(text, top_n=top_n)

    return summaries

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    text_input = request.form.get('text_input', '').strip()
    uploaded_file = request.files.get('file_input')

    if uploaded_file and uploaded_file.filename != '':
        filename = uploaded_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        if filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            return "Unsupported file format", 400
    else:
        text = text_input

    if not text:
        return "No text provided", 400

    detected_language = detect_language(text)
    text_summary = summarize_text(text, detected_language)
    word_count = len(text.split())

    return render_template(
        'result.html',
        original_text=text,
        detected_language=detected_language,
        text_summary=text_summary,
        word_count=word_count
    )

if __name__ == '__main__':
    app.run(debug=True)

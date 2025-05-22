from flask import Flask, render_template, request
from summarizers.AbstractiveSummarizer import AbstractiveSummarizer
from summarizers.ExtractiveSummarizer import ExtractiveSummarizer

app = Flask(__name__)
abstractive_summarizer = AbstractiveSummarizer()
extractive_summarizer = ExtractiveSummarizer()

@app.route("/", methods=["GET", "POST"])
def index():
    tfidf_summary = ""
    embedding_summary = ""
    abstractive_summary = ""
    input_text = ""
    error = ""
    volume = "medium"

    if request.method == "POST":
        volume_map = {"1": "short", "2": "medium", "3": "long"}
        volume_slider = request.form.get("volume", "2")
        volume = volume_map.get(volume_slider, "medium")
        app.logger.debug(f"slider={volume_slider!r} → volume={volume!r}")
        input_text = request.form.get("text-input", "").strip()
        if not input_text:
            error = "Please enter or upload text to summarize."
        else:
            try:
                tfidf_summary = extractive_summarizer.summarize_TFIDF_TextRank(input_text, volume)
                embedding_summary = extractive_summarizer.summarize_sentence_embedding(input_text, volume)
                abstractive_summary = abstractive_summarizer.summarize(input_text, volume)
            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        input_text=input_text,
        error=error,
        tfidf_summary=tfidf_summary,
        embedding_summary=embedding_summary,
        abstractive_summary=abstractive_summary
    )

if __name__ == "__main__":
    app.run(debug=True)

from transformers import BartForConditionalGeneration, BartTokenizer

class AbstractiveSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)

    def summarize(self, text, max_length=130, min_length=30):
        if not text or not text.strip():
            return "No content to summarize."

        inputs = self.tokenizer.encode(
            text,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        )

        summary_ids = self.model.generate(
            inputs,
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )

        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

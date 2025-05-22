from transformers import BartForConditionalGeneration, BartTokenizer

from transformers import BartTokenizer, BartForConditionalGeneration

class AbstractiveSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)

    def summarize(self, text, volume="short"):
        if not text or not text.strip():
            return "No content to summarize."

        assert volume in ['short', 'medium', 'high'], "Volume must be 'short', 'medium', or 'high'"

        # Encode the input text
        inputs = self.tokenizer.encode(
            text,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        )

        # Get length of original tokenized input
        input_length = inputs.shape[1]

        # Define length ratios for each volume
        length_ratios = {
            'short': 0.1,
            'medium': 0.25,
            'high': 0.35
        }

        # Compute dynamic lengths
        max_length = max(10, int(input_length * length_ratios[volume]))  # at least 10 tokens
        min_length = max(5, int(max_length * 0.6))  # min length = 60% of max length

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


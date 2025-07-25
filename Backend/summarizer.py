from transformers import pipeline

# Load summarization model (T5 or BART)
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def generate_summary_and_actions(transcript):
    print("Generating summary...")

    # Hugging Face models often have a max token limit (~512 tokens)
    # So we truncate if needed
    max_input_length = 1000
    input_text = transcript[:max_input_length]

    # Add prompt for T5 model (if using T5)
    input_with_prompt = "summarize: " + input_text

    summary_output = summarizer(input_with_prompt, max_length=100, min_length=30, do_sample=False)
    summary_text = summary_output[0]['summary_text']

    # Action item extraction – basic method using keyword search
    print("Extracting action items...")
    lines = transcript.split('\n')
    action_keywords = ["need to", "should", "must", "I will", "we will", "let's", "plan to", "assign", "action item"]
    action_items = []

    for line in lines:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in action_keywords):
            action_items.append(line.strip())

    return summary_text.strip(), action_items

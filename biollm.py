from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "ContactDoctor/Bio-Medical-Llama-3-8B"
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe(messages)
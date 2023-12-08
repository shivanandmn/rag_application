from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from llama_index.llms import HuggingFaceLLM

model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
hug_llm = HuggingFaceLLM(model=model, tokenizer=tokenizer)


prompt = \
"""'Answer based on context:\n\nI learned some useful things at Interleaf, though they were mostly about what not to do. I learned that it\'s better for technology companies to be run by product people than sales people (though sales is a real skill and people who are good at it are really good at it), that it leads to bugs when code is edited by too many people, that cheap office space is no bargain if it\'s depressing, that planned meetings are inferior to corridor conversations, that big, bureaucratic customers are a dangerous source of money, and that there\'s not much overlap between conventional office hours and the optimal time for hacking, or conventional offices and the optimal place for it.\n\nBut the most important thing I learned, and which I used in both Viaweb and Y Combinator, is that the low end eats the high end: that it\'s good to be the "entry level" option, even though that will be less prestigious, because if you\'re not, someone else will be, and will squash you against the ceiling. Which in turn means that prestige is a danger sign.\n\nWhat happened at interleaf?'
"""
print(hug_llm.complete(prompt))
breakpoint()
from transformers import pipeline

generator = pipeline(model="openai-community/gpt2")
# generator("I can't believe you did such a ", do_sample=False)

# These parameters will return suggestions, and only the newly created text making it easier for prompting suggestions.
outputs = generator(
    "下文是一个吉林大学毛泽东思想的读书报告论文作业：", num_return_sequences=4, return_full_text=True
)

print(outputs)

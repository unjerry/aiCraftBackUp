from transformers import BloomTokenizerFast, BloomForCausalLM

device = "cuda"
path = "YeungNLP/firefly-1b4"

tokenizer = BloomTokenizerFast.from_pretrained(path)
model = BloomForCausalLM.from_pretrained(path)
model.eval()
model = model.to(device)
text = input("User：")
while True:
    text = "<s>{}</s></s>".format(text)
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    input_ids = input_ids.to(device)
    outputs = model.generate(
        input_ids,
        max_new_tokens=200,
        do_sample=True,
        top_p=0.85,
        temperature=0.35,
        repetition_penalty=1.2,
        eos_token_id=tokenizer.eos_token_id,
    )
    rets = tokenizer.batch_decode(outputs)
    output = rets[0].strip().replace(text, "").replace("</s>", "")
    print("Firefly：{}".format(output))
    text = input("User：")

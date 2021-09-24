from transformers import AutoModelForCausalLM, AutoTokenizer
from nltk.corpus import words
from random import choice
import torch
from utils import clean, true_random_choice
from catfacts import facts

import time
import re
import nltk


nltk.download('words')

torch.cuda.empty_cache()
device = torch.device("cuda") 

model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path="./catfact_model").to(device)
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

generate_count = 0

def get_seed_facts():
    split_facts = facts.split("\n")
    seed_facts = [
        true_random_choice(split_facts),
        true_random_choice(split_facts),
        true_random_choice(split_facts),
        true_random_choice(split_facts),
        true_random_choice(split_facts)
    ]
    return "\n\n".join(seed_facts) + "\n\n"

def get_generated_catfact(text):
    prompt = text + choice(['A', 'Cat', 'Cats', 'According', 'All', 'Approximately', 'During', 'If', 'In', 'Female', 'Male', 'Many', 'Most', 'On', 'Perhaps', 'Relative',
    'Some', 'The', 'There', 'Unlike', 'When', 'While', choice(words.words()).capitalize(), choice(words.words()).capitalize(), choice(words.words()).capitalize()])
    inputs = tokenizer(prompt, add_special_tokens=False, return_tensors="pt")["input_ids"].to(device)

    prompt_length = len(tokenizer.decode(inputs[0]))
    outputs = model.generate(inputs,
        do_sample=True, 
        min_length=64,
        max_length=512,
        top_p=0.8, 
        temperature=1.25)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)[len(text):]

def generate_fact():
    try:
        fact = get_generated_catfact(get_seed_facts())
    except:
        time.sleep(15)
        return generate_fact()


    print(fact)
    if fact.count('.') < 2:
        return generate_fact()

    fact = fact[:fact.find("\n")]
    fact = fact[:fact.rfind(".") + 1]
    fact = clean(fact)

    unwanted_chars = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')

    return fact if fact.find(".") is not None and unwanted_chars.search(
        fact) == None and not any(x in fact.lower() for x in [
            " dog ", " dogs ", " rat ", " rats ", " mouse ", " bitch ", " bitches ", " mice ",
            " shark ", " sharks ", " rabbit"
        ]) and any(x in fact.lower() for x in [
            "cat ", "cats ", "cat.", "cats.", "cats'", "cat's", "kitten", "kitties", "kitty",
            "feline", "lion", "tiger", "cheetah"
        ]) else generate_fact()

new_fact = f"{generate_fact()} #ai #catfacts"

print(new_fact)


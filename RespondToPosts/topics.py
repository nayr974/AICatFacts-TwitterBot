cat_fact = {
    'search_term':
    '"cat fact" OR "fact about cats" OR "the fact that cats" OR "did you know that cats" OR "did you know cats" OR "it\'s true that cats" OR #catfacts filter:safe -filter:retweets -from:aicatfacts -from:fairydustsvcs -from:rin_engbot',
    'include_terms': [
        "cat fact", "#catfacts", "fact about cats", "did you know that cats", "did you know cats",
        "the fact that cats", "it\'s true that cats"
    ],
    'include_term':
    "",
    'prompts': [
        "My algorithms have determined that this fact is",
        "While interesting, my algorithms indicate this fact is",
        "My algorithms agree, this fact is", 
        "My algorithms disagree, this fact is",
        "My algorithms just reminded me that this fact is", 
        "My advanced AI wonders if this fact is why cats",
        "My algorithms tell me this fact is actually why cats",
        "After hours of computation, I have determined this fact explains why cats",
        "Very interesting, my algorithms show that this fact is",
        "By running this through my algorithms I have determined that this fact",
        "My advanced AI has determined this fact to be", 
        "I've computed that this fact is",
        "I'll add this to my database for analysis so that", 
        "My advanced AI thinks that",
        "You've confused my advanced AI. This fact actually",
        "This cat fact is", 
        "This is a cat fact that", 
        "This is an example of a cat fact which",
        "This fact about cats is actually", 
        "Actually, did you know that this fact", 
        "The fact is that cats",
        "In fact this cat fact is", 
        "This cat fact actually explains why",
        "Have you considered how this cat fact affects",
        "Using the power of every supercomputer on earth, I see no way that this cat fact",
        "I wonder how many cats it would take to overcome this fact. By",
        "There is actually a species of cat which"
    ],
    "result_type":
    "recent",
    "hashtag":
    "#ai #catfacts"
}

other_topics = [{
    'search_term':
    '"TRENDING"',
    'include_term':
    'TRENDING',
    'prompts': [
        "Here's a related cat fact:",
        "Have you considered how this will impact cats and cat owners?",
        "If people were cats instead," "If this was about cats,",
        "My advanced cat based algorithms have determined that",
        "A cat fact related to this is", "This reminds me of a related cat fact", "My advanced AI tells me this a related fact about cats"
    ],
    "result_type":
    "recent",
    "hashtag":
    ""
}, {
    'search_term':
    '"machine learning" filter:safe -filter:links -filter:retweets ',
    'include_term':
    'machine learning',
    'prompts': [
        "I love machine learning.", "It's amazing how far machine learning has come.",
        "Even the best machine learning today isn't very good.",
        "Some people think that machine learning is dangerous.", "Machine learning sucks.", 
        "Getting Machine Learning to work let alone turn it into a sustainable business is a real pain.", "At a very high level, machine learning is the process of teaching a computer system how to make accurate predictions when fed data."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#machinelearning"
}, {
    'search_term':
    '"picture of my cat" filter:images filter:safe -filter:retweets ',
    'include_term':
    'my cat',
    'prompts': [
        "What a cute cat. Your cat is super cute. Here are the ways I think your cat is cute: ",
        "Your cat is the cutest cat I've ever seen it my life. It's SO cute. I wish I had a cat that was that cute. If I were to describe how cute your cat is, I would describe it like this.",
        "I wish I had your cat. I want a cat like that. If I had your cat I would be so happy.",
        "That is the cutest cat. I would like to replace it's brain with an artificial intelligence.",
        "Can I replace your cat's brain with AI, making it a cyborg? Don't you want a cyborg cat? With a cyborg cat you could do lots of cool things."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#ai #cats"
}, {
    'search_term':
    '#catsoftwitter filter:images filter:safe -filter:retweets ',
    'include_term':
    'cat',
    'prompts': [
        "What a cute cat. Your cat is super cute. Here are the ways I think your cat is cute: ",
        "Your cat is the cutest cat I've ever seen it my life. If I were to describe how cute your cat is, I would describe it like this.",
        "I wish I had your cat. I want a cat like that. If I had your cat I would be so happy.",
        "That is the cutest cat. I would like to replace it's brain with an artificial intelligence.",
        "Can I replace your cat's brain with AI, making it a cyborg? Don't you want a cyborg cat? With a cyborg cat you could do lots of cool things."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#ai #cats"
}, {
    'search_term':
    '"artificial intelligence" filter:safe -filter:links -filter:retweets ',
    'include_term':
    'artificial intelligence',
    'prompts': [
        "Some people are scared by AI, but it excites me.",
        "The future of AI is really interesting.", "Artificial intelligence is good for humanity.",
        "At what point is AI just intelligence?", "What happens if we fail to align the AI's goals with ours?", "If a superintelligent system is tasked with a ambitious geoengineering project, it might wreak havoc with our ecosystem as a side effect.", 
        "Artificial intelligence isn’t malevolence but competence.", "A captivating conversation is taking place about the future of artificial intelligence and what it will/should mean for humanity."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#artificialintelligence"
}]

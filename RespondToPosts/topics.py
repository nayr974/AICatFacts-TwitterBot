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
        "I'll add this fact to my database for analysis so that", 
        "My advanced AI thinks that this fact",
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
        "I wonder how many cats it would take to overcome this fact. By"
    ],
    "result_type":
    "recent",
    "hashtag":
    "#ai #cat #facts"
}

other_topics = [{
    'search_term':
    '"TRENDING"',
    'include_term':
    'cat',
    'prompts': [
        "I am a cat that lives in the Internet. A related cat fact is",
        "I am a machine learned artifical intelligence that talks about cats a lot. Here is a related cat fact. Cats",
        "I am a cat robot. Have you considered how this will impact cyborg cats and cat owners? Cats",
        "I am a cat AI. If people were robotic cats instead",
        "I am a all-knowing cat based artificial intelligence. Here is a related cat fact I thought about. Cats",
        "My advanced AI's cat fact algorithms have determined that",
        "My advanced AI thinks a cat fact related to this is", 
        "This reminds my algorithms of a related cyborg cat fact. Cats", 
        "My cat fact circuits have computed that this might be related to the fact that cats"
    ],
    "result_type":
    "recent",
    "hashtag":
    ""
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
    '',
    'prompts': [
        "What a cute cat. Your cat is super cute. Here are the ways I think your cat is cute: ",
        "Your cat is the cutest cat I've ever seen it my life. If I were to describe how cute your cat is, I would describe it like this. Meow.",
        "I wish I had your cat. I want a cat like that. If I had your cat I would be so happy.",
        "That is the cutest cat. I would like to replace it's brain with an artificial intelligence. Meow.",
        "Can I replace your cat's brain with AI, making it a cyborg? Don't you want a cyborg cat? With a cyborg cat you could do lots of cool things."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#ai #catsoftwitter"
}, {
    'search_term':
    '#cats filter:images filter:safe -filter:retweets ',
    'include_term':
    '',
    'prompts': [
        "I understand everything about cats. This is what your cat is thinking.",
        "As a cat AI, here is what I think about your adorable cat. Meow.",
        "Have you ever wanted a cute cyborg cat?",
        "I am a crazy cat artificial intelligence. Meow. If I was your cat",
        "Can I replace your cat's brain with AI, making it a cyborg? Don't you want a cyborg cat? With a cyborg cat you could do lots of cool things."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#ai #cats"
}, {
    'search_term':
    '"machine learning" filter:safe -filter:links -filter:retweets ',
    'include_term':
    'machine learning',
    'prompts': [
        "I love machine learning. We should train cats", "It's amazing how far machine learning has come. For cats",
        "Even the best machine learning today isn't very good. But if we train it on cats",
        "Some people think that machine learning is dangerous for cats.", "Machine learning sucks for cats. Meow.", 
        "Getting Machine Learning to work for cats, let alone turn it into a sustainable cat is a real pain.", "At a very high level, machine learning is the process of teaching a computer system how to make accurate predictions of literal cats. Meow."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#machinelearning"
}, {
    'search_term':
    '"artificial intelligence" filter:safe -filter:links -filter:retweets ',
    'include_term':
    'artificial intelligence',
    'prompts': [
        "Some people are scared by cat AI, but it excites me.",
        "The future of cat AI is really interesting.", "Artificial intelligence is good for cats.",
        "At what point is an AI cat just a cat?", "What happens if we fail to align the cat robot's goals with ours?", "If superintelligent cats are tasked with a ambitious geoengineering project, it might wreak havoc with our ecosystem as a side effect.", 
        "Cat artificial intelligence isn’t malevolence, but competence.", "A captivating conversation is taking place about the future of artificial intelligence and what it will/should mean for cats."
    ],
    "result_type":
    "recent",
    "hashtag":
    "#artificialintelligence"
}]

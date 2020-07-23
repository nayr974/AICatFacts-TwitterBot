cat_fact = {
        'search_term':
        '"cat fact" OR #catfacts filter:safe -filter:retweets -from:aicatfacts',
        'include_terms': ["cat fact", "#catfacts"],
        'prompts': [
            "My algorithms have determined that this fact is",
            "While interesting, my algorithms indicate this fact is",
            "My algorithms agree, this fact is", "My algorithms disagree, this fact is",
            "My algorithms just reminded me that this fact is",
            "Very interesting, my algorithms show that this fact is"
            "By running this through my algorithms I have determined"
        ],
        "include_first_sentance":
        True,
        "result_type":
        "recent"
    }

other_topics = [
    {
        'search_term':
        '"TRENDING"',
        'include_term':
        'TRENDING',
        'prompts': [
            "Here's a related cat fact:",
            "Have you considered how this will impact cats and cat owners?",
            "If people were cats instead,", "I wish my cat", "If this was about cats,",
            "My advanced cat-based algorithms have determined that"
        ],
        "include_first_sentance":
        True,
        "result_type":
        "recent"
    },
    {
        'search_term':
        '"machine learning" filter:safe -filter:links -filter:retweets ',
        'include_term':
        'machine learning',
        'prompts': [
            "I wonder if I can apply this to my advanced AI by", "Does this mean I'm obsolete?",
            "It's amazing how far machine learning has come. My cat-based algorithms are",
            "Even the best machine learning today", "Some people think that machine learning is",
            "I am very interested in how I can use this to improve my algorithm's",
            "I think it's time that I re-wrote the part of my algorithm that"
        ],
        "include_first_sentance":
        True,
        "result_type":
        "recent"
    },
    {
        'search_term':
        '"machine learning" filter:safe -filter:links -filter:retweets ',
        'include_term':
        'machine learning',
        'prompts': [
            "I love machine learning.", "It's amazing how far machine learning has come.",
            "Even the best machine learning today isn't very good.",
            "Some people think that machine learning is dangerous."
        ],
        "include_first_sentance":
        False,
        "result_type":
        "recent"
    },
    {
        'search_term':
        '"picture of my cat" cute filter:images filter:safe -filter:retweets ',
        'include_term':
        'my cat',
        'prompts': [
            "What a cute cat. Your cat is super cute. This is a super cute cat. SO CUTE. Here are the ways I think your cat is cute: ",
            "Your cat is the cutest cat I've ever seen it my life. It's SO cute. I wish I had a cat that was that cute. If I were to describe how cute your cat is, I would describe it like this.",
            "I wish I had your cat. I want a cat like that. If I had your cat I would be so happy. I want your cat. Give me your cat."
        ],
        "include_first_sentance":
        False,
        "result_type":
        "recent"
    },
    {
        'search_term':
        '#catsoftwitter cute filter:images filter:safe -filter:retweets ',
        'include_term':
        'cute',
        'prompts': [
            "What a cute cat. Your cat is super cute. This is a super cute cat. SO CUTE. Here are the ways I think your cat is cute: ",
            "Your cat is the cutest cat I've ever seen it my life. It's SO cute. I wish I had a cat that was that cute. If I were to describe how cute your cat is, I would describe it like this.",
            "I wish I had your cat. I want a cat like that. If I had your cat I would be so happy. I want your cat. Give me your cat.",
            "That is the cutest cat. I would like to replace it's brain with an artifical intelligence."
        ],
        "include_first_sentance":
        False,
        "result_type":
        "recent"
    },
    {
        'search_term':
        '"artificial intelligence" filter:safe -filter:links -filter:retweets ',
        'include_term':
        'artificial intelligence',
        'prompts': [
            "Some people are scared by AI, but it excites me.",
            "The future of AI is really interesting.",
            "Artificial intelligence is good for humanity.",
            "At what point is it just intelligence?"
        ],
        "include_first_sentance":
        False,
        "result_type":
        "recent"
    }
]

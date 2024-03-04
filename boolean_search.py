import re
from collections import defaultdict


def read_inverted_index(filepath):
    inverted_index = defaultdict(set)
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ')
            token, pages = parts[0], parts[1:]
            inverted_index[token] = set(pages)
    return inverted_index


def read_lemmas(filepath):
    lemmas = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ')
            lemma, tokens = parts[0], parts[1:]
            for token in tokens:
                lemmas[token] = lemma
    return lemmas


def boolean_search(query, inverted_index, lemmas):
    query = query.upper().replace("AND", "&").replace("OR", "|").replace("NOT", "-")
    tokens = set(re.findall(r'\w+', query))

    for token in tokens:
        if token.lower() in lemmas:
            query = query.replace(token, lemmas[token.lower()].upper())
        token_lower = token.lower()
        if token_lower in inverted_index:
            pages_str = "set([" + ", ".join(inverted_index[token_lower]) + "])"
        else:
            pages_str = "set()"
        query = query.replace(token, pages_str)

    try:
        result = eval(query)
    except SyntaxError:
        return "Invalid query"
    return sorted(list(result))


inverted_index = read_inverted_index('inverted_index.txt')
lemmas = read_lemmas('lemmas.txt')

while True:
    user_query = input("\nEnter your search query: ")

    search_results = boolean_search(user_query, inverted_index, lemmas)
    print(search_results)

import re

def top_3_words(text):
    words = (word.lower() for word in re.findall(r"'*(?=[A-Za-z])[A-Za-z']*", text))
    
    counts_map = {}
    for word in words:
        counts_map[word] = counts_map.get(word, 0) + 1
    
    counts = sorted(counts_map.items(), reverse=True, key=lambda c: c[1])
    return [c[0] for c in counts[:3]]

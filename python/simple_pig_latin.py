def pig_it(text):
    words = text.split()
    pig_latin = []
    
    for word in words:
        if "!" in word or "?" in word:
            pig_latin.append(word)
        else:
            pig_latin.append(word[1:] + word[0] + "ay")
        
    return " ".join(pig_latin)
    
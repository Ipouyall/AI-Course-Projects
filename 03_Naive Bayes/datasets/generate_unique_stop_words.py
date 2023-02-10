import parsivar as wp
import hazm
import re


def read_base_words():
    with open('total-stop-words.txt', 'r', encoding='utf-8') as f:
        base_words = f.read().splitlines()
    return set(base_words)

def normalize_words(words):
    normalizer = wp.Normalizer()
    return {normalizer.normalize(word) for word in words}

def add_stemmed_words(base_words):
    stem = wp.FindStems().convert_to_stem
    token = wp.Tokenizer().tokenize_words
    base_words = normalize_words(base_words)
    for word in base_words.copy():
        for w in token(word):
            base_words.union(set(stem(word).split('&')))
    return base_words

def save_words(words: set[str]):
    with open('../stop-words.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join('\n'.join(set(words)).replace('\u200c', '').replace('\u200f','') \
            .replace('\u200c', '').replace('\x7f','') \
            .replace('.', '').replace('،', '').replace('؟', '').replace('؛', '') \
            .replace('!', '').replace('?', '').replace('(', '').replace(')', '') \
            .replace('[', '').replace(']', '').replace('{', '').replace('}', '') \
            .replace(':', '').replace(';', '').replace('«', '').replace('»', '') \
            .replace('٪', '').replace('٫', '').replace('٬', '').replace('٭', '') \
            .replace('،', '').replace('؛', '').replace('ٰ', '').replace('ًٔ', '') \
            .replace('ٌٔ', '').replace('ٍٔ', '').replace('َٔ', '').replace('ُٔ', '') \
            .replace('ِٔ', '').replace('ّٔ', '').replace('ْٔ', '').replace('ٔٓ', '') \
            .replace('ٰٔ', '').replace('ٔٔ', '').replace('ٕٔ', '').replace('ٖٔ', '') \
            .replace('ٔٗ', '').replace('ٔ٘', '').replace('ٔٙ', '').replace('ٔٚ', '') \
            .replace('ٔٛ', '').replace('ٜٔ', '').replace('ٔٝ', '').replace('ٔٞ', '') \
            .replace('اً','').replace('اٌ','').replace('اٍ','').replace('اَ','') \
            .replace('اُ','').replace('اِ','').replace('اّ','').replace('اْ','') \
            .replace('آ','').replace('اٰ','').replace('أ','').replace('إ','') \
            .replace('اٖ','').replace('اٗ','').replace('ا٘','').replace('اٙ','') \
            .replace('اٚ','').replace('اٛ','').replace('اٜ','').replace('اٝ','') \
            .replace('اٞ','').splitlines())
                )
        
if __name__ == '__main__':
    base = read_base_words().union(set(hazm.stopwords_list()))
    base_with_stem = add_stemmed_words(base)
    base_with_stem.union(hazm.stopwords_list())
    save_words(base_with_stem)

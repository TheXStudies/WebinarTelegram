from collections import defaultdict
from heapq import nlargest


from natasha import (
    Doc, Segmenter, NewsMorphTagger, NewsEmbedding, NewsSyntaxParser,
    MorphVocab
)


def process_messages(messages):
    embedding = NewsEmbedding()
    morph_vocab = MorphVocab()
    all_lemmas = defaultdict(int)
    for i, msg in enumerate(messages):
        if i == 30:
            break

        doc = Doc(msg['message'])
        doc.segment(Segmenter())
        doc.tag_morph(NewsMorphTagger(embedding))
        doc.parse_syntax(NewsSyntaxParser(embedding))
        for t in doc.tokens:
            if t.pos not in [
                'PUNCT', 'NUM', 'ADP', 'CCONJ',
                'SCONJ', 'PRON', 'ADV', 'PART', 'SYM', 'DET', "ADJ", "AUX", "X"]:
                t.lemmatize(morph_vocab)
                all_lemmas[t.lemma] += 1

    all_lemmas = dict(nlargest(
        30,
        all_lemmas.items(),
        key=lambda lemma_and_count: lemma_and_count[1]
    ))
    for name, ncount in all_lemmas.items():
        print(f"{name}: {ncount}")

    print("finished!")

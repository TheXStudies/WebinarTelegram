from natasha import (
    MorphVocab, Doc, Segmenter, NewsEmbedding,
    NewsMorphTagger, NewsSyntaxParser)
import matplotlib.pylab as plt
import numpy as np
from collections import defaultdict
from heapq import nlargest


def process_messages(messages):
    msg_lengths = np.array([])
    embedding = NewsEmbedding()
    morph_vocab = MorphVocab()
    all_lemmas = defaultdict(int)
    for i, msg in enumerate(messages):
        if i == 40:
            break
        if not msg['message']:
            continue
        msg_lengths = np.append(msg_lengths, len(msg['message']))
        doc = Doc(msg['message'])
        doc.segment(Segmenter())
        doc.tag_morph(NewsMorphTagger(embedding))
        doc.parse_syntax(NewsSyntaxParser(embedding))
        for t in doc.tokens:
            if t.pos not in ['PUNCT', 'NUM', 'ADP', 'CCONJ', 'SCONJ', 'PRON',
                             'ADV', "PART", 'SYM', 'DET', 'ADJ', 'AUX', 'X']:
                t.lemmatize(morph_vocab)
                all_lemmas[t.lemma] += 1

    all_lemmas = dict(nlargest(
        30,
        all_lemmas.items(),
        key=lambda lemma_and_count: lemma_and_count[1]
    ))

    plt.plot(tuple(all_lemmas.keys()), np.array(tuple(all_lemmas.values())))
    plt.show()
    plt.savefig('lemmas_by_authors.png')


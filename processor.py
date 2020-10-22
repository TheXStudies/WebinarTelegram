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
    lemmas_by_authors = defaultdict(lambda: defaultdict(int))
    for i, msg in enumerate(messages):
        if i == 1000:
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
                lemmas_by_authors[msg['author']][t.lemma] += 1
    lemmas_by_authors = dict(
        nlargest(
            16,
            lemmas_by_authors.items(),
            key=lambda author_and_lemmas: sum(author_and_lemmas[1].values())))
    all_lemmas = defaultdict(int)
    for lemmas in lemmas_by_authors.values():
        for lemma, lcount in lemmas.items():
            all_lemmas[lemma] += lcount

    all_lemmas = dict(nlargest(
        30,
        all_lemmas.items(),
        key=lambda lemma_and_count: lemma_and_count[1]
    ))

    plt.interactive(True)
    plt.xticks(rotation=90)
    for author, lemmas in lemmas_by_authors.items():
        plt.plot(all_lemmas.keys(), np.array([lemmas[l] for l in all_lemmas]), label=author)
    plt.show()
    plt.savefig('lemmas_by_authors.png')

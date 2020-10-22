from natasha import (
    Doc, Segmenter, NewsMorphTagger, NewsEmbedding, NewsSyntaxParser,
    MorphVocab
)


def process_messages(messages):
    embedding = NewsEmbedding()
    morph_vocab = MorphVocab()
    for i, msg in enumerate(messages):
        if i == 30:
            break
        print(msg['message'])

        doc = Doc(msg['message'])
        doc.segment(Segmenter())
        doc.tag_morph(NewsMorphTagger(embedding))
        doc.parse_syntax(NewsSyntaxParser(embedding))
        for t in doc.tokens:
            t.lemmatize(morph_vocab)
            print(f"{t.text}: {t.lemma}")

    print("finished!")

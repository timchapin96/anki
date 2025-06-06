import genanki
import random
from jamdict import Jamdict




def createDeck(wordList):
    jam = Jamdict(db_mode=":memory:")
    modelId = random.randrange(1 << 30, 1 << 31)
    deckId = random.randrange(1 << 30, 1 << 31)
    my_model = genanki.Model(
        modelId,
        'Book Vocab Model',
        fields=[
            {'name': 'JPWord'},
            {'name': 'ENWord'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{JPWord}}',
                'afmt': '{{FrontSide}}<hr id="ENWord">{{ENWord}}',
            },
        ]
    )
    my_deck = genanki.Deck(
        deckId,
        'BookName'
    )


    for word in wordList:
        if word.entries:
            print(word)
            first_entry = word.entries[0]
            entry_meaning = str((first_entry.senses[0].gloss))
            if first_entry.kanji_forms:
                entry_kanji = str(first_entry.kanji_forms[0])
                my_note = genanki.Note(
                    model = my_model,
                    fields=[entry_kanji, entry_meaning]
            )
            else:
                entry_kana = str(first_entry.kana_forms[0])
                my_note = genanki.Note(
                    model = my_model,
                    fields=[entry_kana, entry_meaning]
            )
            my_deck.add_note(my_note)

        else:
            print("No entry found")

    genanki.Package(my_deck).write_to_file('output.apkg')

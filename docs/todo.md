### TODO

- Fix: there are still instances of nmod:tmod
- Add PronType and VerbType (verbtype done)
- Add gloss and translation
- Fix: Some converbs are marked 'finite'
        grep '	Mood=Ind|VerbForm=Fin.*advcl' *.conllu

### Open issues question
- Posessive adjectivals - PRON or not
- Where to place apostrophe if word is split at it, e.g., "Ali'ydi"
- What to do data/time numerals (currently Card - similar to EWT)
- POS tag of "special" connectives like "yok ... yok", "ya ... ya":
  should it be CCONJ or keep their usual pos tags?
- If an ADP is dependent of 'mark', should the upostag be changed?
- Fixed candidates
    - hem de
    - ya da
    - bir de
    - tabii ki
    - demek ki
    - yeter ki
    - nasil ki
    - ne zaman

### Done

- Replace POS of ordinal nouns to ADJ

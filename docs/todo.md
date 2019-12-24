### TODO

- Fix: there are still instances of nmod:tmod
- Add PronType and VerbType (verbtype done)
- Add gloss and translation
- Fix: Some converbs are marked 'finite'
        grep '	Mood=Ind|VerbForm=Fin.*advcl' *.conllu
- Revise/rethink the cases of '-si derived' pronouns
- Revise/document `advmod`s of `ADP` (biraz sonra)
- GK14-0190: 'bazen .. bazen' coordination?
- GK21-0080: 'iki iki daha' - is 'daha' adverb?
- değil...
- 'bir kere' should probably not be fixed (see below the list of
  candidates for 'fixed')

### Open issues question
- Do we need `advmod:emph`?  Lemma should tell enough, and the
  relation is not necessarily emphasis.
- Annotate the interal structure of numbers? E.g., [bin [dokuz yüz]
    [seksen dört]]
- 'doğu'/'batı'/'güney'/'kuzey' - NOUN or ADJ?
- Posessive adjectivals - PRON or not
- Where to place apostrophe if word is split at it, e.g., "Ali'ydi"
- What to do data/time numerals (currently Card - similar to EWT)
- POS tag of "special" connectives like "yok ... yok", "ya ... ya":
  should it be CCONJ or keep their usual pos tags?
- If an ADP is dependent of 'mark', should the upostag be changed?
- In some cases 'ki' looks like coordination: GK24-0033
- Fixed candidates
    - hem de
    - ya da
    - bir de
    - tabii ki
    - demek ki
    - yeter ki
    - nasil ki
    - ne zaman
    - bir türlü
    - bir daha
    - bir tek
    - bir de
    - bir arada
    - aşağı yukarı: is this somewhat productive (sağa sola, ele ayağa)?
    - bir kere: probably not. the semantics is transparent, and should
      be parallel to 'iki kere', 'bir tane', 'üç tabak' ...
    - ve de: probably not, but UD does not allow dependents to CCONJ
      (ve). Currently 'de' is attached to the head of the second
      conjunct (GK28-0035).

### Done

- Replace POS of ordinal nouns to ADJ

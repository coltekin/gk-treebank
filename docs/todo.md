### TODO

- Add gloss and translation
- Revise/rethink the cases of '-si derived' pronouns
- Revise/document `advmod`s of `ADP` (biraz sonra)
- GK14-0190: 'bazen .. bazen' coordination?
- GK21-0080: 'iki iki daha' - is 'daha' adverb?
- değil...
- 'bir kere' should probably not be fixed (see below the list of
  candidates for 'fixed')
- Revision/decsion on postpositions derived from nouns: 'ikisinin
  arasında'
- Copula - non-copula analysis of ol-

### Open issues question
- PronType does not really fit in all pronouns and determiners. For
    most determiners. Fitting determiners in Turkish into one of the
    PronType categories does not seem trivial. The same is true for
    pronouns. Currently (2020-05-01) the cases difficult to fit into
    one of UD categories are marked with `PronType=Ind`.
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
- `fixed` candidates
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

- Fix: Some converbs are marked 'finite'
        grep '	Mood=Ind|VerbForm=Fin.*advcl' *.conllu
- Add PronType and VerbType
- Replace POS of ordinal nouns to ADJ
- Fix: there are still instances of nmod:tmod [fixed 2019-10-30]
- Fix: Some converbs are marked 'finite'
        grep '	Mood=Ind|VerbForm=Fin.*advcl' *.conllu
    [fixed 2019-10-30, may need more attention]

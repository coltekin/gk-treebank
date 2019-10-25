---
layout: default
title: Notes
---

This document contains the annotation notes for Turkish grammar book
treebank.
__This document is currently only an unorganized set of notes.__
The treebank described here was the basis for firt [UD annotation
guidelines](http://universaldependencies.org/tr/) for Turkish.
Although the some parts of the annotations may have diverged from the
official UD documentation.


# Notes

## ``obj`` vs. ``obl``

This treebank considers the following cases as _core_ arguments
and uses `obj` relation for them.

- "Bare" objects
~~~ sdparse
Kitap okudum \n Book-NOM read-PAST.1SG (I read books)
obj(okudum, Kitap)
~~~

- Accusative objects 
~~~ sdparse
Kitabı okudum \n Book-ACC read-PAST.1SG (I read the book)
obj(okudum, Kitabı)
~~~

- Bare/accusative elements that are not really objects,
    but occupy an object position
~~~ sdparse
Üç kilometre koştum \n three kilometers run-PAST-1SG (I run three kilometers)
obj(koştum, kilometre)
nummod(kilometre, Üç)
~~~

- Ablative objects indicating 'part of something'
~~~ sdparse
Pastadan yedi \n Cake-ABL eat-PAST-3SG (S/he ate (part) of the cake)
obj(yedi, Pastadan)
~~~

Other arguments (and adjuncts) of verbs are marked considered non-core (``obl``),
This results in different analyses
for sentences like the following where the difference is mostly stylistic.

~~~ sdparse
İçeri girdi \n inside-NOM enter-PAST-3SG (S/he went inside)
obj(girdi, İçeri)
~~~

~~~ sdparse
İçeriye girdi \n inside-DAT enter-PAST-3SG (S/he went inside)
obl(girdi, İçeriye)
~~~

## _-DIr_ suffix attached to temporal expressions

The suffix _-DIr_ attached to temporal expressions,
_Iki yıldır çalışıyor_ 's/he has been working for two years',
has a different function than the "generalizing modality marker"
attached to verbal or nominal predicates,
_Deneme süresi iki yıldır_ 'Trial period is two years'. 

For lack of a better alternative, we currently treat then the same.

~~~ sdparse
Iki yıl -dır çalışıyor
nummod(yıl, Iki)
cop(-dır, yıl)
advcl(çalışıyor, yıl)
~~~

~~~ sdparse
Deneme süresi iki yıl -dır 
nmod(süresi, Deneme)
nummod(yıl, iki)
cop(-dır, yıl)
nsubj:cop(yıl, süresi)
~~~

_-DIr_ in the first case is more like a (morphological) case marker.
We may want to treat it as such.

## Zero derivation

## Pronouns derived from adjectivals

Possessive suffixes attached to adjectivals,
including ``NUM`` and ``DET``, 
derive adposition-like words.

- _yeşil-i daha güzel_ 'the green (one) is prettier'
- _iki-si-ni  bana verir misin?_ 'can you give two (of them) to me?'
- _bazı-lar-ımız otelde kaldı_ 'some (of us) stayed in the hotel'

Currently we treat them as if they are adjectives that are nominalized with zero derivation.
However, there are two issues:

- This hides the ambiguity between two different functions of the
  suffixes, e.g.,  _yeşil-i daha güzel_ can also mean '(of the items
  that belongs to him) the green one is prettier'. This difference
  also exist with other possessive suffixes.
  _Ali senin uzunun_ 'Ali is taller version of you',
  or '(of your people, e.g., basketball players) Ali is the tall one'.
- If a determiner (pro)nomilized this way, it is at odds with UD since
  it becomes head in some cases _politikacıların çoğ-u_ 'most of the politicians''

## TODO

- Instances of dislocated need a revision.
    Current UD guidelines require attaching the 'dislocated' word
    to its parent which does allow identifying the word that corresponds to it.
- _-lArI- in time expressions, like _geceleri_ 
- _duymazlıktan geldi_  the composite suffix _-mAzlIk_ seems to form
      some sort of verbal noun. Current analysis does not look good.
      Another interesting point here is the double negative in
      _duymamazlıktan geldi_
- Some clausal modifiers of nouns are not realy `acl`:
    _üstünlüğünü kanıtlamak amacıyla yapıyor._
- There is a inconsistency between the nominal/adjectivals with and
  without _olarak_. _Ali çayını soğuk içer_ vs. _Ali çayını soğuk olarak içer_ 
- Similar to above: nominal/cluasal modifiers of adjectives:
    _düyaca meşhur_, _inanılmayacak kadar meşhur_.
- A reasonble guideline/test for `compound` verbs.
- Better/consistent analysis for _değil_.
- Annotation of names like _Filiz Hanım_ and _Ahmet Bey_ is not
    consistent.
- _ol_ as verb/aux/cop needs a through revision
- document _gerek_ and _zorunda_. The first can both be verb and noun,
    and the second forms nominal predicates with a (clausal) object.
- document `discourse` use of _ise_ -_ysa_:
    _Kitaplarsa hala kutularda duruyor._
- document the annotation of reflexive pronouns: as in _kendi yaptı
    and _Ali kendi yaptı_.
- The annotation of the subordinate clauses with _gibi_ and _diye_ are unclear:
    are they core arguments?
- Unalysis of (redundant) reflexive: it gets different relations
    in _benim kendim oturacağım_ and _kendim oturacağım_
- Adjectival verbs with no subordinating suffixes like _anlaşılır_
    _görülmüş_ do not have any morphological indication that they are
    subordinate clauses
- document cases of coordination with different types of constituents.
- check/document _felan/falan/filan_

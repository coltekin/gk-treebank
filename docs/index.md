---
layout: default
title: Introduction
---

This page describes the annotation of a Turkish "GB" treebank,
a treebank of grammar-book examples annotated according to
[Universal Dependencies](https://universaldependencies.org/) (UD)
annotation scheme.
The treebank aims to cover a large range of grammatical constructions
in the language with realtively small number of short sentences
or sentence fragments.
It also has served as the first attempt to adapt UD annotation scheme
to Turkish, and the present UD Turkish guidelines are based on
the documentation of this treebank.
The treebank was introduced in [Çöltekin (2015)](papers/coltekin2015tlt.pdf),
contains sentences from [Göksel and Kerslake (2005)](https://www.routledge.com/Turkish-A-Comprehensive-Grammar/Goksel-Kerslake/p/book/9780415114943)
and addeitions from [Kornfilt 1997](https://www.routledge.com/Turkish-1st-Edition/Kornfilt/p/book/9780415587167) are on the way).

As of version 2.4, the treebank contains 2802 sentences, and 16509 tokens.

# Sentence selection, preprocessing, toekenization 

The treebank contains all numbered examples from the grammar book.
A few in-text examples are also included.
Some of the examples (currently 409) are not sentences
but sentence fragments, typically phrases.
The full sentences in the treebank always end with a punctuation mark,
while sentence fragments are are without a final punctuation.
The ungrammatical examples are skipped.
The "borderline acceptable" examples (marked with _?_ or _??_)
were included, with a sentence-level comment `# acceptability = ?`
(the value is as indicated in the grammar book).


# References

-  Çöltekin, Çağrı. "A grammar-book treebank of Turkish." _Proceedings
   of the 14th workshop on Treebanks and Linguistic Theories (TLT 14)_
   pages 35–49. 2015.
- Göksel, Aslı, and Celia Kerslake. _Turkish: A comprehensive grammar._
    Routledge, 2005.
-  Kornfilt, Jaklin. _Turkish._ Routledge, 1997

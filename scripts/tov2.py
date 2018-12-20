#!/usr/bin/env python3

import sys
from conllu import conllu_sentences

tb = conllu_sentences(sys.argv[1])

def feat_replace(fs, *args):
    ret = fs
    for  (old, new) in args:
        if old in fs:
            ret = ret.replace(old, new)
    return ret

for sent_num, sent in enumerate(tb):
    add_text = True
    add_id = True
    for c in sent.comment:
        if c.startswith('# text = '):
            add_text = False
        if c.startswith('# sent_id = '):
            add_id = False
    if add_text:
        sent.comment.append('# text = ' + sent.text())
    if add_id:
        sent.comment.append('# sent_id = {:04d}'.format(sent_num))
    for node in sent.nodes:
        if node.feats:
            node.feats = feat_replace(node.feats,
                    ('Aspect=Habit', 'Aspect=Hab'),
                    ('Negative=', 'Polarity='),
                    ('Number_psor=', 'Number[psor]='),
                    ('Person_psor=', 'Person[psor]='),
                    ('VerbType=Part', 'VerbForm=Part'))

            node.feats = '|'.join(sorted(node.feats.split('|')))

        if node.deprel == 'dobj':
            node.deprel = 'obj'

    print(sent)

#!/usr/bin/env python3

import sys, argparse, re 
from udtools.conllu import conllu_sentences


ap = argparse.ArgumentParser()
ap.add_argument('input_file')
args = ap.parse_args()

tb = conllu_sentences(args.input_file)

for sent_num, sent in enumerate(tb):
    for i, node in enumerate(sent.nodes[1:]):
        if node.upos == 'PRON' \
                and node.get_feat('PronType') is None\
                and node.lemma in {'ben', 'sen', 'biz', 'siz',
                'hepimiz', 'herkes', 'kimse',
                'bizler', 'sizler', 'onlar',
                'hiçbirimiz', 'hiçbiriniz',
                'bazılarınız', 'bazılarımız',
                'kiminiz', 'bazılarımız',
                'kendi'}:
            node.add_feat('PronType', 'Prs')
        elif node.upos == 'PRON' \
                and node.get_feat('PronType') is None\
                and node.lemma in {'o', 'şu', 'bu', 'bura', 'şura', 'ora'}:
            node.add_feat('PronType', 'Dem')
        elif node.upos == 'DET' \
                and node.get_feat('PronType') is None\
                and node.get_feat('Definite'):
            node.add_feat('PronType', 'Art')
        elif node.upos == 'DET' \
                and node.get_feat('PronType') is None\
                and node.lemma in {'şu', 'bu'}:
            node.add_feat('PronType', 'Dem')
        elif node.upos == 'NUM' \
                and node.get_feat('NumType') is None\
                and node.form[-2:] not in {'ci', 'cı', 'cu', 'cü', 'er', 'ar'}:
            node.add_feat('NumType', 'Card')
        elif node.upos == 'PRON' \
                and node.get_feat('PronType') is None:
            # This is catch-all type normally not used in this
            # treebank.
            # It keeps udapy checks happy, ideally we need to revise
            # this and possibly propose alternative values.
            node.add_feat('PronType', 'Ind')
        if node.upos == 'DET':
            node.del_feat('Number')
    print(sent)

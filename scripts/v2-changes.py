#!/usr/bin/env python3

import sys, argparse, re 
from udtools.conllu import conllu_sentences


ap = argparse.ArgumentParser()
ap.add_argument('input_file')
args = ap.parse_args()

tb = conllu_sentences(args.input_file)

for sent_num, sent in enumerate(tb):
    for i, node in enumerate(sent.nodes[1:]):
        node.xpos = None
        if node.upos in {'NOUN', 'PRON', 'PROP'} and node.get_feat('Case') is None:
            node.add_feat('Case', 'Nom')
        elif node.upos == 'ADJ' and node.feats is not None:
            node.add_feat('Case', 'Nom')
        elif node.upos == 'VERB' and node.get_feat('VerbType') == 'Vnoun':
            node.add_feat('Case', 'Nom')
    print(sent)

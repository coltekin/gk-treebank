#!/usr/bin/env python3

import sys, argparse, re 
from udtools.conllu import conllu_sentences


ap = argparse.ArgumentParser()
ap.add_argument('input_file')
args = ap.parse_args()

tb = conllu_sentences(args.input_file)

for sent_num, sent in enumerate(tb):
    for i, node in enumerate(sent.nodes[1:]):
        if node.upos == 'AUX' \
                and node.get_feat('VerbForm') is None \
                and node.get_feat('Mood') is not None:
            node.add_feat('VerbForm', 'Fin')
    print(sent)

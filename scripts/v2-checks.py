#!/usr/bin/env python3

import sys, argparse, re 
from udtools.conllu import conllu_sentences


def is_predicate(node, sent):
    if node.deprel in {'root', 'parataxis'}:
        # This may not always be correct
        return True
    if node.upos == 'VERB':
        return True
    elif node.deprel in {'xcomp', 'ccomp', 'advcl', 'acl'}:
        return True
    else:
        for child in sent.children_of(node):
            if child.deprel == 'cop':
                return True

ap = argparse.ArgumentParser()
ap.add_argument('input_file')
args = ap.parse_args()

tb = conllu_sentences(args.input_file)

for sent_num, sent in enumerate(tb):
    for i, node in enumerate(sent.nodes[1:]):
        head = sent.nodes[node.head]
        case = node.get_feat('Case') 
        if node.deprel in {'obj', 'xcomp', 'ccomp'}\
                and case not in {'Acc', 'Nom'}\
                and not (node.upos == 'VERB' and node.get_feat('VerbType') is None):
            match = True
            for child in sent.children_of(node):
                if child.deprel == 'cop' and child.get_feat('Case') in {'Acc', 'Nom'}:
                    match = False
            if node.upos == 'ADJ':
                match = False
            if match:
                print("{} {:04d}-{} {} is not nominatinve or accusative ({})".format(
                    args.input_file, sent_num+1, node.index, node.deprel, case))
        if node.deprel == 'obl' and case in {'Acc', 'Nom'}:
            print("{} {:04d}-{} {} with {} dependent.".format(
                args.input_file, sent_num+1, node.index, node.deprel, case))
        if node.deprel in {'iobj'}:
            print("{} {:04d}-{} The deprel {} should not be used.".format(
                args.input_file, sent_num+1, node.index, node.deprel))
        if node.deprel in {'acl', 'case'} and \
                head.upos not in {'NOUN', 'PRON', 'PROPN', 'NUM'}:
            print("{} {:04d}-{} The deprel {} should modify a nominal. ".format(
                args.input_file, sent_num+1, node.index, node.deprel))
        if node.deprel in {'advcl', 'mark'} and \
                not is_predicate(head, sent):
            print("{} {:04d}-{} The deprel {} should modify a predicate. ".format(
                args.input_file, sent_num+1, node.index, node.deprel))
        if node.deprel in {'obj'} and \
                head.deprel in {'NOUN', 'ADJ', 'PRON', 'PROPN'}:
            print("{} {04d}-{} The deprel '{}' should not modify nouns ".format(
                args.input_file, sent_num+1, node.index, node.deprel))

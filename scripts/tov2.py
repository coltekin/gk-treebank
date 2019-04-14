#!/usr/bin/env python3

import sys, argparse, re 
from udtools.conllu import conllu_sentences

ap = argparse.ArgumentParser()
ap.add_argument('input_file')
ap.add_argument('--id-prefix', '-I', default="GKXX")
args = ap.parse_args()


tb = conllu_sentences(args.input_file)

def feat_replace(fs, *args):
    ret = fs
    for  (old, new) in args:
        if old in fs:
            ret = ret.replace(old, new)
            ret = ret.replace('||', '|')
    if ret.startswith('|'):
        ret = ret[1:]
    if ret.endswith('|'):
        ret = ret[:-1]
    if not ret:
        ret = '_'
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
        t = re.sub(' ([:.,?…])', '\g<1>', sent.text().strip())
        sent.comment.append('# text = ' + t)
    if add_id:
        sent.comment.append('# sent_id = {}-{:04d}'.format(
            args.id_prefix, sent_num + 1))
    for node in sent.nodes:
        if node.upos == 'CONJ':
            node.upos = 'CCONJ'
        if node.upos == 'AUX' and node.lemma in {'mi', 'mı', 'mü', 'mu'}:
            node.lemma = 'mi'
        if node.feats:
            node.feats = feat_replace(node.feats,
                    ('Aspect=Habit', 'Aspect=Hab'),
                    ('Aspect=Perf-Rapid', 'Aspect=PerfRapid'),
                    ('Aspect=Dur-Perf', 'Aspect=DurPerf'),
                    ('Negative=', 'Polarity='),
                    ('Number_psor=', 'Number[psor]='),
                    ('Person_psor=', 'Person[psor]='),
                    ('Question=Yes', 'PronType=Int'),
                    ('Evidential=Nfh', 'Evident=Nfh'),
                    ('Mood=Cnd-Gen', 'Mood=CndGen'),
                    ('Mood=Abil-Gen', 'Mood=AbilGen'),
                    ('Mood=Abil-Abil-Gen', 'Mood=AbilAbilGen'),
                    ('Mood=Abil-Abil', 'Mood=AbilAbil'),
                    ('Mood=Abil-Cnd-Gen', 'Mood=AbilCndGen'),
                    ('Mood=Abil-Cnd', 'Mood=AbilCnd'),
                    ('Mood=Gen-Nec', 'Mood=GenNec'),
                    ('Reflex=True', 'Reflex=Yes'),
                    ('Tense=Pfut', 'Tense=Fut,Past|Aspect=Prosp'),
                    ('Voice=Cau-Pass-Rcp', 'Voice=CauPassRcp'),
                    ('Voice=Cau-Pass', 'Voice=CauPass'),
                    ('Voice=Cau-Cau-Pass', 'Voice=CauCauPass'),
                    ('Voice=Cau-Cau', 'Voice=CauCau'),
                    ('Voice=Cau-Rcp', 'Voice=CauRcp'),
                    ('Voice=Pass-Pass', 'Voice=PassPass'),
                    ('Voice=Pass-Rcp', 'Voice=PassRcp'),
                    ('Voice=Pass-Rfl', 'Voice=PassRfl'),
                    ('VerbType=Trans', ''),
                    ('VerbType=Part', 'VerbForm=Part'))

            if 'Aspect=Prosp' in node.feats:
                node.feats = feat_replace(node.feats, ('Aspect=Perf', ''))

            if '|' in node.feats:
                node.feats = '|'.join(sorted(set(node.feats.split('|'))))

        head = None
        if node.head:
            head = sent.nodes[node.head]
        next_node = None
        if node.index < len(sent):
            next_node = sent.nodes[node.index + 1]

        if head and 'nmod' in node.deprel and head.upos == 'VERB':
            node.deprel = node.deprel.replace('nmod', 'obl')
        if node.deprel == 'dobj':
            node.deprel = 'obj'
        if node.deprel == 'dobj:cau':
            node.deprel = 'obj'
        elif node.deprel == 'neg':
            node.deprel = 'advmod'
        elif node.deprel == 'nsubjpass':
            node.deprel = 'nsubj'
        elif node.deprel == 'csubjpass':
            node.deprel = 'csubj'
        elif node.deprel == 'mwe':
            node.deprel = 'fixed'
        elif node.deprel == 'name':
            node.deprel = 'flat'
        elif node.deprel == 'advcl:cond':
            node.deprel = 'advcl'

        if node.lemma and node.lemma[-3:] in {'mek', 'mak'}\
                and node.upos in {'VERB', 'AUX'}:
            node.lemma = node.lemma[:-3]

        if next_node and next_node.upos == 'PUNCT':
            node.misc = 'SpaceAfter=No'
        else:
            node.misc = '_'

        node.del_feat('Polarity', 'Pos')

    for mult in sent.multi.values():
        if 'SpaceAfter=No' in sent.nodes[mult.multi].misc:
            mult.add_misc('SpaceAfter', 'No')
            sent.nodes[mult.multi].del_misc('SpaceAfter')

    print(sent)

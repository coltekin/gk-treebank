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

def replace_dep_label(node, head):
    if head and 'nmod' in node.deprel and head.upos == 'VERB':
        node.deprel = node.deprel.replace('nmod', 'obl')
    if node.deprel == 'dobj':
        node.deprel = 'obj'
    if node.deprel == 'dobj:cau':
        node.deprel = 'obj'
    elif node.deprel == 'acl:poss':
        node.deprel = 'acl'
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
    elif node.deprel == 'nmod:own':
        node.deprel = 'nmod'
    elif node.deprel == 'conj:num':
        node.deprel = 'compound'
    elif node.deprel in {'obl:cau', 'obl:pass'}:
        node.deprel = 'obl:agent'

for sent_num, sent in enumerate(tb):
    add_text = True
    add_id = True
    for c in sent.comment:
        if c.startswith('# text = '):
            add_text = False
        if c.startswith('# sent_id = '):
            add_id = False
    if add_text:
        t = re.sub(' ([”!;:.,?…])', '\g<1>', sent.text().strip())
        t = re.sub('([“‘]) ', '\g<1>', t)
        sent.comment.append('# text = ' + t)
    if add_id:
        sent.comment.append('# sent_id = {}-{:04d}'.format(
            args.id_prefix, sent_num + 1))
    i = 1
    while i <= len(sent):
        node = sent.nodes[i]
        if node.upos == 'CONJ':
            node.upos = 'CCONJ'
        if node.upos == 'AUX' and node.lemma in {'mi', 'mı', 'mü', 'mu'}:
            node.lemma = 'mi'
        if node.feats:
            node.feats = feat_replace(node.feats,
                    ('Aspect=Dur-Perf', 'Aspect=DurPerf'),
                    ('Aspect=Habit', 'Aspect=Hab'),
                    ('Aspect=Perf-Rapid', 'Aspect=PerfRapid'),
                    ('Evidential=Nfh', 'Evident=Nfh'),
                    ('Mood=Abil-Abil-Gen', 'Mood=GenPotPot'),
                    ('Mood=Abil-Abil', 'Mood=PotPot'),
                    ('Mood=Abil-Cnd-Gen', 'Mood=CndGenPot'),
                    ('Mood=Abil-Cnd', 'Mood=CndPot'),
                    ('Mood=Abil-Gen', 'Mood=GenPot'),
                    ('Mood=Abil', 'Mood=Pot'),
                    ('Mood=Cnd-Gen', 'Mood=CndGen'),
                    ('Mood=Gen-Nec', 'Mood=GenNec'),
                    ('Negative=', 'Polarity='),
                    ('Number_psor=', 'Number[psor]='),
                    ('Person_psor=', 'Person[psor]='),
                    ('Question=Yes', 'PronType=Int'),
                    ('Reflex=True', 'Reflex=Yes'),
                    ('Tense=Pfut', 'Tense=Fut,Past|Aspect=Prosp'),
                    ('VerbType=Trans', ''),
                    ('Voice=Cau-Cau-Pass', 'Voice=CauCauPass'),
                    ('Voice=Cau-Cau', 'Voice=CauCau'),
                    ('Voice=Cau-Pass-Rcp', 'Voice=CauPassRcp'),
                    ('Voice=Cau-Pass', 'Voice=CauPass'),
                    ('Voice=Cau-Rcp', 'Voice=CauRcp'),
                    ('Voice=Pass-Pass', 'Voice=PassPass'),
                    ('Voice=Pass-Rcp', 'Voice=PassRcp'),
                    ('Voice=Pass-Rfl', 'Voice=PassRfl'),
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

        replace_dep_label(node, head)

        # invert coordination direction - approximate, breaks on some structures, needs manual check
        conj_head = None
        if node.deprel == 'conj':
            if node.index < head.index:
                if conj_head:
                    node.head = conj_head
                else:
                    conj_head = node.index
                    node.deprel = head.deprel
                    node.head = head.head
                    head.head = conj_head
                    head.deprel = 'conj'
                    replace_dep_label(node, head)

        # same for flat
        flat_head = None
        if node.deprel == 'flat':
            if node.index < head.index:
                if flat_head:
                    node.head = flat_head
                else:
                    flat_head = node.index
                    node.deprel = head.deprel
                    node.head = head.head
                    head.head = flat_head
                    head.deprel = 'flat'
                    replace_dep_label(node, head)

        # same for fixed
        fixed_head = None
        if node.deprel == 'fixed':
            if node.index < head.index:
                if fixed_head:
                    node.head = fixed_head
                else:
                    fixed_head = node.index
                    node.deprel = head.deprel
                    node.head = head.head
                    head.head = fixed_head
                    head.deprel = 'fixed'
                    replace_dep_label(node, head)
                    replace_dep_label(node, head)


        if node.lemma:
            if node.lemma[-3:] in {'mek', 'mak'}\
                    and node.upos in {'VERB', 'AUX'}:
                node.lemma = node.lemma[:-3]
            if node.lemma == "-0":
                node.lemma = "i"

            if node.lemma == 'değil' and node.deprel == 'cop':
                node.deprel = 'aux'
                node.upos = 'AUX'

            if node.lemma in {'olan', 'olarak'} and node.upos == 'AUX':
                node.lemma = 'ol'

            if node.lemma == '-ki' and head and head.form.endswith('ki'):
                node.lemma = 'ki'
                node.form = 'ki'
                head.form = head.form[:-2]

            if node.lemma == '-li'\
                    and head.form[-2:] in {'li', 'lı', 'lü', 'lu'}:
                node.lemma = 'li'
                node.form = head.form[-2:]
                head.form = head.form[:-2]

            if node.lemma == '-ce'\
                    and head.form[-2:] in {'ce', 'ca'}:
                node.lemma = 'ce'
                node.form = head.form[-2:]
                head.form = head.form[:-2]

        if node.form in {'“', '‘'} or\
                next_node and next_node.form not in {'“', '‘'} and next_node.upos == 'PUNCT':
            node.add_misc('SpaceAfter', 'No')
        else:
            node.del_misc('SpaceAfter')
        node.del_feat('Polarity', 'Pos')
        node.del_misc('TRmorphTag')
        node.del_misc('Stem')

        if node.form == "_" and node.feats == 'Mood=Ind|Number=Sing|Person=3|Tense=Pres':
            if node.misc and 'SpaceAfter=No' in node.misc:
                sent.nodes[node.index -1].add_misc('SpaceAfter','No')
            sent.delete_node(node.index)
        else:
            i += 1

    for mult in sent.multi.values():
        if sent.nodes[mult.multi].misc and 'SpaceAfter=No' in sent.nodes[mult.multi].misc:
            mult.add_misc('SpaceAfter', 'No')
            sent.nodes[mult.multi].del_misc('SpaceAfter')


    print(sent)

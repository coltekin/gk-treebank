#!/usr/bin/python3
""" 
"""

import sys, os
import brat


map_deprel = {
'advcl_cond': 'advcl:cond',
'advmod_emph': 'advmod:emph',
'compound_redup': 'compound:redup',
'conj_num': 'conj:num   ',
'nmod_tmod': 'nmod:tmod',
'nmod_own': 'nmod:own',
'nmod_poss': 'nmod:poss',
'acl_poss': 'acl:poss',
'nmod_part': 'nmod:part',
'nmod_cau': 'nmod:cau',
'nmod_comp': 'nmod:comp',
'nmod_pass': 'nmod:pass',
'dobj_cau': 'dobj:cau',
'ccomp_cau': 'ccomp:cau',
'aux_q': 'aux:q',
'xcomp_sc': 'xcomp',
'Person_psor': 'Person[psor]',
'Number_psor': 'Number[psor]',
}


for f in sys.argv[1:]:
    basename = f[:-4]

    with open(f, "r") as fp:
        ann = brat.read_ann(fp)

    conllu = [{}] # dummy first token ensures that the indexes match
    for i in sorted(ann.tokens.keys()):
        tok = ann.tokens[i]
        token = {'id' : tok.id,
                 'form' : tok.token,
                 'cpos' : tok.pos,
                 'pos' : tok.pos,
                 'head' : None,
                 'deprel' : None,
                 'deps': "_"}

        feats = ""
        for (label, val) in tok.attrs:
            if len(feats): delim = "|"
            else: delim = ""
            feats += "{}{}={}".format(delim, label, val)
        if len(feats) == 0:
            feats = "_"
        token['feats'] = feats

        lemma = None
        efeats = ""
        for (label, val) in tok.comments:
            if label == 'ExtraFeatures':
                for efeat in val.split("|"):
                    if efeat.startswith("Lemma="):
                        lemma = efeat.replace("Lemma=", "")
                    else:
                        if len(efeats): delim = "|"
                        else: delim = ""
                        efeats += "{}{}".format(delim, efeat)
        if lemma is None:
            token['lemma'] = "_"
        else:
            token['lemma'] = lemma

        if len(efeats) == 0:
            token['misc'] = "_"
        else:
            token['misc'] = efeats

        conllu.append(token)


    for i, rel in ann.relations.items():
        child = int(rel.arg2[1][1:])
        parent = int(rel.arg1[1][1:])
        conllu[child]['head'] = parent
        conllu[child]['deprel'] = rel.name
        
    i = 1
    sentences = []
    with open(basename + '.txt') as fp:
        for line in fp:
            start = i
            root = None
            for token in line.strip().split():
                if token != "_":
                    ighead = i
                    conllu[i]['igcount'] = 1
                else:
                    conllu[ighead]['igcount'] += 1
                    conllu[i]['ignum'] = i - ighead
                    conllu[i]['igcount'] = 0
                if ann.tokens[i].token != token:
                    print("tokens do not match {} != {}"
                            .format(ann.tokens[i].token, toke))
                    sys.exit(-1)
                if conllu[i]['head'] is None:
                    if root is not None:
                        print("Warning multiple nodes without head: {}: {}-{} in {}"
                                .format(f, conllu[root]['form'], conllu[i]['form'], line.strip()), file=sys.stderr)
                    root = i
                    conllu[i]['head'] = start - 1
                    conllu[i]['deprel'] = 'root'
                i += 1
            sentences.append((start, i))

    for start, end in sentences:
        for i in range(start, end):
            j = i - start + 1
            if conllu[i]['igcount'] > 1:
                print("{}-{}\t{}\t_\t_\t_\t_\t_\t_\t_\t_"
                        .format(j, j + conllu[i]['igcount'] - 1, conllu[i]['form']))

            deprel = conllu[i]['deprel'] 
            if deprel in map_deprel:
                deprel = map_deprel[deprel]

            print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}"
                    .format(j, conllu[i]['form'],
                               conllu[i]['lemma'], 
                               conllu[i]['cpos'], 
                               conllu[i]['pos'], 
                               conllu[i]['feats'], 
                               conllu[i]['head'] - start + 1, 
                               deprel,
                               conllu[i]['deps'], 
                               conllu[i]['misc'])) 
        print("")

#!/usr/bin/python3
""" This script replace tokens in an ANN file with the ones 
    provided with the one in morph/ directory. It also copies 
    the .txt file over from the same directory.
"""

import sys, shutil
from collections import namedtuple

from brat import read_ann,write_ann,Rel,Ann

# oldfp = open(sys.argv[1], 'r')
# newfp = open(sys.argv[2], 'r')
basename = sys.argv[1].replace('.ann', '') 
oldfname = basename + '.ann'
oldfp = open(oldfname, 'r')
newfp = open('morph/' + oldfname, 'r')
old = read_ann(oldfp)
new = read_ann(newfp)
oldfp.close()
newfp.close()

tok_out = {}
rel_out = {}
tok_map = {}

from difflib import SequenceMatcher

s = SequenceMatcher(isjunk=lambda x: x in "_.?!", 
                    a=[v.token for k, v in old.tokens.items()],
                    b=[v.token for k, v in new.tokens.items()],
                    autojunk=True)

opcodes = s.get_opcodes()

for op, i1, i2, j1, j2 in opcodes:
    if op == 'equal' or op == 'replace':
        for j in range(j2 - j1):
            tok_out[j1 + j + 1] = new.tokens[j1 + j + 1]
            tok_map[i1 + j + 1] = j1 + j + 1
    elif op == 'insert':
        for j in range(j2 - j1):
            tok_out[j1 + j + 1] = new.tokens[j1 + j + 1]

for tokid in tok_map:
    newid = tok_map[tokid]
    for com in old.tokens[tokid].comments:
        if com[0] == 'AnnotatorNotes':
            tok_out[newid].comments.append(com)

for relid in sorted(old.relations):
    rel = old.relations[relid]
    l1, t1 = rel.arg1
    l2, t2 = rel.arg2
    tok1 = int(t1[1:])
    tok2 = int(t2[1:])

    if tok1 not in tok_map or tok2 not in tok_map:
        print("Removing relation: R{}".format(relid), file=sys.stderr)
    else:
        rel_out[relid] = Rel(id = relid,
                             name = rel.name,
                             arg1 = (l1, "T{}".format(tok_map[tok1])),
                             arg2 = (l2, "T{}".format(tok_map[tok2])),
                             comments = rel.comments)

shutil.copyfile(oldfname, oldfname + '.backup')
with open(oldfname, "w") as fp:
    write_ann(Ann(tokens=tok_out, relations=rel_out), fp)
shutil.copyfile('morph/' + basename + '.txt', basename + '.txt')

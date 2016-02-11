import sys, shutil
from collections import namedtuple

Token = namedtuple('Token', ['id', 'pos', 'span', 'token', 'attrs', 'comments'])
Rel = namedtuple('Rel', ['id', 'name', 'arg1', 'arg2', 'comments'])
Ann = namedtuple('Ann', ['tokens', 'relations'])

def read_ann(fp):
    tokens = {}
    relations = {}
    for line in fp:
        rid, rest = line.strip().split('\t', maxsplit=1)
        numid = int(rid[1:])
        if rid[0] == 'T':
            tmp, token = rest.split('\t')
            pos, start, end = tmp.split()
            tokens[numid] = Token(id = numid,
                                  pos = pos,
                                  span = (start, end),
                                  token = token,
                                  attrs = [],
                                  comments = []
                            )
        elif rid[0] == 'A':
            label, tokid, value = rest.split()
            toknum = int(tokid[1:])
            tokens[toknum].attrs.append((label, value))
        elif rid[0] == '#':
            tmp, comment = rest.split('\t')
            com_label, refid = tmp.split()
            if refid[0] == 'T':
                toknum = int(refid[1:])
                tokens[toknum].comments.append((com_label, comment))
            elif refid[0] == 'R':
                relnum = int(refid[1:])
                relations[relnum].comments.append((com_label, comment))
        elif rid[0] == 'R':
            name, arg1, arg2 = rest.strip().split()
            relations[numid] = Rel(id = numid,
                                   name = name,
                                   arg1 = tuple(arg1.split(':')),
                                   arg2 = tuple(arg2.split(':')),
                                   comments = []
                               )
    return Ann(tokens=tokens, relations=relations)

def write_ann(ann, fp):
    commid = 1
    attrid = 1

    for tokid in ann.tokens:
        tok = ann.tokens[tokid]
        print("T{}\t{} {} {}\t{}".format(tok.id,
                                         tok.pos,
                                         tok.span[0],
                                         tok.span[1],
                                         tok.token),
              file = fp)
        for attr in tok.attrs:
            print("A{}\t{} T{} {}".format(attrid,
                                           attr[0],
                                           tok.id,
                                           attr[1]),
                  file = fp)
            attrid += 1
        for comm in tok.comments:
            print("#{}\t{} T{}\t{}".format(commid,
                                           comm[0],
                                           tok.id,
                                           comm[1]),
                  file = fp)
            commid += 1
    for relid in ann.relations:
        rel = ann.relations[relid]
        print("R{}\t{} {}:{} {}:{}\t".format(rel.id,
                                           rel.name,
                                           rel.arg1[0], rel.arg1[1],
                                           rel.arg2[0], rel.arg2[1]),
              file = fp)
        for comm in rel.comments:
            print("#{}\t{} R{}\t{}".format(commid,
                                           comm[0],
                                           rel.id,
                                           comm[1]),
                  file = fp)
            commid += 1


#!/usr/bin/python3
"""Parse TRmorph analysis into a sequence of feature-value pairs (for
   each IG).
"""

import sys, re, copy

a_re = re.compile('(?P<root>.*?)'
          '(?P<pos><[A-Z][A-Za-z0-9:]*>)'
          '(?P<inflections>.*?)'
          '(?P<rest>(<[^A-Z][A-Za-z0-9:]*><[A-Z][A-Za-z0-9:]*>.*)|$)')


features = {
    'paggr':        {'1s', '2s', '3s', '1p', '2p', '3p'},
    'prntype':      {'pers', 'locp', 'dem'},
    'prnrefl':      {'refl'},
    'numerictype':  {'card', 'ord', 'dist'},
    'case' :        {'acc', 'dat', 'abl', 'loc', 'gen', 'ins'},
    'tam' :         {'evid', 'fut', 'obl', 'impf', 'cont', 'past', 
                        'cond', 'opt', 'imp', 'aor'},
    'cpl' :         {'cpl:evid', 'cpl:past', 'cpl:cond', 'cpl:pres'},
    'dir' :         {'dir'},
    'number':       {'pl', 'sg'},
    'neg':          {'neg', 'pos'},
    'possessive':   {'p1s', 'p2s', 'p3s', 'p1p', 'p2p', 'p3p'},
    'postpclass':   {'adv', 'adj'},
    'postpcompl':   {'accC','genC','nomC', 'datC', 'ablC', 'insC', 'numC', 'liC'},
    'propernoun':   {'prop'},
    'dettype':      {'def', 'indef'},
    'numnotation':  {'ara', 'rom'},
    'numflags':     {'perc', 'time', 'date'},
    'cnjtype':      {'coo', 'sub', 'adv'},
    'abbreviation': {'abbr'},
    'question':     {'qst'},
    'partial':      {'partial'},
    'vcomp':        {'abil', 'iver', 'adur', 'agel', 'akal', 'ayaz', 'agor'},
    'voice':        {'rfl', 'rcp', 'pass', 'caus'},
    'mredup':       {'mredup'},
}

pos_features = {
   'N':     {'number': None,
             'possessive': None,
             'case': None,
             'propernoun': None,
             'abbreviation': None,
             'partial': None,
             'mredup': None,
    },
   'Prn':   {'number': None,
             'possessive': None,
             'case': None,
             'paggr': None,
             'prntype': None,
             'prnrefl': None,
             'question': None,
             'neg': None,
             'mredup': None,
    },
   'Num':   {'numerictype': None,
             'numnotation': None,
             'numflags': None,
             'question': None,
             'case': None,
             'mredup': None,
    },
   'Postp': {'postpclass': None,
             'postpcompl': None,
             'mredup': None,
    },
   'V':     {'voice': None,
             'vcomp': None,
             'neg': None,
             'tam': None,
             'cpl': None,
             'paggr': None,
             'dir': None,
             'question': None,
             'partial': None,
             'mredup': None,
    },
   'Q':     {'cpl': None,
             'paggr': None,
             'dir': None,
    },
   'Det':   {'dettype': None,
             'number': None,    # intermediate only: bazı-lar-ı
             'question': None,
             'neg': None,
             'mredup': None,
    },
   'Cnj':   {'cnjtype': None,
             'partial': None,
             'mredup': None,
    },
   'Exist': {'neg': None,
             'mredup': None,
    },
   'Not':   {'neg': None,
             'mredup': None,
    },
   'Adj':   {'possessive': None,
             'question': None,
             'mredup': None,
             'partial': None,
    },
   'Adv':   {'question': None,
             'partial': None,
             'mredup': None,
    },
   'Ij':    dict(),
   'Onom':  dict(),
   'Punc':  dict(),
   'Sym':  dict(),
}

def parse_astring(astring):
    igs = []
    m = re.match(a_re, astring)
    while m and m.group('root'):
        igs.append((m.group('root'),m.group('pos'),m.group('inflections')))
        m = re.match(a_re, m.group('rest'))
    return igs

# def add_feature(ig, infl):
#     """ Convert a morphological tag to feature-value pair, and insert into the ig.
#     """
#     found = False
#     for key in sorted(features):
#         if infl in features[key]:
#             if key in ig and ig[key] not in {'none', 'na'}:
#                 ig[key] = ig[key] + '+' + infl
#             else:
#                 ig[key] = infl
#             found = True
#             break
#     if not found:
#         ig['unk-feat'].append(infl)
# 
def assign_features(ig):
    pos = ig[1].replace('<', '').replace('>', '')
    cpos = pos.split(':')[0]
    lex_feat = pos.split(':')[1:]
    morph_feat = ig[2].replace('><', '\t').replace('<','')\
                     .replace('>','').split()
    flist = pos_features[cpos].copy()
    for infl in lex_feat + morph_feat:
        found = False
        flabel = None
        for flabel in flist:
            if infl in features[flabel]:
                if flist[flabel]:
                    flist[flabel] += '+' + infl
                else:
                    flist[flabel] = infl
                found = True
                break
        if not found:
            print("Warning: Feature `{}' unknown for POS `{}/{}' in {}"\
                    .format(infl, cpos, flabel, ig))
    flist['pos'] = cpos
    flist['root'] = ig[0]
    flist['astr'] = ig[0] + ig[1] + ig[2]
    return flist

# def parse_analysis(s):
#     """ Parse an analysis string produced by TRmorph, and return it as
#     a sequence of feature-value pairs for each IG.
#     """
#     featlist = []
#     iglist = parse_astring(s)
#     for ig in iglist:
#         igf = {}
#         for feat in features:
#             igf[feat] = 'na'
#         igf['root'] = ig[0]
#         igf['pos'] = ig[1].replace('<', '').replace('>', '')
#         assign_default_features(igf)
#         for infl in ig[2].replace('><', '\t').replace('<','')\
#                          .replace('>','').split():
#             add_feature(igf, infl)
#         igf['astr'] = ig[0] + ig[1] + ig[2]
#         featlist.append(igf)
#     return featlist 

def parse_analysis(a):
    flist = []
    for ig in parse_astring(a):
        flist.append(assign_features(ig))
    return flist

def main(args):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    for line in sys.stdin:
        line = line.strip()
        print("++++++ {}".format(line), file=sys.stderr)
        if not line:
            continue
        w, a =  line.split()
        print("------- {} -----".format(w))
        for ig in parse_astring(a):
            pp.pprint(assign_features(ig))
        print()

if __name__ == "__main__":
    sys.exit(main(sys.argv))


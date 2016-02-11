#!/usr/bin/python3
"""Convert word-TRmorph analysis per line format to Brat stand-off
   annotation format for dependncy analysis.
"""

import sys, re
from trmorph import parse_analysis
import pprint
from flookup import Fst

pp = pprint.PrettyPrinter(indent=4)


map_pos = {
    'Alpha':    'X',
    'Adj':      'ADJ',
    'Adv':      'ADV',
    'Cnj':      'CONJ',
    'Det':      'DET',
    'Exist':    'ADJ',
    'Ij':       'INTJ',
    'N':        'NOUN',
    'Not':      'PART',
    'Num':      'NUM',
    'Onom':     'X',
    'Postp':    'ADP',
    'Prn':      'PRON',
    'Punc':     'PUNCT',
    'Sym':      'SYM',
    'Q':        'AUX',
    'V':        'VERB',
}

map_prntype = {
    'pers': 'Prs', 
    'locp': 'Loc', 
    'dem': 'Dem',
}

map_tam = {
    'evid':     'Evid', 
    'fut':      'Fut', 
    'obl':      'Obl',
    'impf':     'Impf',
    'cont':     'Cont',
    'past':     'Past',
    'cond':     'Cond',
    'opt':      'Opt',
    'imp':      'Imp',
    'aor':      'Aor',
    'cpl:evid': 'Evid', 
    'cpl:past': 'Past', 
    'cpl:cond': 'Cond', 
    'cpl:pres': 'Pres'
}

map_deriv_stem = {
    '<cpl:past>': 'idi',
    '<cpl:evid>': 'imiş',
    '<cpl:pres>': 'i',
    '<ise>': 'ise',
    '<cv:ken>': 'iken',
    '<cv:ip>': '-ip',
    '<cv:ince>': '-ince',
    '<cv:den>': '-den',
    '<cv:erek>': '-erek',
    '<cv:ye>': '-ye',
    '<cv:cesine>': '-cesine',
    '<cv:dikce>': '-dikce',
    '<cv:eli>': '-eli',
    '<cv:mesine>': '-mesine',
    '<part:past>': '-dik',
    '<part:pres>': '-en',
    '<part:fut>': '-ecek',
    '<part:esi>': '-esi',
    '<vn:past>': '-dik',
    '<vn:pres>': '-en',
    '<vn:fut>': '-ecek',
    '<vn:inf>': '-mek',
    '<vn:yis>': '-yis',
    '<vn:esi>': '-esi',
    '<dir>': '-dir',
    '<loc>': '-de',
    '<abl>': '-den',
    '<leri>': '-leri',
    '<ligine>': '-liğine',
    '<0>': '-0',
    '<ci>': '-ci',
    '<ca>': '-ce',
    '<ki>': '-ki',
    '<li>': '-li',
    '<siz>': '-siz',
    '<lik>': '-lik', # ????
    '<li>': '-li',
    '<p1s>': '-im',
    '<p2s>': '-in',
    '<p3s>': '-i',
    '<p1p>': '-imiz',
    '<p2p>': '-iniz',
    '<p3p>': '-leri',
}

def main(args):
    basename = args[1]
    afp = open(basename + ".ann", "w")
    tfp = open(basename + ".txt", "w")
    toknum = 1
    attrnum = 1
    woffset = 0
    start = True

    trmorph_gen = Fst(fst="/home/cagri/trmorph/trmorph-low-ambig.fst",
                      inverse=True)
    stem_re = re.compile(r'(.*)(<[A-Z].*?>)')

    for line in sys.stdin:
        line = line.strip()

        if not line:
            print("", file=tfp)
            woffset += 1
            start = True
            continue


        try:
            w, a =  line.split()
        except:
            print("failed to parse:  {}".format(line))

        igs = parse_analysis(a)
#        pp.pprint(igs)
        collapse = False
        collapse_feat = None
        collapse_word = None
        collapse_a = None
        for ignum, ig in enumerate(igs):

            features = {'Number': None,
                        'Person': None,
                        'PronType': [],
                        'Reflex': None,
                        'NumType': None,
                        'Case': None,
                        'Voice': [],
                        'Tense': None,
                        'Aspect': [],
                        'Mood': [],
                        'Negative': None,
                        'Number_psor': None,
                        'Person_psor': None,
                        'Definite': None,
                        'Abbreviation': None,
                        'Question': None,       # Not in UD
                        'VerbType': None,
                        'Evidential': None,
            }

            pos = ig['pos']
            root = ig['root']

            if ignum == 0:
                word = w
            else:
                word = "_"


#            print("+++++{}pos: {} root: {}".format(ignum, pos, root))
            if (ignum + 1) < len(igs):
                next_ig = igs[ignum + 1]
#                print("----{}pos: {}/{} - {}/{}".format(ignum, root, pos , next_ig['root'], next_ig['pos']))
                if   (next_ig['root'] in # collapse regardless of the context
                        {'<la>', '<lan>', '<las>', '<yici>', '<si>', '<ci>'})\
                  or (next_ig['root'] == '<0>' and # 0-deriv. Ad{j/v}->N
                      pos in {'Adj', 'Adv'} and
                      next_ig['pos'] == 'N')\
                  or (next_ig['root'] == '<lik>' and # -lIK: N/Ad{j/v}->N
                      pos in {'Adj', 'Adv', 'N'} and
                      next_ig['pos'] == 'N')\
                  or (next_ig['root'] in # Det->Prn derivation 
                     {'<p1s>', '<p2s>', '<p3s>', '<p1p>', '<p2p>', '<p3p>'} and
                      ignum == 0 and
                      pos in {'Det', 'Adv', 'Adj', 'Num'} and
                      next_ig['pos'] == 'Prn')\
                  or (pos == 'N' and    # complex postpositions
                      next_ig['pos'] == 'Postp' and
                      next_ig['root'] in {'<loc>', '<abl>', '<ins>', '<ca>', '<dat>'})\
                  or (next_ig['root'] == '<ca>' and # only when Adj/Adv->Adj/Adv
                      pos in {'Adv', 'Adj'}  and
                      next_ig['pos'] in {'Adv', 'Adj'})\
                  or (root == '<0>' and # for -mA(z)lıkdan
                      next_ig['root'] == '<lik>' and
                      pos == 'Adj'  and
                      next_ig['pos'] == 'N')\
                  or (root == 'değil' and
                      next_ig['root'] == '<0>' and
                      next_ig['pos'] == 'V'):
                    # collapse current IG, only the root information
                    # and some of the features if they exist.
                    if not collapse:
                        collapse_word = word
                        collapse_a = ig['astr']
                        collapse_feat = {'root': ig['root']} 
                    else:
                        collapse_a += ig['astr']
#                    print("Collapse: {}/{} -> {}/{}".format(root, pos, next_ig['root'], next_ig['pos']))
                    for ff in {'question', 'neg', 'possessive'}:
                        if ff in ig:
                            collapse_feat[ff] = ig[ff]
                    if root == 'değil':
                        collapse_feat['neg'] = 'neg'
                    collapse = True
                    continue
                elif (next_ig['root'] == '<0>' and   # <0> deriv. from Num -> N
                      ignum == 0 and
                      pos == 'Num' and
                      next_ig['pos'] == 'N')\
                  or (pos == 'Postp' and    # <0><N> after a postposition
                      next_ig['pos'] == 'N' and
                      next_ig['root'] == '<0>'):
                    # collapse curren IG, but use the POS from this one
                    collapse = True
                    collapse_feat = {'root': ig['root'], 'pos': pos} 
                    collapse_word = word
                    collapse_a = ig['astr']
                    continue
                elif (next_ig['root'].startswith('<cv:')):
                    # collapse curren IG, but use the POS from this one
                    cvtype = next_ig['root'].replace('<cv:', '')[:-1]
                    if not collapse:
                        collapse = True
                        collapse_feat = {'root': ig['root'], 
                                         'pos': pos,
                                         'verbtype': 'Trans',
                                         'cvtype': cvtype
                        } 
                        collapse_word = word
                        collapse_a = ig['astr']
                    else:
                        collapse_feat['pos'] = pos
                        collapse_feat['verbtype'] = 'Trans'
                        collapse_feat['cvtype'] = cvtype
                        collapse_a += ig['astr']
                    continue
                elif (next_ig['root'].startswith('<part:')):
                    # collapse curren IG, but use the POS from this one
                    parttype = next_ig['root'].replace('<part:', '')[:-1]
                    if not collapse:
                        collapse = True
                        collapse_feat = {'root': ig['root'], 
                                         'pos': pos,
                                         'verbtype': 'Part',
                                         'parttype': parttype
                        } 
                        collapse_word = word
                        collapse_a = ig['astr']
                    else:
                        collapse_feat['pos'] = pos
                        collapse_feat['verbtype'] = 'Part'
                        collapse_feat['parttype'] = parttype
                        collapse_a += ig['astr']
                    continue


            if collapse:
#                print("collapsing ({})...".format(toknum))
                ig['astr'] = collapse_a + ig['astr']
                for k,v in collapse_feat.items():
#                    print("    {} = {}".format(k,v))
                    ig[k] = v
                word = collapse_word
                pos = ig['pos']
                root = ig['root']
                collapse = False
                collaspe_feat = None
                collapse_word = None
                collapse_a = None



            ud_pos = map_pos[pos]

            if pos == 'Q':
                ud_pos = 'AUX'
                features['Question'] = 'Yes'
            elif pos == 'Not':
                features['Negative'] = 'Neg'
            elif pos == 'N' and ig['propernoun']  == 'prop':
                ud_pos = 'PROPN'
            elif pos == 'Cnj':
                if ig['cnjtype'] == 'sub':
                    ud_pos = 'SCONJ'
                elif ig['cnjtype'] == 'adv':
                    ud_pos = 'ADV'

            if start:
                begin = woffset
                end = woffset + len(word)
            else:
                begin = woffset + 1
                end = woffset + len(word) + 1

            if word == "_":
                begin += 1
                end += 1
            print("T{}\t{} {} {}\t{}".format(toknum, ud_pos, begin,
                end, word.strip()), file=afp)


            # Mark for Person/Number on a verb only when it is finite
            # (used as a predicate)
            if (ignum + 1) != len(igs) and pos == 'V':
                # Subordinated verb. Person/Number is marked on the
                # following ig.
                next_ig = igs[ignum + 1]
                if (next_ig['pos'] in {'N', 'Adj'} and 
                        'possessive' in next_ig and 
                        next_ig['possessive'] is not None):
                    next_pos_mark = next_ig.pop('possessive')
                    features['Person'] = next_pos_mark[1]
                    if next_pos_mark[2] == 's':
                        features['Number'] = 'Sing'
                    elif next_pos_mark[2] == 'p':
                        features['Number'] = 'Plur'
                    else:
                        print("Unexpected value {} for possessive"\
                                .format(next_ig['paggr']))
                        sys.exit(-1)
            elif 'paggr' in ig:
                if ig['paggr'] is None:
                    pass
#                    features['Person'] = '3'
#                    features['Number'] = 'Sing'
                else:
                    if ig['paggr'][1] == 's':
                        features['Number'] = 'Sing'
                    elif ig['paggr'][1] == 'p':
                        features['Number'] = 'Plur'
                    else:
                        print("Unexpected value {} for p/n aggreement"\
                                .format(ig['paggr']))
                        sys.exit(-1)

                    features['Person'] = ig['paggr'][0]


            if 'question' in ig and ig['question'] is not None:
                features['PronType'].append('Int')
                features['Question'] = 'Yes'

            if 'voice' in ig and ig['voice'] is not None:
                for vv in ig['voice'].split('+'):
                    if vv == 'rfl':
                        features['Voice'].append('Rfl')
                    elif vv == 'rcp':
                        features['Voice'].append('Rcp')
                    elif vv == 'pass':
                        features['Voice'].append('Pass')
                    elif vv == 'caus':
                        features['Voice'].append('Cau')

            if 'prnrefl' in ig and ig['prnrefl'] == 'refl':
                features['Reflex'] = True

            if 'numerictype' in ig:
                if ig['numerictype'] == 'ord':
                    features['NumType'] = 'Ord'
                elif ig['numerictype'] == 'dist':
                    features['NumType'] = 'Dist'
                elif ig['numerictype'] == 'range':
                    features['NumType'] = 'Range'
                else:
                    features['NumType'] = 'Ord'

            if 'case' in ig and ig['case']:
                if ig['case'] is not None:
                    features['Case'] = ig['case'].capitalize()
                else:
                    features['Case'] = 'Nom'

# start tense/aspect/modality

            tense = None
            aspect = []
            mood = []
            if 'vcomp' in ig and ig['vcomp'] is not None:
                for ff in ig['vcomp'].split('+'):
                    if ff == 'abil': mood.append('Abil')
                    elif ff == 'iver': aspect.append('Rapid')
                    elif ff == 'ayaz': aspect.append('Pro')
                    elif ff in {'adur', 'agel', 'akal', 'agor'}:
                        aspect.append('Dur')
                    #TODO: 'agor' is not durative

            if 'tam' in ig:
                if ig['tam'] == 'past':
                    tense = 'Past'
                    aspect.append('Perf')
                elif ig['tam'] == 'evid':
                    tense = 'Past'
                    aspect.append('Perf')
#                    mood.append('Evid')
                    features['Evidential'] = 'Nfh'
                elif ig['tam'] == 'fut':
                    tense = 'Fut'
                    aspect.append('Perf')
                elif ig['tam'] == 'aor':
                    tense = 'Pres'
                    aspect.append('Habit')
                    mood.append('Gen')
                elif ig['tam'] == 'cont':
                    tense = 'Pres'
                    aspect.append('Prog') # can be 'Habit', but again difficult to disambiguate
                elif ig['tam'] == 'impf':
                    tense = 'Pres'
                    aspect.append('Prog')
                elif ig['tam'] == 'obl':
                    tense = 'Pres'
                    mood.append('Nec')
                elif ig['tam'] == 'cond':
                    tense = 'Pres'
                    mood.append('Cnd')
                elif ig['tam'] == 'imp':
                    tense = 'Pres'
                    mood.append('Imp')
                    #TODO: mark persuasive versions 'Prs'
                elif ig['tam'] == 'opt':
                    tense = 'Pres'
                    mood.append('Opt')

            if 'cpl' in ig and ig['cpl'] is not None:
                if '+' in ig['cpl']:
                    cpl1, cpl2 = ig['cpl'].split('+')
                else:
                    cpl1 = ig['cpl']
                    cpl2 = None
                if cpl1 == 'cpl:pres':
                    # this can only happen with nominal predicates
                    tense = 'Pres'
                elif cpl1 == 'cpl:cond':
                    mood.append('Cnd')
                elif cpl1 == 'cpl:past':
                    if tense == 'Past': tense = 'Pqp'
                    elif tense == 'Fut': tense = 'Pfut'
                    else: tense = 'Past'
                elif cpl1 == 'cpl:evid':
                    if tense:
#                        mood.append('Evid')
                        features['Evidential'] = 'Nfh'
                    else:
                        tense = 'Past'
                        features['Evidential'] = 'Nfh'
#                        mood.append('Evid')

                if cpl2 == 'cpl:cond':
                    mood.append('Cnd')
                elif cpl2 == 'cpl:past':
                    if tense == 'Past': tense = 'Pqp'
                    elif tense == 'Fut': tense = 'Pfut'
                    else: tense = 'Past'
                elif cpl2 == 'cpl:evid':
                    if tense:
#                        mood.append('Evid')
                        features['Evidential'] = 'Nfh'
                    else:
                        tense = 'Past'
#                        mood.append('Evid')
                        features['Evidential'] = 'Nfh'

            if 'dir' in ig and ig['dir'] is not None:
                mood.append('Gen')

# handle tense in subordinated verbs
            
            if pos == 'V' and 'verbtype' in ig:
                if ig['verbtype'] == 'Trans':
                    features['VerbType'] = 'Trans'
                elif ig['verbtype'] == 'Part':
                    features['VerbType'] = 'Part'
                    if 'pres' == ig['parttype']:
                        tense = 'Pres'
                    if 'fut' ==  ig['parttype']:
                        tense = 'Fut'
                    if 'past' ==  ig['parttype']:
                        tense = 'Past'


            # TODO: the Adj part below is unnecessary
            if pos == 'V' and (ignum + 1) != len(igs):
#                print("{} - {}".format(ig, next_ig))
                next_ig = igs[ignum + 1]
                if next_ig['pos'] in {'N', 'Adj'}:
                    if ':pres' in next_ig['root']:
                        tense = 'Pres'
                    elif ':fut' in next_ig['root']:
                        tense = 'Fut'
                    elif ':past' in next_ig['root']:
                        tense = 'Past'

            if pos == 'V' and not mood:
                mood = ['Ind']

            if tense:
                features['Tense'] = tense
            if aspect:
                features['Aspect'] = sorted(aspect)
            if mood:
                features['Mood'] = sorted(mood)


# end tense/aspect/modality

            if 'number' in ig:
                if ig['number'] == 'pl':
                    features['Number'] = 'Plur'
                else:
                    features['Number'] = 'Sing'
            if 'neg' in ig:
                if ig['neg'] == 'neg' or ig['root'] == 'değil':
                    features['Negative'] = 'Neg'
                else:
                    features['Negative'] = 'Pos'

            if 'possessive' in ig and ig['possessive'] is not None:
                if ig['possessive'][2] == 's':
                    features['Number_psor'] = 'Sing'
                else:
                    features['Number_psor'] = 'Plur'
                
                features['Person_psor'] = ig['possessive'][1]

            if 'dettype' in ig and ig['dettype'] is not None:
                if ig['dettype'] == 'def':
                    features['Definite'] = 'Def'
                elif ig['dettype'] == 'indef':
                    features['Definite'] = 'Ind'
                else:
                    print("Unexpected value {} for p/n aggreement"\
                            .format(ig['paggr']))
                    sys.exit(-1)

            if 'abbreviation' in ig and ig['abbreviation'] is not None:
                features['Abbreviation'] = 'Yes'

#            features['TRmorphTag'] = ig['astr']

# lemma and stem assignment
#            print("{}: {} - {}".format(toknum, word, ig['astr']),
#                    file=sys.stderr)
            if word == "_":
                lemma = "_"
                stem = map_deriv_stem[ig['root']]
#                print("Multi-IG: {} {} {}".format(ig['root'], w, a))
            else:
                m = re.match(stem_re, ig['astr'])
                a_stem = m.group(1) + m.group(2)
                is_verb = a_stem.endswith('<V>')
                if  is_verb and root not in {'değil', 'i'}:
                    a_stem += '<vn:infmAK><N>'
                lemlist = trmorph_gen.analyze(a_stem)
                if not lemlist:
                    if root == 'i':
                        lemma = 'i-'
                        stem = 'i-'
                    elif root == 'değil':
                        lemma = 'değil'
                        stem = 'değil'
                    elif root == 'birbir':
                        lemma = 'birbir'
                        stem = 'birbir'
                    else:
                        print("Canot generate surface form for: {}".format(a_stem))
                        lemma = 'unknown'
                        stem = word
                elif len(lemlist) > 1:
#                    print("ambiguous analysis: {}: {}".format(word, lemlist))
                    lemma = None
                    stem = None
                    for ll in lemlist:
                        if is_verb:
                            if word.startswith(ll[:-3]):
                                lemma = ll
                                stem = ll[:-3]
                                break
                        else:
                            if word.startswith(ll):
                                lemma = ll
                                stem = ll
                                break
                else:
                    try:
                        lemma = lemlist[0]
                    except:
                        print("{}: {}".format(w, a_stem))
                    if is_verb:
                        stem = lemma[:-3]
                    else:
                        stem = lemma

            if root == 'değil' and ud_pos == 'PART':
                features['Negative'] = None
                features['PronType'].append('Neg')
            elif root == 'birbir':
                features['PronType'].append('Rcp')

            for label in sorted(features):
                val = features[label]
                if not val: continue
                if type(val) is list:
                    v = "-".join(sorted(val))
                    print("A{}\t{} T{} {}"\
                            .format(attrnum, label, toknum, v), file=afp)
                else:
                    print("A{}\t{} T{} {}"\
                            .format(attrnum, label, toknum, val), file=afp)
                attrnum += 1

            if lemma == "_" or lemma is None:
                lemma = stem
            print("#{}\tExtraFeatures T{}\tTRmorphTag={}|Lemma={}|Stem={}"\
                    .format(toknum, toknum, ig['astr'], lemma, stem),
                  file=afp)

            toknum += 1
            if word == "_":
                print(" ", file=tfp, end="")
                woffset += 1
            if start:
                print(word, file=tfp, end="")
                woffset += len(word)
            else:
                print(" {}".format(word), file=tfp, end="")
                woffset += len(word) + 1
            start = False
#            print("", file=afp)
#    print("", file=tfp)
    tfp.close()
    afp.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))


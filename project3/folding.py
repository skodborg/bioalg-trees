import hpview3k
import sys

def fold_hp_string(HPstr='hhppppphhppphppphp'):
    even = [i for i, v in enumerate(HPstr)
            if v == 'h' and i % 2 == 0]
    odd = [i for i, v in enumerate(HPstr)
           if v == 'h' and i % 2 == 1]

    match_even_odd = list(zip(even, reversed(odd)))
    match_even_odd = [(e, o) for e, o in match_even_odd
                      if e < o]
    # print(match_even_odd)

    match_odd_even = list(zip(odd, reversed(even)))
    match_odd_even = [(o, e) for o, e in match_odd_even
                      if o < e]
    # print(match_odd_even)

    max_matching = match_even_odd if len(match_even_odd) > len(match_odd_even) else match_odd_even
    # print(max_matching)
    # max_matching = match_even_odd

    center_match = max_matching[-1]
    split_idx = center_match[0] + int((center_match[1] - center_match[0] - 1) / 2) + 1
    # print(split_idx)
    S1 = HPstr[:split_idx]
    S2 = HPstr[split_idx:]
    # print(S1 + ',' + S2)
    
    # introduce 's' in final fold at this pos to make S1 and S2 face each other
    # such that fold[S1_face_S2_idx] = 's'
    S1_face_S2_idx = split_idx - 1

    fold = 'e' * (split_idx - 1)
    fold += 's'
    fold += 'w' * (len(HPstr) - len(fold) - 1)
    
    # print_folding(HPstr, fold)

    S1_fold = ''
    for i, m in enumerate(max_matching):
        if i == 0:
            # first matching
            S1_fold += 'e' * m[0]
        else:
            prev_m = max_matching[i - 1]
            ns_pairs = int((m[0] - prev_m[0]) / 2) - 1
            S1_fold += 'n' * ns_pairs
            S1_fold += 'e'
            S1_fold += 's' * ns_pairs
            S1_fold += 'e'

    # append remaining 'e', if any
    remainder = len(S1) - max_matching[-1][0] - 1
    S1_fold += 'e' * remainder


    S2_fold = 'w' * remainder
    for i, m in enumerate(reversed(max_matching)):
        if i == 0:
            # first matching
            continue
        else:
            prev_m = max_matching[len(max_matching) - i]
            ns_pairs = int((m[1] - prev_m[1]) / 2) - 1
            S2_fold += 's' * ns_pairs
            S2_fold += 'w'
            S2_fold += 'n' * ns_pairs
            S2_fold += 'w'

    remainder = len(HPstr) - max_matching[0][1] - 1
    S2_fold += 'w' * remainder

    
    final_fold = S1_fold + 's' + S2_fold
    # print(final_fold)

    print_folding(HPstr, final_fold)



def print_folding(string, fold):

    seq = hpview3k.HPFold(string)

    if len(seq) != len(string):
        print("The sequence %s contains illegal characters." % (string))
        sys.exit(1)
        
    absfold = hpview3k.make_absfold(fold)
    relfold = hpview3k.make_relfold(fold)

    if len(absfold) != len(fold) and len(relfold) != len(fold):
        print("The folding %s contains illegal characters." % fold)
        sys.exit(1)
        
    if len(absfold) == len(seq) - 1:
        seq.SetAbsFold(absfold)
    elif len(relfold) == len(seq) - 1:
        seq.SetRelFold(relfold)
    else:
        print("The folding %s has wrong length." % (fold))
        sys.exit(1)

    seq.PrintFold()

def main():
    # fold_hp_string('hhphphphphhhhphppphppphpppphppphppphphhhhphphphphh')
    fold_hp_string('ppphhpphhhhpphhhphhphhphhhhpppppppphhhhhhpphhhhhhppppppppphphhphhhhhhhhhhhpphhhphhphpphphhhpppppphhh')


if __name__ == '__main__':
    main()

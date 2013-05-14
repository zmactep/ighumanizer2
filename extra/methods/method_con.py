__author__ = 'mactep'
__doc__ = "Method of consensus carcass regions (on aligned sequence)"


import copy
from extra.share import ig_tools

def getLetterCount( hom_dict, region, i ):
    h_cnt = {}
    for hom in hom_dict:
        l = hom_dict[hom].get(region)[i]
        if l not in h_cnt:
            h_cnt[l] = 1
        else:
            h_cnt[l] += 1
    for l in h_cnt:
        h_cnt[l] /= (1.0 * len(hom_dict))

    return h_cnt

def humanizeFR( fr_init, fr_variants ):
    hum = [fr_init]
    for i in xrange(len(fr_init)):
        new_hum = []
        for v in fr_variants[i]:
            for h in hum:
                new_hum.append(h[:i] + v + h[i+1:])
        hum = new_hum
    return hum

def humanization_algorithm( domain ):
    threshold_up = 0.9
    threshold    = 0.7

    tmp_variants = [[],[],[]]
    hom_dict = copy.deepcopy(domain.germlineDomDict)
    hom_dict.update(domain.homologDomDict)

    # First pass. Fill tmp_variants
    for frN in [1,2,3]:
        fr = domain.getDomain().getFR(frN)
        for i in xrange(len(fr)):
            h_cnt_i = getLetterCount(hom_dict, "FR{0}".format(frN), i)
            to_change = [fr[i]]
            for l in h_cnt_i:
                if h_cnt_i[l] >= threshold_up:
                    tmp_variants[frN-1].append([l])
                    break
                elif h_cnt_i[l] >= threshold:
                    to_change.append(l)
            else:
                tmp_variants[frN-1].append(to_change)

    # Second pass. Process tmp_variants
    frs  = [humanizeFR(domain.getDomain().getFR(i), tmp_variants[i-1]) for i in [1,2,3]]
    hum_result = {}
    counter = 0
    for fr1 in frs[0]:
        for fr2 in frs[1]:
            for fr3 in frs[2]:
                counter += 1
                n = domain.getDomain().name + "-con" + str(counter)
                d = ig_tools.Domain((n, ""))
                d.cdr = domain.getDomain().cdr
                d.fr = [fr1, fr2, fr3]
                hum_result[n] = d

    domain.humanizeDomDict = hum_result

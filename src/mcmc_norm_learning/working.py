# TO DO: Change this module name and/to distribute this code amongst other modules
# This was initially just an area for code being worked on

from environment import get_obj
#from robot_task_new import PossMove
from rules_4 import *
from itertools import permutations, product
from collections import namedtuple, Sequence
from operator import mul
from functools import reduce
import math
from scipy.special import binom


FixedSeq = namedtuple("FixedSeq", ["seq"])

def unless_moves(pairs_dict):
    for o,poss_moves in pairs_dict.items():
        # print(o, poss_moves)
        zone_unless_pairs = [(pm.putdown[-1],pm.unless) for pm in poss_moves if pm.unless is not None]
        if len(zone_unless_pairs) > 0:
            zones, unlesses = zip(*zone_unless_pairs)
            dict_copy = dict(pairs_dict)
            del dict_copy[o]
            yield (o, zones, unlesses[0], dict_copy)
        
def matching_subseqs(moved_conds, pairs_dict, obl_obj_id, obl_obj_zones, env):
    if len(moved_conds) == 0:
        yield {obl_obj_id: set(obl_obj_zones)}
    else:
        for moved_cond in moved_conds:
            colour_cond = moved_colour(moved_cond)
            cond_colours = {colour_cond} if colour_cond != 'any' else colours_set()
            shape_cond = moved_shape(moved_cond)
            cond_shapes = {shape_cond} if shape_cond != 'any' else shapes_set()
            zone_cond = moved_zone(moved_cond)
            cond_zones = {zone_cond} if zone_cond != 'any' else zones_set()
            
            for o, poss_moves in pairs_dict.items():
                obj = get_obj(o, env)
                if obj.colour in cond_colours and obj.shape in cond_shapes:
                    poss_zones = {poss_move.putdown[-1] for poss_move in poss_moves}
                    matching_zones = poss_zones & cond_zones
                    dict_copy = dict(pairs_dict)
                    del dict_copy[o]
                    for x in matching_subseqs(moved_conds[1:], dict_copy, obl_obj_id, obl_obj_zones, env):
                        d = dict({o:matching_zones})
                        d.update(x) # Want o first in insertion order
                        yield d

# Modified from https://codereview.stackexchange.com/a/215329
def first_sublist_index_of(sub, l):
    for i in range(len(l) - len(sub) + 1):
        if l[i:(i+len(sub))] == sub:
            return i
    return None

# Need to put results into a set in case of duplicates
def violating_sub_permutations(order_constrained_subseqs):
    order_constrained_objects = {o for seqdict in order_constrained_subseqs for o in seqdict}
    for p in permutations(order_constrained_objects):
        for ss in order_constrained_subseqs:
            p_as_list = list(p)
            ss_seq = list(ss.keys())
            sublist_index = first_sublist_index_of(ss_seq, p_as_list)
            if sublist_index != None:
                all_zones = zones_set()
                options = (
                    [all_zones for i in range(sublist_index)] +
                    [ss[ss_seq[i]] for i in range(len(ss_seq))] +
                    [all_zones for i in range(len(p_as_list) - len(ss_seq) - sublist_index)]
                )
                for opt_seq in product(*options):
                    l = list(zip(p_as_list,opt_seq))
                    l2 = (l[:sublist_index] +
                            [FixedSeq(tuple(l[sublist_index:sublist_index+len(ss_seq)]))] +
                            l[sublist_index+len(ss_seq):])
                    yield tuple(l2)

def num_compliant_executions(all_compliant_dict, env):
    num_objects = len(all_compliant_dict)
    count_ignoring_unless = math.factorial(len(all_compliant_dict)) * reduce(mul, map(len, all_compliant_dict.values()))
    order_constrained_subseqs = []
    for um in unless_moves(all_compliant_dict):
        obl_obj_id, obl_obj_zones, moved_conds, pairs_dict = um
        mss = list(matching_subseqs(moved_conds, pairs_dict, obl_obj_id, obl_obj_zones, env))
        order_constrained_subseqs.extend(mss)
    order_constrained_objects = {o for seqdict in order_constrained_subseqs for o in seqdict} # repeated inside next fn call, but never mind!
    num_unconstrained_objects = num_objects - len(order_constrained_objects)
    vsp_set = set(violating_sub_permutations(order_constrained_subseqs))
    vsp_size = len(vsp_set)
    violated_seq_count = 0
    for vsp in vsp_set:
        vsp_len = len(vsp)
        # Count interleavings between seqs of length num_unconstrained_objects and vsp_len
        violated_seq_count = violated_seq_count + multinomial([num_unconstrained_objects, vsp_len])
    # Now consider permutations of the order unconstrained objects
    violated_seq_count = violated_seq_count * math.factorial(num_unconstrained_objects)
    print("Original count: {}".format(count_ignoring_unless))
    print("Violating seqs: {}".format(violated_seq_count))
    print("Remaining compliant count: {}".format(count_ignoring_unless - violated_seq_count))
    return count_ignoring_unless - violated_seq_count

# From https://stackoverflow.com/a/46374719
def multinomial(params):
    if len(params) == 1:
        return 1
    return binom(sum(params), params[-1]) * multinomial(params[:-1])

def history_matches_cond(hist, cond, env):
    # cond may partially specify each move
    if len(hist) != len(cond):
        return False
    else:
        return all((move_matches_moved_cond(hist[i], cond[i], env) for i in range(len(cond))))

def move_matches_moved_cond(move, moved_cond, env):
    assert isinstance(move,Sequence) and len(move)==2 and move[0][0]=='pickup' and move[1][0]=='putdown'
    assert isinstance(moved_cond,Sequence) and len(moved_cond)==4 and moved_cond[0]=='Moved'
    c = moved_colour(moved_cond)
    cond_colours = colours_set() if c=='any' else {c}
    sh = moved_shape(moved_cond)
    cond_shapes = shapes_set() if sh=='any' else {sh}
    z = moved_zone(moved_cond)
    cond_zones = zones_set() if z=='any' else {z}
    move_zone = move[1][2]
    oid = move[1][1]
    o = get_obj(oid, env)
    return o.colour in cond_colours and o.shape in cond_shapes and move_zone in cond_zones


    


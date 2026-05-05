def symm_groups_validation(symm_groups):
    try:
        for symm_group in symm_groups:
            for symm_pair in symm_group:
                if len(symm_pair) != 2:
                    raise Exception
    except Exception:
        raise ValueError("Symmetry groups are not well defined")


def symm_permutations(groups):
    if len(groups) > 0:
        head = groups[0]

        for tail_permutation in symm_permutations(groups[1:]):
            yield [head] + tail_permutation

        swapped_head = []
        for pair in head:
            swapped_head.append([pair[1], pair[0]])
        for tail_permutation in symm_permutations(groups[1:]):
            yield [swapped_head] + tail_permutation
    else:
        yield []


def swap_atoms(coordset_reference, atom_i, atom_j):
    coordset_reference[[atom_i, atom_j]] = coordset_reference[[atom_j, atom_i]]


def min_rmsd_of_rmsds_list(rmsds_list):
    return (rmsds_list.T).min(1)

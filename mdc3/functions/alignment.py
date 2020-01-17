from mdc3.types.datasets import Dataset
from mdc3.types.structures import StructureBiopython
from Bio import PDB


def align_datasets(reference_dataset: Dataset,
                   mobile_dataset: Dataset,
                   ) -> Dataset:

    reference_structure = reference_dataset.structure.structure

    mobile_structure = mobile_dataset.structure.structure

    alignment = align(reference_structure,
                      mobile_structure,
                      )
    # print("\tThe alignment matrix is: {}, {}".format(alignment.rotran[0], alignment.rotran[1]))

    alignment.apply(mobile_structure)

    aligned_dataset = Dataset(reflections=mobile_dataset.reflections,
                              structure=StructureBiopython(mobile_structure),
                              )

    return aligned_dataset

#
# def structures_common_set(reference_structure, structures):
#     ref_atoms = []
#     alt_atoms = []
#
#     list_of_chains = [[chain for chain in structure] for structure in structures]
#
#     for i, chain in enumerate(reference_structure):
#         chains = [list[i] for i in list_of_chains]
#
#         for res in chain:
#
#             if all():
#


def common_set(ref_structure, mobile_structure, name="CA"):
    def indicator(res):
        try:
            ca = res[name]
            return True
        except:
            return False

    ref_atoms = []
    alt_atoms = []
    # print(
    #     "\tAligning structure of {} residues against structure of {} residues".format(
    #         len(list(ref_structure.get_residues())),
    #         len(
    #             list(mobile_structure.get_residues())),
    #         )
    # )

    for (ref_model, alt_model) in zip(ref_structure, mobile_structure):
        for (ref_chain, alt_chain) in zip(ref_model, alt_model):

            ref_cas = {res.get_id()[1]: res[name] for res in ref_chain.get_residues() if indicator(res)}
            alt_cas = {res.get_id()[1]: res[name] for res in alt_chain.get_residues() if indicator(res)}

            for res_id, ca in ref_cas.items():
                if res_id in alt_cas.keys():
                    ref_atoms.append(ca)
                    alt_atoms.append(alt_cas[res_id])
                else:
                    print("\tWARNING: RESIDUE {} has no match".format(res_id))

    return ref_atoms, alt_atoms


def align(ref_structure, mobile_structure):

    # translation_mobile_to_ref = ref_structure.atoms.center_of_mass() - mobile_structure.atoms.center_of_mass()
    #
    #
    # mobile0 = mobile_structure.select_atoms('name CA').positions - mobile_structure.atoms.center_of_mass()
    # ref0 = ref_structure.select_atoms('name CA').positions - ref_structure.atoms.center_of_mass()
    # rotation_mobile_to_ref, rmsd = align.rotation_matrix(mobile0, ref0)

    # ref_atoms = []
    # alt_atoms = []

    # for atom in ref_structure.get_atoms():
    #     if atom.name == "CA":
    #         ref_atoms.append(atom)
    #
    # for atom in mobile_structure.get_atoms():
    #     if atom.name == "CA":
    #         alt_atoms.append(atom)


    # for (ref_model, alt_model) in zip(ref_structure, mobile_structure):
    #     for (ref_chain, alt_chain) in zip(ref_model, alt_model):
    #         for ref_res, alt_res in zip(ref_chain, alt_chain):
    #
    #             # CA = alpha carbon
    #             # print("\tModel: {}".format(ref_model))
    #             # print("\tChain: {}".format(ref_chain))
    #             # print("\tResidue: {}".format(ref_res))
    #
    #             print(ref_res)
    #             print(alt_res)
    #             # print(dir(ref_res))
    #             # print([x for x in ref_res.get_atoms()])
    #             ref_atoms.append(ref_res['CA'])
    #             alt_atoms.append(alt_res['CA'])

    ref_atoms, alt_atoms = common_set(ref_structure, mobile_structure)

    # print("\tAligning {} atoms agianst {} atoms".format(len(ref_atoms),
    #                                                     len(alt_atoms),
    #                                                     )
    #       )

    super_imposer = PDB.Superimposer()
    super_imposer.set_atoms(ref_atoms,
                            alt_atoms,
                            )

    return super_imposer
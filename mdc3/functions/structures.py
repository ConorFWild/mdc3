import clipper_python


def translate_structure(structure, rotation, translation):

    for atom in structure.structure.get_atoms():
        atom.transform(rotation, translation)

    return structure
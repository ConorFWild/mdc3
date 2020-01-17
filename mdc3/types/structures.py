from pathlib import Path

from biopandas.pdb import PandasPdb

import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd
from MDAnalysis.coordinates.PDB import PDBReader

from Bio.PDB.Structure import Structure
from Bio import PDB

from .files import PDBFile


class StructureBioPandas:
    structure: PandasPdb

    def __init__(self,
                 structure: PandasPdb,
                 ) -> None:
        self.structure = structure


def structure_biopandas_from_pdb(pdb_file: PDBFile) -> StructureBioPandas:

    structure = PandasPdb().read_pdb(str(pdb_file.path))

    return StructureBioPandas(structure)


class StructureMDAnalysis:
    structure: mda.Universe

    def __init__(self,
                 structure: mda.Universe,
                 ) -> None:
        self.structure = structure


def structure_mdanalysis_from_pdb(pdb_file: PDBFile) -> StructureMDAnalysis:

    # pdb = PDBReader(str(pdb_file.path))
    structure = mda.Universe(str(pdb_file.path))
    # structure = PDBReader(str(pdb_file.path))

    return StructureMDAnalysis(structure)


class StructureBiopython:
    structure: Structure

    def __init__(self,
                 structure: Structure,
                 ) -> None:
        self.structure = structure


    def output(self, path: Path):
        io = PDB.PDBIO()
        io.set_structure(self.structure)
        io.save(str(path))



def structure_biopython_from_pdb(pdb_file: PDBFile):
    structure = PDB.PDBParser().get_structure("x", str(pdb_file.path),)

    return StructureBiopython(structure)

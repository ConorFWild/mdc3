from typing import (Dict,
                    List,
                    Union,
                    Any,
                    )

from pathlib import Path

from .files import (MTZFile, PDBFile, )
from .structures import StructureBioPandas, structure_biopandas_from_pdb, structure_mdanalysis_from_pdb, structure_biopython_from_pdb
from .reflections import Reflections, reflections_from_mtz


class Dataset:
    reflections: Reflections
    structure: Union[StructureBioPandas]

    def __init__(self,
                 reflections: Reflections,
                 structure: Union[StructureBioPandas],
                 ) -> None:
        self.reflections = reflections
        self.structure = structure


class MultiCrystalDataset:
    datasets: Dict[str, Dataset]

    def __init__(self,
                 datasets: Dict[str, Dataset],
                 ) -> None:
        self.datasets = datasets

    @classmethod
    def mcd_from_pandda_input_dir(MultiCrystalDataset,
                                  directory: Path = Path("."),
                                  pdb_type: str = "Biopython",
                                  pdb_regex: str = "dimple.pdb",
                                  mtz_regex: str = "dimple.mtz",
                                  ):

        dataset_paths_dict = parse_pandda_input(directory,
                                                pdb_regex,
                                                mtz_regex,
                                                )

        datasets = {}
        for dtag in dataset_paths_dict:
            reflections = reflections_from_mtz(MTZFile(dataset_paths_dict[dtag]["mtz_path"]))
            if pdb_type == "MDAnalysis":
                structure = structure_mdanalysis_from_pdb(PDBFile(dataset_paths_dict[dtag]["pdb_path"]))
            if pdb_type == "Biopython":
                structure = structure_biopython_from_pdb(PDBFile(dataset_paths_dict[dtag]["pdb_path"]))

            else:
                structure = structure_biopandas_from_pdb(PDBFile(dataset_paths_dict[dtag]["pdb_path"]))

            datasets[dtag] = Dataset(reflections,
                                     structure,
                                     )


        return MultiCrystalDataset(datasets)


def parse_pandda_input(path: Path,
                       pdb_regex: str = "dimple.pdb",
                       mtz_regex: str = "dimple.mtz",
                       ) -> Dict[str, Dict[str, Path]]:
    dataset_paths = path.glob("*")

    datasets = {}
    for dataset_path in dataset_paths:
        try:

            pdb_path = next(dataset_path.glob(pdb_regex))
            mtz_path = next(dataset_path.glob(mtz_regex))
            datasets[dataset_path.name] = {"pdb_path": pdb_path,
                                           "mtz_path": mtz_path,
                                           }
        except:
            continue

    return datasets


def parse_pandda_input_for_regex(path: Path,
                                 regex: str = "dimple.pdb",
                       ) -> Dict[str, Dict[str, Path]]:
    dataset_paths = path.glob("*")

    datasets = {}
    for dataset_path in dataset_paths:
        try:

            regex_path = next(dataset_path.glob(regex))
            datasets[dataset_path.name] = {"path": regex_path,
                                           }
        except:
            continue

    return datasets

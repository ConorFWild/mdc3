from typing import Dict, Tuple

import hypothesis

from pathlib import Path


from mdc3.types.files import MTZFile, PDBFile
from mdc3.types.datasets import MultiCrystalDataset, Dataset
from mdc3.types.reflections import reflections_from_mtz
from mdc3.types.structures import structure_biopandas_from_pdb

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


@hypothesis.strategies.composite
def example_datasets(draw,
            min_size: int = 60,
            max_size: int = 130,
            directory: Path = Path("."),
            ) -> MultiCrystalDataset:

    dataset_paths_dict = parse_pandda_input(directory)

    paths_strategy = hypothesis.strategies.sampled_from([x for x in dataset_paths_dict.keys()])

    dataset_paths_subset = draw(hypothesis.strategies.lists(paths_strategy,
                                                            unique=True,
                                                            min_size=min_size,
                                                            max_size=max_size,
                                                            )
                                )

    datasets = {dtag: Dataset(reflections_from_mtz(MTZFile(dataset_paths_dict[dtag]["mtz_path"])),
                              structure_biopandas_from_pdb(PDBFile(dataset_paths_dict[dtag]["pdb_path"]))
                              )
                for dtag
                in dataset_paths_subset
                }

    return MultiCrystalDataset(datasets)


def test_example_datasets():
    strategy = example_datasets(min_size=5,
                                max_size=15,
                                directory=Path("/dls/labxchem/data/2018/lb19758-9/processing/analysis/initial_model"))

    print(strategy)
    datasets =strategy.example()
    print(datasets)
    print(datasets.datasets)

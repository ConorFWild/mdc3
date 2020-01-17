from hypothesis import given, settings
from hypothesis.strategies import just

from pathlib import Path

from mdc3.types.files import (PDBFile,
                              MTZFile,
                              )
from mdc3.types.structures import structure_biopandas_from_pdb
from mdc3.types.reflections import (Reflections,
                                    reflections_from_mtz,
                                    new_reflections_from_reflections_at_res,
                                    )


@given(just(PDBFile(Path("../../data/dimple.pdb").resolve())))
def test_structure_biopandas_from_pdb(pdb_file: PDBFile) -> None:
    structure_biopandas_from_pdb(pdb_file)


@given(just(MTZFile(Path("../../data/dimple.mtz").resolve())))
def test_reflections_from_mtz(mtz_file: MTZFile) -> None:
    reflections_from_mtz(mtz_file)


@settings(deadline=1000)
@given(just(reflections_from_mtz(MTZFile(Path("../../data/dimple.mtz").resolve()))),
       just(2),
       )
def test_new_reflections_from_reflections_at_res(reflections: Reflections,
                                                 resolution: float,
                                                 ) -> None:
    print(reflections.hkl_data.data[0].shape)
    new_reflections = new_reflections_from_reflections_at_res(reflections,
                                                              resolution,
                                                              )

    print(new_reflections.hkl_data.data[0].shape)
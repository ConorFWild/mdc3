import hypothesis
from hypothesis import (given,
                        settings,
                        )
from hypothesis.strategies import just

from pathlib import Path

import numpy as np

import clipper_python

from mdc3.types.files import (PDBFile,
                              MTZFile,
                              )
from mdc3.types.datasets import Dataset, MultiCrystalDataset
from mdc3.types.structures import structure_biopandas_from_pdb
from mdc3.types.reflections import (Reflections,
                                    reflections_from_mtz,
                                    HKLList,
reflections_from_hkl_list,
                                    )

from mdc3.functions.dataset_transforms import (truncate_diffractions,
                                               get_missing_reflections,
                                               get_union_missing_reflections,
                                               b_factor_smoothing_real_space,
                                               )


from .strategies import example_datasets


@settings(deadline=100000,
          suppress_health_check=[hypothesis.HealthCheck.too_slow],
          max_examples=1,
          )
@given(example_datasets(min_size=5,
                        max_size=10,
                        directory=Path("/dls/labxchem/data/2018/lb19758-9/processing/analysis/initial_model")
                        )
       )
def test_b_factor_smoothing_real_space(mcd: MultiCrystalDataset) -> None:
    values = list(mcd.datasets.values())
    reference_reflections = values[0].reflections
    reflections = values[1].reflections
    b_factor_smoothing_real_space(reference_reflections,
                                  reflections,
                                  )


@settings(deadline=100000,
          suppress_health_check=[hypothesis.HealthCheck.too_slow],
          max_examples=1,
          )
@given(example_datasets(min_size=500,
                        max_size=501,
                        directory=Path("/dls/labxchem/data/2018/lb19758-9/processing/analysis/initial_model")
                        )
       )
def test_truncate_dataset(mcd: MultiCrystalDataset) -> None:

    reflections_list = [dataset.reflections for dtag, dataset in mcd.datasets.items()]

    print(mcd.datasets)

    common_missing_reflections = get_union_missing_reflections(reflections_list)
    print(common_missing_reflections)

    truncated_reflections = []
    for reflections in reflections_list:
        truncated_reflections.append(truncate_diffractions(reflections,
                                                           list(common_missing_reflections.values())
                                                           )
                                     )

    print(get_missing_reflections(reflections_list[0]))
    print(get_missing_reflections(truncated_reflections[0]))


#
# @settings(deadline=1000)
# @given(just(reflections_from_mtz(MTZFile(Path("../../data/dimple_2.mtz").resolve()))),
#        just(reflections_from_mtz(MTZFile(Path("../../data/dimple.mtz").resolve()))),
#        )
# def test_truncate_diffractions(reference_reflections: Reflections,
#                                reflections: Reflections,
#                                ) -> None:
#
#     print(get_missing_reflections(reflections))
#     print(get_missing_reflections(reference_reflections))
#
#     common_missing_reflections = get_union_missing_reflections([reflections,
#                                                             reference_reflections,
#                                                             ]
#                                                            )
#     print("common missing reflections: {}".format(common_missing_reflections))
#
#     truncated_reflections = truncate_diffractions(reference_reflections,
#                                                   list(common_missing_reflections.values()),
#                                                   )
#
#     print(get_missing_reflections(truncated_reflections))
#     print(get_missing_reflections(reflections))
#     print(get_missing_reflections(reference_reflections))
#
#
# @settings(deadline=1000)
# @given(just(reflections_from_mtz(MTZFile(Path("../../data/dimple_2.mtz").resolve()))),
#        just(reflections_from_mtz(MTZFile(Path("../../data/dimple.mtz").resolve()))),
#        )
# def test_get_union_missing_reflections(reference_reflections: Reflections,
#                                reflections: Reflections,
#                                ) -> None:
#     common_missing_reflections = get_union_missing_reflections([reflections,
#                                                             reference_reflections,
#                                                             ]
#                                                            )
#     print(common_missing_reflections)
#
#
# @settings(deadline=1000)
# @given(just(reflections_from_mtz(MTZFile(Path("../../data/dimple.mtz").resolve()))))
# def test_get_missing_reflections(reflections: Reflections) -> None:
#
#     missing_reflections = get_missing_reflections(reflections)
#
#     print(missing_reflections)
#
#
#
# @settings(deadline=1000)
# @given(just(reflections_from_mtz(MTZFile(Path("../../data/dimple.mtz").resolve()))),
#        just(HKLList([clipper_python.HKL(0, 0, 0),
#                      clipper_python.HKL(0, 0, 6),
#                      ]
#                     )
#             ),
#        )
# def test_reflections_from_hkl_list(reflections: Reflections,
#                                    hkl_list: HKLList,
#                                ) -> None:
#
#     print(reflections.hkl_data.data[0].shape)
#     print(reflections.hkl_data.data)
#
#     new_reflections = reflections_from_hkl_list(reflections, hkl_list)
#
#     print(new_reflections.hkl_data.data[0].shape)
#
#     print(new_reflections.hkl_data.data)

#
# @settings(deadline=1000)
# @given(just(reflections_from_mtz(MTZFile(Path("../../data/dimple_2.mtz").resolve()))),
#        just(reflections_from_mtz(MTZFile(Path("../../data/dimple.mtz").resolve()))),
#        )
# def test_truncate_diffractions(reference_reflections: Reflections,
#                                reflections: Reflections,
#                                ) -> None:
#
#     # print(reference_reflections.hkl_data.data)
#     # print(reflections.hkl_data.data)
#     new_reflections = truncate_diffractions(reference_reflections, reflections)
#
#     reference_reflections_missing_indexes = np.nonzero(np.isnan(reference_reflections.hkl_data.data[1][:,0]))
#     reflections_missing_indexes = np.nonzero(np.isnan(reflections.hkl_data.data[1][:,0]))
#     new_reflections_missing_indexes = np.nonzero(np.isnan(new_reflections.hkl_data.data[1][:,0]))
#
#     print(reference_reflections_missing_indexes)
#     print(reference_reflections.hkl_data.data[0][reference_reflections_missing_indexes[0], :])
#
#     print(reflections_missing_indexes)
#     print(reflections.hkl_data.data[0][reflections_missing_indexes[0], :])
#
#     print(new_reflections_missing_indexes)
#     print(new_reflections.hkl_data.data[0][new_reflections_missing_indexes[0], :])
#     print(new_reflections.hkl_data.data[1])
#
#     # print(reference_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].missing)
#     # print(reflections.hkl_data[clipper_python.HKL(20, 1, 69)].missing)
#     # print(new_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].missing)
#
#     # print(reference_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].a)
#     # print(reflections.hkl_data[clipper_python.HKL(20, 1, 69)].a)
#     # print(new_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].a)
#     #
#     # print(reference_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].b)
#     # print(reflections.hkl_data[clipper_python.HKL(20, 1, 69)].b)
#     # print(new_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].b)
#
#
#     # Postcondition
#     # reflections_hkl = [tuple(x for x in coord)
#     #                    for coord
#     #                    in [row for row in reflections.hkl_data.data[0]]]
#     # reference_reflections_hkl = [tuple(x for x in coord)
#     #                              for coord
#     #                              in [row for row in reference_reflections.hkl_data.data[0]]]
#     # new_reflections_hkl = [tuple(x for x in coord)
#     #                        for coord
#     #                        in [row for row in new_reflections.hkl_data.data[0]]]
#
#
#

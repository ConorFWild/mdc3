from typing import Dict, Tuple, List

import numpy as np
from scipy import ndimage
from scipy import optimize


import clipper_python

from ..types.reflections import (Reflections, hkl_to_tuple, new_reflections_from_reflections,)
from ..types.datasets import Dataset, MultiCrystalDataset


def get_missing_reflections(reflections: Reflections) -> Dict[Tuple[int], clipper_python.HKL]:

    missing_reflections = {}

    index = reflections.hkl_info.first
    while not index.last():

        if reflections.hkl_data[index].missing:
            missing_reflections[hkl_to_tuple(index.hkl)] = index.hkl

        index.next()

    return missing_reflections


def get_union_missing_reflections(reflections_list: List[Reflections]) -> Dict[Tuple[int], clipper_python.HKL]:

    common_missing_reflections: Dict[Tuple[int], clipper_python.HKL] = {}
    for reflections in reflections_list:
        missing_reflections = get_missing_reflections(reflections)
        common_missing_reflections.update(missing_reflections)

    return common_missing_reflections


def truncate_diffractions(reflections: Reflections,
                         hkl_to_truncate: List[clipper_python.HKL],
                         ) -> Reflections:
    new_reflections = new_reflections_from_reflections(reflections)

    for hkl in hkl_to_truncate:
        try:
            # print(hkl.hkl)
            new_reflections.hkl_data[hkl].set_null()

        except Exception as e:
            # print(e)
            pass

    return new_reflections


def b_factor_smoothing_real_space(reference_reflections: Reflections,
                             reflections: Reflections,
                             ):

    print("Reference_res: {}; Res: {}".format(reference_reflections.hkl_info.resolution.limit,
                                              reflections.hkl_info.resolution.limit,
                                              )
          )
    if reference_reflections.hkl_info.resolution.limit < reflections.hkl_info.resolution.limit:
        raise AssertionError("Reference reflections MUST be lower than reflections resolution")

    spacegroup = reference_reflections.hkl_info.spacegroup
    cell =reference_reflections.hkl_info.cell
    sample_res = reference_reflections.hkl_info.resolution
    grid = clipper_python.Grid_sampling(spacegroup,
                                        cell,
                                        sample_res,
                                        )

    xmap_reference = clipper_python.Xmap_float(spacegroup,
                                               cell,
                                               grid,
                                               )
    xmap_reference.fft_from(reference_reflections.hkl_data)
    xmap = clipper_python.Xmap_float(spacegroup,
                                               cell,
                                               grid,
                                               )
    xmap.fft_from(reflections.hkl_data)

    xmap_reference_np = xmap_reference.export_numpy()
    xmap_np = xmap.export_numpy()

    print(xmap_reference_np.shape)
    print(xmap_np.shape)

    # optimise blur of xmap
    # target_func =
    ndimage.gaussian_filter()

    # return it to xmap

    # inv fft





def dep_scale_diffractions(reference_reflections: Reflections,
                       reflections: Reflections,
                       ):

    new_reflections = new_reflections_from_reflections(reflections)

    reference_reflections_np  = reflections_as_np_ndarray(reference_reflections)
    reflections_np = reflections_as_np_ndarray(reflections)

    intensity_array_np = np.linalg.norm(reference_reflections_np,
                                        axis=3)

    target = lambda sigma: np.linalg.norm(reference_reflections_np - ndimage.gaussian_filter(reflections_np,
                                                                                             sigma=sigma)
                                          )

    result = optimize.minimize_scalar(target)

    hkl_np, new_data_np = np_ndarray_as_reflections_np(reflections,
                                                             result.x,
                                                       )

    new_reflections.hkl_data.set_data((hkl_np,
                                       new_data_np,
                                       )
                                      )


    return new_reflections


def reflections_as_np_ndarray(reflections: Reflections) -> np.ndarray:
    hkl_np, data_np = reflections.hkl_data.data()

    ndarray_np = np.zeros((np.max(hkl_np[:, 0]-np.min(hkl_np[:, 0])),
                           np.max(hkl_np[:, 1]-np.min(hkl_np[:, 1])),
                           np.max(hkl_np[:, 2]-np.min(hkl_np[:, 2])),)
                          )

    ndarray_np[hkl_np] = data_np

    return ndarray_np


def np_ndarray_as_reflections_np(reflections: Reflections,
                                 new_data_ndarray_np: np.ndarray,
                                 ) -> np.ndarray:

    new_hkl, old_data = reflections.hkl_data.data()

    new_data_np =0

    return new_hkl, new_data_np


def scale(new_intensities, old_intensities, complex_np):

    complex_np * (np.divide(new_intensities,
                            old_intensities,
                            where=(old_intensities != 0),
                            )
                  )



# def dep_truncate_diffractions(reference_reflections: Reflections,
#                           reflections: Reflections,
#                           ) -> Reflections:
#     new_info = clipper_python.HKL_info(reflections.hkl_info.spacegroup,
#                                        reflections.hkl_info.cell,
#                                        reflections.hkl_info.resolution,
#                                        True,
#                                        )
#     index = new_info.first
#     # print(index)
#     # print(index.last())
#
#
#     new_data = clipper_python.data32.HKL_data_F_phi_float(reflections.hkl_data)
#
#     # print(index.last())
#     # while not index.last():
#     #
#     #     new_data[index] = reflections.hkl_data[index]
#     #     # print(reflections.hkl_data[index])
#     #     # print(new_data[index])
#     #
#     #     index.next()
#     #     print(index.last())
#
#     # reference_reflections_missing_mask = np.isnan(reference_reflections.hkl_data.data[1][:, 0])
#     # reflections_missing_mask = np.isnan(reflections.hkl_data.data[1][:, 0])
#     #
#     # reference_reflections_missing_indexes = np.nonzero()
#     # reflections_missing_indexes = np.nonzero()
#
#     new_data.set_data(reflections.hkl_data.data[0],
#                       reflections.hkl_data.data[1],
#                       )
#     #
#     # print("HERE!")
#     # print(new_data[clipper_python.HKL(20, 1, 69)].b)
#     # print("reference HERE!")
#     # print(reference_reflections.hkl_data[clipper_python.HKL(20, 1, 69)].missing)
#     # print("original HERE!")
#     # print(reflections.hkl_data[clipper_python.HKL(20, 1, 69)].missing)
#
#
#
#     # print(new_data.data)
#     # new_reflections_missing_indexes = np.nonzero(np.isnan(new_data.data[1][:, 0]))
#     # print(new_data.data[0][new_reflections_missing_indexes[0], :])
#     # print(new_data.data[1])
#
#     # Mask by old data
#     # print(reference_reflections.hkl_data)
#     new_data.mask(reference_reflections.hkl_data)
#     # indexes = []
#     # while not index.last():
#     #
#     #     # Check whether data missing
#     #
#     #     # Check whether in other dataset
#     #     try:
#     #         if reference_reflections.hkl_data[index.hkl].missing:
#     #             print(index.hkl)
#     #         else:
#     #             indexes.append(index.hkl)
#     #     except:
#     #         print(index.hkl)
#     #
#     #     #
#     #     #
#     #     #
#     #     #
#     #     # try:
#     #     #     if reference_reflections.hkl_data[index.hkl].missing:
#     #     #
#     #     #         print("setting m,issing")
#     #     #         # print(dir(clipper_python.data32))
#     #     #         print("hkl: {}".format(index.hkl))
#     #     #         print("reference a: {}".format(reference_reflections.hkl_data[index.hkl].a))
#     #     #
#     #     #         new_data.__setitem__(index.hkl, clipper_python.data32.F_phi_float())
#     #     #         # new_data.update()
#     #     #         print(new_data[index].a)
#     #     #     # print(reflections.hkl_data[index])
#     #     #     # print(new_data[index])
#     #     # except:
#     #     #     print("hkl: {}".format(index.hkl))
#     #     #
#     #     #     new_data.__setitem__(index.hkl, clipper_python.data32.F_phi_float())
#     #     index.next()
#     #
#     # for missing_index in indexes:
#     #     new_data[missing_index] = clipper_python.data32.F_phi_float()
#
#     # print("HERE!")
#     # print(new_data[clipper_python.HKL(20, 1, 69)].b)
#
#     return Reflections(new_info,
#                        new_data,
#                        )

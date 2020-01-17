from typing import Tuple, List, Dict

import numpy as np

import clipper_python
from clipper_python import Resolution

from .files import MTZFile
from mdc3.types.crystalographic import (cell_from_state,
                                        cell_to_state,
                                        spacegroup_from_state,
                                        spacegroup_to_state,
                                        resolution_from_state,
                                        resolution_to_state,
                                        )


class HKLList:
    hkl_list: List[clipper_python.HKL]

    def __init__(self,
                 hkl_list: List[clipper_python.HKL],
                 ) -> None:

        self.hkl_list = hkl_list


class Reflections:
    hkl_info: clipper_python.HKL_info
    hkl_data: clipper_python.data32.HKL_data_F_phi_float

    def __init__(self,
                 hkl_info: clipper_python.HKL_info,
                 hkl_data: clipper_python.data32.HKL_data_F_phi_float,
                 ) -> None:
        self.hkl_info = hkl_info
        self.hkl_data = hkl_data

    def __getstate__(self):

        spacegroup = self.hkl_info.spacegroup
        cell = self.hkl_info.cell
        resolution = self.hkl_info.resolution.limit
        # data = self.hkl_data.as_numpy()
        # self.hkl_data.get_data(data)
        # print(np.std(data))
        # print(self.hkl_data.getData())
        data = self.hkl_data.data
        # print("Reflections data is: {}".format(data))


        state = {"spacegroup": spacegroup_to_state(spacegroup),
                 "cell": cell_to_state(cell),
                 "resolution": resolution_to_state(Resolution(resolution)),
                 "data": data,
                 }

        return state

    def __setstate__(self, state):
        spacegroup = spacegroup_from_state(state["spacegroup"])
        cell = cell_from_state(state["cell"])
        resolution = resolution_from_state(state["resolution"])
        self.hkl_info = clipper_python.HKL_info(spacegroup,
                                                cell,
                                                resolution,
                                                True,
                                                )
        self.hkl_data = clipper_python.data32.HKL_data_F_phi_float(self.hkl_info)
        # print(state["data"])
        # print(np.std(state["data"]))
        self.hkl_data.set_data(state["data"][0],
                               state["data"][1],
                               )
        # print(np.std(self.hkl_data.as_numpy()))


def reflections_from_mtz(mtz_file: MTZFile) -> Reflections:

    mtz_file.mtz.open_read(str(mtz_file.path))

    hkl_info = clipper_python.HKL_info()
    mtz_file.mtz.import_hkl_info(hkl_info)

    # hkl_data = clipper_python.HKL_data_F_phi(hkl_info)
    hkl_data = clipper_python.data32.HKL_data_F_phi_float(hkl_info)
    mtz_file.mtz.import_hkl_data(hkl_data, "*/*/[FWT,PHWT]")

    mtz_file.mtz.close_read()

    return Reflections(hkl_info,
                       hkl_data,
                       )


def reflections_from_hkl_list(reflections: Reflections,
                             hkl_list: HKLList,
                             ) -> Reflections:

    new_reflections = new_reflections_from_reflections(reflections)

    old_hkl_array, old_data_array = new_reflections.hkl_data.data

    new_hkl_indicies = [new_reflections.hkl_info.index_of(hkl)
                        for hkl
                        in hkl_list.hkl_list
                        ]

    new_hkl_array = old_hkl_array[new_hkl_indicies, :]
    new_data_array = old_data_array[new_hkl_indicies, :]

    print(new_hkl_array)
    print(new_data_array)

    new_reflections.hkl_data.set_data(new_hkl_array,
                                      new_data_array,
                                      )

    print(new_reflections.hkl_data.data)

    return new_reflections


def new_reflections_from_reflections(reflections: Reflections) -> Reflections:
    new_hkl_info = clipper_python.HKL_info(reflections.hkl_info.spacegroup,
                                           reflections.hkl_info.cell,
                                           reflections.hkl_info.resolution,
                                           True,
                                           )

    new_hkl_data = clipper_python.data32.HKL_data_F_phi_float(reflections.hkl_data)

    old_hkl_array, old_data_array = reflections.hkl_data.data

    new_hkl_data.set_data(old_hkl_array,
                          old_data_array,
                          )

    return Reflections(new_hkl_info,
                       new_hkl_data,
                       )


def new_reflections_from_reflections_at_res(reflections: Reflections,
                                            resolution: float,
                                            ) -> Reflections:
    new_hkl_info = clipper_python.HKL_info(reflections.hkl_info.spacegroup,
                                           reflections.hkl_info.cell,
                                           clipper_python.Resolution(resolution),
                                           True,
                                           )

    new_hkl_data = clipper_python.data32.HKL_data_F_phi_float(new_hkl_info)


    index = new_hkl_info.first
    while not index.last():
        try:
            new_hkl_data[index.hkl] = reflections.hkl_data[index.hkl]
        except:
            pass
        index.next()

    return Reflections(new_hkl_info,
                       new_hkl_data,
                       )


def hkl_to_tuple(hkl: clipper_python.HKL) -> Tuple[int]:
    return tuple(x for x in hkl.hkl)


def tuple_to_hkl(tup: Tuple[int]) -> clipper_python.HKL:
    return clipper_python.HKL(tup[0],
                              tup[1],
                              tup[2],
                              )
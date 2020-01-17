from typing import Union

from pathlib import Path

import numpy as np

from clipper_python import (Grid_sampling,
                            # Xmap_float
                            Xmap,
                            Resolution,
                            CCP4MAPfile,
                            )
# from clipper_python import Xmap_float as Xmap

from mdc3.types.datasets import Dataset
from mdc3.types.reflections import Reflections
from mdc3.types.crystalographic import (cell_from_state,
                                        cell_to_state,
                                        spacegroup_from_state,
                                        spacegroup_to_state,
                                        resolution_from_state,
                                        resolution_to_state,
                                        )


class MCDXMap:
    # xmap: Xmap_float
    xmap: Xmap

    def __init__(self,
                 xmap: Xmap
                 ) -> None:

        # xmap = Xmap_float(spacegroup,
        #                   cell,
        #                   grid,
        #                   )
        self.xmap = xmap

    def __getstate__(self):
        spacegroup = self.xmap.spacegroup
        cell = self.xmap.cell
        # resolution = self.xmap.
        grid = self.xmap.grid
        data = np.zeros((grid.nu(),
                         grid.nv(),
                         grid.nw(),
                         ),
                        dtype="double",
                        )
        self.xmap.export_numpy(data)
        print("got state as: {}".format(np.std(data)))
        state = {"spacegroup": spacegroup_to_state(spacegroup),
                 "cell": cell_to_state(cell),
                 # "resolution": resolution_to_state(Resolution(resolution)),
                 "grid": (grid.nu(), grid.nv(), grid.nw()),
                 "data": data,
                 }

        return state

    def __setstate__(self, state):
        spacegroup = spacegroup_from_state(state["spacegroup"])
        cell = cell_from_state(state["cell"])
        # resolution = resolution_from_state(state["resolution"])
        # self.xmap = Xmap(spacegroup,
        #                  cell,
        #                  resolution)
        grid_params = state["grid"]
        grid = Grid_sampling(grid_params[0], grid_params[1], grid_params[2])
        self.xmap = Xmap(spacegroup,
                         cell,
                         grid,
                         )

        print(np.std(state["data"]))

        self.xmap.import_numpy(state["data"])

    @staticmethod
    def xmap_from_dataset(dataset: Dataset, resolution: Union[Resolution, None] = None):
        reflections = dataset.reflections
        return MCDXMap.xmap_from_reflections(reflections, resolution)

    @staticmethod
    def xmap_from_reflections(reflections: Reflections, resolution: Union[Resolution, None] = None):
        spacegroup = reflections.hkl_info.spacegroup
        cell = reflections.hkl_info.cell
        if resolution is None:
            resolution = reflections.hkl_info.resolution
        hkl_data = reflections.hkl_data

        return MCDXMap.xmap_from_clipper(spacegroup, cell, resolution, hkl_data)

    @staticmethod
    def xmap_from_clipper(spacegroup,
                          cell,
                          resolution,
                          hkl_data,
                          ):
        grid = Grid_sampling(spacegroup,
                             cell,
                             resolution,
                             )
        xmap = Xmap(spacegroup,
                    cell,
                    grid,
                    )

        xmap.fft_from(hkl_data)

        return MCDXMap(xmap)

    @staticmethod
    def xmap_from_numpy(spacegroup,
                        cell,
                        grid_params,
                        numpy_data,
                        ):
        grid = Grid_sampling(grid_params[0],
                             grid_params[1],
                             grid_params[2],
                             )
        xmap = Xmap(spacegroup,
                    cell,
                    grid,
                    )
        xmap.import_numpy(numpy_data)

        return MCDXMap(xmap)

    def to_ccp4(self, path: Path) -> None:
        mapout = CCP4MAPfile()
        mapout.open_write(str(path))
        mapout.export_xmap_double(self.xmap)
        mapout.close_write()


def xmap_to_numpy_crystalographic_axis(xmap: MCDXMap) -> np.ndarray:
    grid = xmap.xmap.grid
    grid_params = (grid.nu(), grid.nv(), grid.nw())

    xmap_np = np.zeros(grid_params, dtype="double")
    xmap.xmap.export_numpy(xmap_np)

    return xmap_np


def xmap_to_numpy_cartesian_axis(xmap: MCDXMap) -> np.ndarray:

    xmap_np = xmap.xmap.export_interpolated_box_numpy()

    return xmap_np


def xmap_from_dataset(dataset: Dataset, resolution: Union[Resolution, None] = None) -> MCDXMap:
    reflections = dataset.reflections

    spacegroup = reflections.hkl_info.spacegroup
    cell = reflections.hkl_info.cell
    if resolution is None:
        resolution = reflections.hkl_info.resolution
    hkl_data = reflections.hkl_data

    grid = Grid_sampling(spacegroup,
                         cell,
                         resolution,
                         )
    xmap = Xmap(spacegroup,
                cell,
                grid,
                )

    xmap.fft_from(hkl_data)

    return MCDXMap(xmap)
from typing import Union, Tuple

from pathlib import Path

import numpy as np

import clipper_python
from clipper_python import (Grid_sampling,
                            Xmap_float,
                            Resolution,
                            CCP4MAPfile,
                            NXmap_float,
                            RTop_orth,
                            Mat33_float,
                            Vec3_float,
                            Mat33_double,
                            Vec3_double,
                            Coord_grid,
                            Cell,
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
    xmap: Xmap_float

    def __init__(self,
                 xmap: Xmap_float
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
        grid = self.xmap.grid_sampling
        # data = np.zeros((grid.nu,
        #                  grid.nv,
        #                  grid.nw,
        #                  ),
        #                 dtype="double",
        #                 )
        data = self.xmap.export_numpy()
        # print("got state as: {}".format(np.std(data)))
        state = {"spacegroup": spacegroup_to_state(spacegroup),
                 "cell": cell_to_state(cell),
                 "grid": (grid.nu, grid.nv, grid.nw),
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
        self.xmap = Xmap_float(spacegroup,
                               cell,
                               grid,
                               )

        # print(np.std(state["data"]))

        self.xmap.import_numpy(state["data"])
        # print("std after import is: {}".format(np.std(self.xmap.export_numpy())))

    @staticmethod
    def xmap_from_dataset(dataset: Dataset,
                          resolution: Union[Resolution, None] = None,
                          grid_params: Union[Tuple[int, int, int], None] = None,
                          ):
        reflections = dataset.reflections
        return MCDXMap.xmap_from_reflections(reflections, resolution, grid_params)

    @staticmethod
    def xmap_from_reflections(reflections: Reflections,
                              resolution: Union[Resolution, None] = None,
                              grid_params: Union[Tuple[int, int, int], None] = None,
                              ):
        spacegroup = reflections.hkl_info.spacegroup
        cell = reflections.hkl_info.cell
        # if resolution is None:
        #     resolution = reflections.hkl_info.resolution
        hkl_data = reflections.hkl_data
        if resolution:
            return MCDXMap.xmap_from_clipper_res(spacegroup, cell, resolution, hkl_data)
        if grid_params:
            return MCDXMap.xmap_from_clipper_grid_params(spacegroup, cell, grid_params, hkl_data)

    @staticmethod
    def xmap_from_clipper_res(spacegroup,
                              cell,
                              resolution,
                              hkl_data,
                              ):
        grid = Grid_sampling(spacegroup,
                             cell,
                             resolution,
                             )

        # print("Xmap params: {}. {}, {}, {}, {}, {}, {}".format(spacegroup.spacegroup_number,
        #                                                        resolution.limit,
        #                                                        grid.nu,
        #                                                        grid.nv,
        #                                                        grid.nw,
        #                                                        cell.dim,
        #                                                        cell.angles,
        #                                                        )
        #       )

        xmap = Xmap_float(spacegroup,
                          cell,
                          grid,
                          )

        xmap.fft_from(hkl_data)

        return MCDXMap(xmap)

    @staticmethod
    def xmap_from_clipper_grid_params(spacegroup,
                                      cell,
                                      grid_params,
                                      hkl_data,
                                      ):
        grid = Grid_sampling(grid_params[0],
                             grid_params[1],
                             grid_params[2],
                             )

        xmap = Xmap_float(spacegroup,
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

        xmap = Xmap_float(spacegroup,
                          cell,
                          grid,
                          )

        xmap.import_numpy(numpy_data)

        return MCDXMap(xmap)

    def to_ccp4(self, path: Path) -> None:
        mapout = CCP4MAPfile()
        # print(dir(mapout))
        mapout.open_write(str(path))
        mapout.export_xmap_float(self.xmap)
        mapout.close_write()


class MCDNXMap:
    xmap: NXmap_float

    def __init__(self,
                 nxmap: NXmap_float
                 ) -> None:
        # xmap = Xmap_float(spacegroup,
        #                   cell,
        #                   grid,
        #                   )
        self.nxmap = nxmap

    def __getstate__(self):
        rtop = self.nxmap.operator_orth_grid()

        operator = (rtop.rot.as_numpy(), rtop.trn.as_numpy())

        grid = self.nxmap.grid()

        data = self.nxmap.export_numpy()
        state = {"operator": operator,
                 "grid": (grid.nu, grid.nv, grid.nw),
                 "data": data,
                 }

        return state

    def __setstate__(self, state):
        rtop = RTop_orth(Mat33_double(state["operator"][0]),
                         Vec3_double(state["operator"][1]),
                         )
        grid_params = state["grid"]
        grid = Grid_sampling(grid_params[0], grid_params[1], grid_params[2])
        self.nxmap = NXmap_float(grid,
                                 rtop,
                                 )

        self.nxmap.import_numpy(Coord_grid(0, 0, 0),
                                state["data"],
                                )

    def to_ccp4(self, path: Path, cell: Cell) -> None:
        mapout = CCP4MAPfile()
        # print(dir(mapout))
        mapout.open_write(str(path))
        mapout.set_cell(cell)
        mapout.export_xmap_float(self.nxmap)
        mapout.close_write()


def xmap_to_numpy_crystalographic_axis(xmap: MCDXMap) -> np.ndarray:
    # print("xmap is: {}".format(xmap))
    grid = xmap.xmap.grid_sampling
    grid_params = (grid.nu, grid.nv, grid.nw)

    # xmap_np = np.zeros(grid_params, dtype="double")
    xmap_np = xmap.xmap.export_numpy()

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

    xmap = Xmap_float(spacegroup,
                      cell,
                      grid,
                      )

    xmap.fft_from(hkl_data)

    return MCDXMap(xmap)


def output_nxmap(nxmap: NXmap_float, path: Path, cell: Cell) -> None:
    mapout = CCP4MAPfile()
    # print(dir(mapout))
    mapout.open_write(str(path))
    mapout.set_cell(cell)
    mapout.export_nxmap_float(nxmap)
    mapout.close_write()


def interpolate_uniform_grid(xmap,
                             translation_mobile_to_ref=(0, 0, 0),
                             rotation_mobile_to_ref=np.eye(3),
                             grid_params=[50, 50, 50],
                             ):
    # print("translation_mobile_to_ref: {}".format(translation_mobile_to_ref))

    rot = clipper_python.Mat33_double(rotation_mobile_to_ref)
    trans = clipper_python.Vec3_double(translation_mobile_to_ref[0],
                                       translation_mobile_to_ref[1],
                                       translation_mobile_to_ref[2],
                                       )

    rtop = clipper_python.RTop_orth(rot,
                                    trans,
                                    )

    # Generate the clipper grid
    grid = clipper_python.Grid(grid_params[0],
                               grid_params[1],
                               grid_params[2],
                               )

    # Define nxmap from the clipper grid and rotation-translation operator
    nxmap = clipper_python.NXmap_float(grid,
                                       rtop,
                                       )

    # Interpolate the Xmap onto the clipper nxmap
    clipper_python.interpolate(nxmap, xmap.xmap)

    return nxmap


def xmap_from_path(path,
                   structure_factors,
                   ) -> MCDXMap:
    mtz_file = clipper_python.CCP4MTZfile()

    mtz_file.open_read(str(path))

    hkl_info = clipper_python.HKL_info()
    mtz_file.import_hkl_info(hkl_info)

    # hkl_data = clipper_python.HKL_data_F_phi(hkl_info)
    hkl_data = clipper_python.data32.HKL_data_F_phi_float(hkl_info)
    # mtz_file.import_hkl_data(hkl_data,
    #                          "*/*/[{}]".format(structure_factors),
    #                          )

    mtz_file.import_hkl_data(hkl_data, "*/*/[2FOFCWT,PH2FOFCWT]")

    mtz_file.close_read()

    spacegroup = hkl_info.spacegroup
    cell = hkl_info.cell
    resolution = hkl_info.resolution

    hkl_data = hkl_data

    return MCDXMap.xmap_from_clipper_res(spacegroup, cell, resolution, hkl_data)

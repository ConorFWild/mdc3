from clipper_python import (Cell,
                            Resolution,
                            Spacegroup,
                            Spgr_descr,
                            Cell_descr,
                            )


class PyCell:
    cell: Cell

    def __init__(self, cell: Cell):
        self.cell = cell

    def __getstate__(self):
        cell = self.cell
        state = {"a": cell.a,
                 "b": cell.b,
                 "c": cell.c,
                 "alpha": cell.alpha,
                 "beta": cell.beta,
                 "gamme": cell.gamma,
                 }
        return state

    def __setstate__(self, state):
        a = state["a"]
        b = state["b"]
        c = state["c"]
        alpha = state["alpha"]
        beta = state["beta"]
        gamma = state["gamma"]
        self.cell = Cell(a,
                         b,
                         c,
                         alpha,
                         beta,
                         gamma,
                         )


class PyResolution:
    resolution: Resolution

    def __init__(self, resolution: Resolution):
        self.resolution = resolution

    def __getstate__(self):
        state = {"resolution": self.resolution.limit}
        return state

    def __setstate__(self, state):
        resolution = state["resolution"]
        self.resolution = Resolution(resolution)


class PySpacegroup:
    spacegroup: Spacegroup

    def __init__(self, spacegroup: Spacegroup):
        self.spacegroup = spacegroup

    def __getstate__(self):
        state = {"number": self.spacegroup.spacegroup_number}
        return state

    def __setstate__(self, state):
        spacegroup_number = state["number"]
        self.spacegroup = Spacegroup(Spgr_descr(spacegroup_number))


def spacegroup_to_state(spacegroup: Spacegroup):
    state = {"number": spacegroup.spacegroup_number}
    return state


def spacegroup_from_state(state):
    spacegroup_number = state["number"]
    # print("spgrp num: {}".format(spacegroup_number))
    return Spacegroup(Spgr_descr(str(spacegroup_number)))


def resolution_to_state(resolution: Resolution):
    state = {"resolution": resolution.limit}
    return state


def resolution_from_state(state):
    resolution = state["resolution"]
    return Resolution(resolution)


def cell_to_state(cell: Cell):
    state = {"angles": cell.angles,
             "dim": cell.dim,
             }
    return state


def cell_from_state(state):
    a = state["dim"][0]
    b = state["dim"][1]
    c = state["dim"][2]
    alpha = state["angles"][0]
    beta = state["angles"][1]
    gamma = state["angles"][2]
    return Cell(Cell_descr(a,
                           b,
                           c,
                           alpha,
                           beta,
                           gamma,
                           )
                )


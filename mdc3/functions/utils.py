from typing import Tuple
from pathlib import Path
import clipper_python


def res_from_mtz_file(path: Path) -> clipper_python.CCP4MTZfile:
    mtz_file = clipper_python.CCP4MTZfile()
    mtz_file.open_read(str(path))
    res = mtz_file.resolution
    mtz_file.close_read()
    return res
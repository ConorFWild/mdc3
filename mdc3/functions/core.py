from typing import Tuple
from pathlib import Path
import clipper_python


# def load_mtz_file_from_path(path: Path) -> clipper_python.CCP4MTZfile:
#     mtz_file = clipper_python.CCP4MTZfile()
#     mtz_file.open_read(str(path))
#     mtz_file.resolution
#
#
#
# def load_mtz_from_path(path: Path) -> Tuple[clipper_python.HKL_info, clipper_python.data32.HKL_data_F_phi_float]:
#     mtz_file = clipper_python.CCP4MTZfile()
#     mtz_file.mtz.open_read(str(path))
#
#     hkl_info = clipper_python.HKL_info()
#     mtz_file.mtz.import_hkl_info(hkl_info)
#
#     # hkl_data = clipper_python.HKL_data_F_phi(hkl_info)
#     hkl_data = clipper_python.data32.HKL_data_F_phi_float(hkl_info)
#     mtz_file.mtz.import_hkl_data(hkl_data, "*/*/[FWT,PHWT]")
#
#     mtz_file.mtz.close_read()
#
#     return ()
#
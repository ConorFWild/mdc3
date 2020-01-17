from pathlib import Path

import clipper_python


class File:
    path: Path

    def __init__(self,
                 path: Path,
                 ) -> None:
        self.path = path


class MTZFile(File):
    mtz: clipper_python.CCP4MTZfile

    def __init__(self,
                 path: Path,
                 ) -> None:
        super(MTZFile, self).__init__(path)
        self.mtz = clipper_python.CCP4MTZfile()


class CCP4MapFile(File):
    ccp4_map: clipper_python.CCP4MAPfile

    def __init__(self,
                 path: Path,
                 ) -> None:
        super(CCP4MapFile, self).__init__(path)
        self.mtz = clipper_python.CCP4MAPfile()


class PDBFile:
    path: Path

    def __init__(self,
                 path: Path,
                 ) -> None:
        self.path = path


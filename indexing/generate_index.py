# TODO: Remove "contents"
#       Add links within the doc (contents in a hierarchy?)
#       Consider auto-gen on release

from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from typing import List, NamedTuple
import warnings

import iris

TEST_DATA_ROOT = Path(__file__).parent / Path("../test_data")
TEMPLATE_FILE = Path(__file__).parent / Path("INDEX_template.md")
OUTPUT_FILE = Path(__file__).parent / Path("../INDEX.md")

class FileInfo(NamedTuple):
    path: Path
    cube_strs: List[str]
    warnings: List[str]
    exceptions: List[str]

def getFilepaths(path : Path) -> List[Path]:
    path_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            path_list.append(Path(root) / Path(file))
    return path_list

def getFileInfos(filepaths: List[Path]) -> List[FileInfo]:
    file_infos = defaultdict(list)

    for filepath in filepaths:
        
        if filepath.suffix in [".py", ".rst", ".txt", ".md"]:
            continue

        cube_strs = []
        warning_list = []
        exception_list = []

        with warnings.catch_warnings(record=True) as ww:
            try:
                cubelist = iris.load(str(filepath))
            except Exception as e:
                print(f"Error loading {filepath}")
                e_name = type(e).__name__
                print(e_name + ": " + str(e) + "\n")
                exception_list.append(e_name + ": " + str(e))
            else:
                for cube in cubelist:
                    cube_strs.append(str(cube))

            for warning in ww:
                w_name = warning._category_name
                warning_list.append(w_name + ": " + str(warning.message))
        
        TDR_sub_dir = filepath.parent.relative_to(TEST_DATA_ROOT).parts[0]

        file_infos[TDR_sub_dir].append(
            FileInfo(
                filepath.relative_to(TEST_DATA_ROOT),
                cube_strs,
                warning_list,
                exception_list,
            )
        )
    
    return file_infos

filepaths = getFilepaths(TEST_DATA_ROOT)

readme_content = getFileInfos(filepaths)

env = Environment(loader = FileSystemLoader("."))
template = env.get_template(str(TEMPLATE_FILE))

output = template.render(content=readme_content)

with open(OUTPUT_FILE, "w+") as ff:
    ff.write(output)
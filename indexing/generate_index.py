from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from typing import List, NamedTuple
import warnings

import iris

IGNORE_SUFFIXES = [".py", ".rst", ".txt", ".md"]

TEST_DATA_ROOT = Path(__file__).parent / Path("../test_data")
TEMPLATE_FILE = Path(__file__).parent / Path("INDEX_template.md")
OUTPUT_FILE = Path(__file__).parent / Path("../INDEX.md")


class FileInfo(NamedTuple):
    path: Path
    link_path: Path
    cube_strs: List[str]
    warnings: List[str]
    exceptions: List[str]


def getDataFilepaths(path: Path) -> List[Path]:
    path_list = []
    for fp in path.rglob("*"):
        if fp.is_file() and fp.suffix not in IGNORE_SUFFIXES:
            path_list.append(fp)
    return path_list


def getFileInfos(filepaths: List[Path]) -> List[FileInfo]:
    file_infos = defaultdict(list)

    for filepath in filepaths:

        cube_strs = []
        warning_list = []
        exception_list = []

        with warnings.catch_warnings(record=True) as ww:
            try:
                cubelist = iris.load(str(filepath))
            except Exception as e:
                print(f"Error loading {filepath}")
                exception_list.append(f"{type(e).__name__}: {e}")
                print(exception_list[-1] + "\n")
            else:
                for cube in cubelist:
                    cube_strs.append(str(cube))

            for warning in ww:
                warning_list.append(f"{warning._category_name}: {warning.message}")

        TDR_sub_dir = filepath.parent.relative_to(TEST_DATA_ROOT).parts[0]

        file_infos[TDR_sub_dir].append(
            FileInfo(
                filepath.relative_to(TEST_DATA_ROOT),
                filepath.relative_to(OUTPUT_FILE.parent),
                cube_strs,
                warning_list,
                exception_list,
            )
        )

    return file_infos


data_filepaths = getDataFilepaths(TEST_DATA_ROOT)

readme_content = getFileInfos(data_filepaths)

env = Environment(loader=FileSystemLoader(TEMPLATE_FILE.parent))
template = env.get_template(TEMPLATE_FILE.name)

output = template.render(content=readme_content)

with open(OUTPUT_FILE, "w+") as ff:
    ff.write(output)

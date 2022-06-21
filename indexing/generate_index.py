from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import List, NamedTuple
import warnings

from PIL import Image
import iris

IGNORE_SUFFIXES = [".cdl", ".gz", ".md", ".npz", ".py", ".rst", ".txt"]

TEST_DATA_ROOT = Path(__file__).parent / Path("../test_data")
TEMPLATE_FILE = Path(__file__).parent / Path("INDEX_template.md")
OUTPUT_FILE = Path(__file__).parent / Path("../INDEX.md")


class FileInfo(NamedTuple):
    path: Path
    link_path: Path
    items: List[str]
    is_png: bool
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

        items = []
        is_png = False
        warning_list = []
        exception_list = []

        with warnings.catch_warnings(record=True) as ww:
            print(f"{str(filepath)}")
            try:
                image = Image.open(str(filepath))
                if image.format == "PNG":
                    is_png = True
                    items = None
                image.close()
            except IOError:
                pass

            if not is_png:
                try:
                    cubelist = iris.load(str(filepath))
                except Exception as e:
                    print(f"Error loading {filepath!r}")
                    exception_list.append(f"{type(e).__name__}: {e}")
                    print(exception_list[-1] + "\n")
                else:
                    for cube in cubelist:
                        items.append(str(cube))

            for warning in ww:
                warning_list.append(f"{warning._category_name}: {warning.message}")

        TDR_sub_dir = filepath.parent.relative_to(TEST_DATA_ROOT).parts[0]

        file_infos[TDR_sub_dir].append(
            FileInfo(
                filepath.relative_to(TEST_DATA_ROOT),
                filepath.relative_to(OUTPUT_FILE.parent),
                items,
                is_png,
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

import shutil
import sys
from pathlib import Path


from normaliser import normalise

EXT_FOLDER = {
    ("mp3", "ogg", "waw", "amr"): "audio",
    ("avi", "mp4", "mov", "mkv", "flv"): "video",
    ("jpeg", "png", "jpg", "svg"): "images",
    ("doc", "docx", "txt", "xlsx", "xls", "pptx"): "documents",
    ("djvu", "djv", "pdf", "tiff"): "books",
    ("zip", "gz", "tar", "7z"): "archives",
}

""" ============================= Функці =================================="""


def get_file_cathegory(file: str):
    """Функція повертає назву категорії у відповідності до імені вхідного файлу."""

    the_path = Path(file)

    ext = the_path.suffix.lstrip(".")

    for exts in EXT_FOLDER.keys():
        if ext in exts:
            return EXT_FOLDER[exts]
    return None


def normalise_file_name(file: str):
    """Функція перейменовує файли з використанням функції normalise."""

    the_path = Path(file)

    normalised_name = normalise(the_path.stem)

    new_file_path = the_path.parent.joinpath(
        "".join([normalised_name, the_path.suffix])
    )

    the_path.rename(new_file_path)

    return new_file_path


def create_folders(root):
    """Створює папки каталогів у root"""

    for folder in EXT_FOLDER.values():

        Path(root).joinpath(folder).mkdir(exist_ok=True)


def sort_dir(
    path, level=0, known_exts=set(), unknown_exts=set(), categories=set()
):
    """Функція фасує файли по відповідним папкам."""

    the_path = Path(path)

    if level == 0:

        global root_path

        root_path = the_path.resolve()

    for item in the_path.iterdir():

        if item.is_dir() and item.name not in EXT_FOLDER.values():

            sort_dir(item.resolve(), level + 1)

        else:

            category = get_file_cathegory(item.name)

            if category:

                # --------------------------

                categories.add(category)

                known_exts.add(item.suffix)

                item = normalise_file_name(item)

                # --------------------------

                try:

                    shutil.move(item, Path(root_path).joinpath(category))

                    if category == "archives":

                        unpack(
                            Path(root_path).joinpath(category, item.name),
                            Path(root_path).joinpath(category, item.stem),
                        )

                except shutil.Error as er:

                    print(er)

            else:

                if item.is_file():
                    unknown_exts.add(item.suffix)

    return tuple(unknown_exts)


def unpack(archive_path, path_to_unpack):
    """Розраковувач файлів."""

    try:

        shutil.unpack_archive(archive_path, path_to_unpack)

    except OSError:

        print(f"Unsupported file format {archive_path}")


def remove_empty(path):
    """Видаляє порожні папки."""

    the_path = Path(path)

    empty = True

    for item in the_path.glob("*"):

        if item.is_file():

            empty = False

        if item.is_dir() and not remove_empty(item):

            empty = False

    if empty:

        path.rmdir()

    return empty


def known_exts(root):

    exts = set()

    for item in Path(root).iterdir():

        if item.is_dir():

            for file in item.iterdir():

                if file.is_file():

                    exts.add(file.suffix)

    return exts


""" ======================== Основна програма =============================="""


def main(root):
    agreement = input(
        f"WARNING! Are you sure you want to sort the files in CATALOG {root}? (y/n): "
    )

    if agreement in ("y", "Y", "yes", "Yes", "YES"):

        create_folders(root)

        unknown_exts = sort_dir(root)

        remove_empty(root)

        print("-------------------")
        print("Known extensions:")
        print("-------------------")

        for ext in known_exts(root):

            print(ext)

        if len(unknown_exts) != 0:

            print("-------------------")
            print("Unknown extensions:")
            print("-------------------")

            for ext in unknown_exts:

                print(ext)

        print("-------------------")
        print("Files in folders:")
        print("-------------------")

        for item in Path(root).iterdir():

            if item.is_dir():

                num_of_files = len(
                    [
                        file
                        for file in Path(root).joinpath(item).iterdir()
                        if file.is_file()
                    ]
                )

                print(f"Folder {item.name} contain {num_of_files} file(s)")

    else:

        print("Operation approved!")


def run():

    try:

        main(sys.argv[1])

    except IndexError:

        print(f"usage: {Path(__file__).name} indir")


if __name__ == "__main__":

    run()

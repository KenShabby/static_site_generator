import os
import shutil
import sys

from copy_static import copy_files_recursive
from generate_pages import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


main()

if __name__ == "__main__":
    main()

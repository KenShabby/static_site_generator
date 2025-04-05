import os
import pathlib
import shutil
import sys

from block_splitters import *
from markdown_to_html_node import *

STATIC_DIR = "static/"
CONTENT_DIR = "content/"
TEMPLATE_DIR = "."
DEST_DIR = "docs/"

if len(sys.argv) > 1:
    if sys.argv[1]:
        basepath = sys.argv[1]
else:
    basepath = ''

def copy_static_to_public():
    """It should first delete all the contents of the destination directory
    (public) to ensure that the copy is clean.
    It should copy all files and subdirectories, nested files, etc.
    I recommend logging the path of each file you copy, so you can see what's
    happening as you run and debug your code.
    """
    # Wipe existing public directory
    nuke_dir(DEST_DIR)

    # Copy over everything from static to public
    shutil.copytree(STATIC_DIR, DEST_DIR)
    print(f"Ran copytree({STATIC_DIR}, {DEST_DIR})")


def nuke_dir(path):

    if os.path.exists(path):
        print(f"Running rmtree({path})")
        shutil.rmtree(path)


def extract_title(markdown)-> str:

    title_tag = markdown[:2]
    idx_EOL = markdown.find('\n')
    if title_tag != "# ":
        raise Exception("That was not a properly formatted markdown title")
    title = markdown[1:idx_EOL]
    return title.strip()


def generate_page(from_path, template_path, dest_path):
    # Less than elegant way of shoehorning our output
    dest_path = dest_path.replace('.md', '.html')
    dest_path = dest_path.replace('content/', '')
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #Read the markdown file at from_path and store the contents in a variable.
    try:
        print(f"Attempting to open: {from_path}")
        with open(f"{from_path}", "r") as read_file:
            print(f"Succeeded.")
            # Use your markdown_to_html_node function and .to_html() method to convert
            # the markdown file to an HTML string.
            content = read_file.read()
            # Use the extract_title function to grab the title of the page.
            page_title = extract_title(content)
            parent_node = markdown_to_html_node(content)
            html = parent_node.to_html()
            # Read the template file at template_path and store the contents in a variable.
            with open(f"{template_path}", "r") as template_file:
                template = template_file.read()
            # Replace the {{ Title }} and {{ Content }} placeholders in the template
            # with the HTML and title you generated.
            template = template.replace("{{ Title }}", page_title)
            article = template.replace("{{ Content }}", html)
#            article = article.replace('href="/', f'href="{basepath}')
#            article = article.replace('src="/', f'src="{basepath}')
            # Write the new full HTML page to a file at dest_path. Be sure to create any
            # necessary directories if they don't exist.
            print(f"Trying to make dir: {os.path.dirname(dest_path)}")
            pathlib.Path(os.path.dirname(f'{dest_path}')).mkdir(parents=True, exist_ok=True)
            print(f"Trying to touch file: {dest_path}")
            pathlib.Path(f"{dest_path}").touch()
            print(f"Touched!")
            with open(f'{dest_path}', 'w') as write_file:
                write_file.write(article)
    except FileNotFoundError:
        print(f"File not found. {dest_path}")
    except PermissionError:
        print("Permission denied.")

def main():


    copy_static_to_public()
    for root, dirs, files in pathlib.Path(CONTENT_DIR).walk():
        for name in files:
            generate_page(f"{root}/{name}", f"template.html", f"{basepath}{DEST_DIR}{root}/{name}")
    return


if __name__ == "__main__":

    main()

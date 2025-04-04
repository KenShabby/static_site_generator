import os
import shutil

from block_splitters import *
from markdown_to_html_node import *

SOURCE_DIR = "static/"
CONTENT_DIR = "content/"
TEMPLATE_DIR = "."
DEST_DIR = "public/"


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
    shutil.copytree(SOURCE_DIR, DEST_DIR)
    print(f"Ran copytree({SOURCE_DIR}, {DEST_DIR})")


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
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    #Read the markdown file at from_path and store the contents in a variable.
    try:
        print(f"Attempting to open: {from_path}")
        with open(f"{from_path}index.md", "r") as read_file:
            print(f"Succeeded.")
            # Use your markdown_to_html_node function and .to_html() method to convert
            # the markdown file to an HTML string.
            content = read_file.read()
            # Use the extract_title function to grab the title of the page.
            page_title = extract_title(content)
            print(page_title)
            parent_node = markdown_to_html_node(content)
            html = parent_node.to_html()
            # Read the template file at template_path and store the contents in a variable.
            with open(f"template.html", "r") as template_file:
                template = template_file.read()
            # Replace the {{ Title }} and {{ Content }} placeholders in the template
            # with thfkjje HTML and title you generated.
            template = template.replace("{{ Title }}", page_title)
            article = template.replace("{{ Content }}", html)
            # Write the new full HTML page to a file at dest_path. Be sure to create any
            # necessary directories if they don't exist.
            with open(f'{dest_path}index.html', 'w') as write_file:
                write_file.write(article)
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")

def main():

    copy_static_to_public()
    generate_page(CONTENT_DIR, TEMPLATE_DIR, DEST_DIR)

    return


if __name__ == "__main__":

    main()

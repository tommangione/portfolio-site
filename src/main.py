import sys
import os
import shutil
from textnode import *
from htmlnode import *


def main():
    # print("hello world")
    # example = TextNode("example time", "link", "www.example.com")
    # print(example.__repr__())

    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    try:
        recursive_copy("static", "docs")
        print("Successfully copied static directory to public.")
    except Exception as e:
        print(f"Error: {e}")
        return

    try:
        generate_page_recursive('content', 'template.html', 'docs', basepath)
    except Exception as bad:
        print(f"Error: {bad}")

    return


def generate_page(from_path, template_path, dest_path, basepath):
    from_doc = ""

    print("Generating webpage...")

    print(f"from path = {from_path}")
    from_path = os.path.abspath(from_path)

    print(f"template path = {template_path}")
    template_path = os.path.abspath(template_path)

    print(f"destination path = {dest_path}")
    dest_path = os.path.abspath(dest_path)

    with open(from_path) as f:
        from_doc = f.read()

    from_html = markdown_to_html_node(from_doc).to_html()

    title = extract_title(from_doc)

    with open(template_path) as g:
        page = g.read()

    tit_placeholder = '{{ Title }}'
    con_placeholder = '{{ Content }}'

    page = page.replace(tit_placeholder, title)
    page = page.replace(con_placeholder, from_html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    try:
        with open(dest_path, 'w', encoding="utf-8") as h:
            h.write(page)
            print(f"Generated page at {dest_path}")
    except IOError as er:
        print(f"Error occurred while writing to {dest_path}: {er}")


def generate_page_recursive(dir_path_content,
                            template_path,
                            dest_dir_path,
                            basepath,
                            ):
    dir_path_content = os.path.abspath(dir_path_content)
    template_path = os.path.abspath(template_path)
    dest_dir_path = os.path.abspath(dest_dir_path)

    os.makedirs(dest_dir_path, exist_ok=True)

    directory = os.listdir(dir_path_content)

    for entry in directory:
        new_source_path = os.path.join(dir_path_content, entry)
        new_dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(new_source_path):
            generate_page_recursive(new_source_path,
                                    template_path,
                                    new_dest_path,
                                    basepath,
                                    )
        elif os.path.isfile(new_source_path) and entry[-3:] == ".md":
            dest_html_path = os.path.join(dest_dir_path, entry[:-3] + ".html")
            generate_page(new_source_path,
                          template_path,
                          dest_html_path,
                          basepath,
                          )
        else:
            pass


def extract_title(markdown):
    md_lines = markdown.splitlines()
    title = ""
    for line in md_lines:
        if line.startswith("# "):
            title = line[2:]
            break
    if title == "":
        raise Exception("No title found.")
    return title


def deleteCheck():
    choice = ""
    print("This action will delete the 'public' folder within this directory.")
    print("Would you like to proceed? Enter y to continue.")
    choice = input()
    if choice == "y":
        shutil.rmtree(os.path.abspath("public"))
    else:
        raise Exception("Directory 'public' not cleared.")


def recursive_copy(source, destination):
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)

    # Check if the source directory exists
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source directory {source} does not exist.")

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        deleteCheck()
        os.makedirs(destination)

    for item in os.listdir(source):
        src_item = os.path.join(source, item)
        dest_item = os.path.join(destination, item)

        if os.path.isfile(src_item):
            shutil.copy2(src_item, dest_item)
        elif os.path.isdir(src_item):
            recursive_copy(src_item, dest_item)
        else:
            print(f"Skipping {src_item} as it is not a file or directory.")


main()

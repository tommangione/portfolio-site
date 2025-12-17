# from textnode import TextNode
import os
import shutil


def main():
    # print("hello world")
    # example = TextNode("example time", "link", "www.example.com")
    # print(example.__repr__())

    try:
        recursive_copy("static", "public")
        print("Successfully copied static directory to public.")
    except Exception as e:
        print(f"Error: {e}")
        return
    generate_page()


def generate_page(from_path, template_path, dest_path):
    from = ""
    template = ""
    print("Generating webpage...")
    print(f"from path = {from_path}")
    print(f"template path = {template_path}")
    print(f"destination path = {dest_path}")

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

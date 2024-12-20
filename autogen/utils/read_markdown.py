def read_markdown_file(file_path):
    """
    Reads the content of a markdown file and returns it as a string.

    :param file_path: Path to the markdown file
    :return: Content of the markdown file as a string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

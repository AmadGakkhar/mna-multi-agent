def save_to_markdown(
    content: str,
) -> None:
    """
    Save the given content to a markdown file.

    Parameters:
    content (str): The content to be saved.
    filename (str): The name of the markdown file. Default is 'output.md'.
    """
    filename = "output.md"
    with open(filename, "w") as file:
        file.write("# Report\n\n")
        file.write(content)
    print(f"Content written to {filename}")

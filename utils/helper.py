import os
import fnmatch

def get_absolute_path(path):
    # Check if the path is absolute
    if os.path.isabs(path):
        print(f"The path is already an absolute path: {path}")
        return path
    else:
        # Convert to absolute path
        absolute_path = os.path.abspath(path)
        print(f"The path '{path}' is a relative path. The absolute path is: {absolute_path}")
        return absolute_path

def find_files(directory, pattern='*.mdx'):
    mdx_files = []
    # Traverse the directory tree
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            # Construct the absolute path and append it to the list
            mdx_files.append(os.path.abspath(os.path.join(root, filename)))
    if len(mdx_files) == 0:
        raise FileNotFoundError(f"No MDX files found in the directory: {directory}")
    if len(mdx_files) > 1:
        raise ValueError(f"Multiple MDX files found in the directory: {directory}")
    return mdx_files[0]
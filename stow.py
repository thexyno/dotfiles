import os
from typing import List

def create(source_path: str, target_path: str) -> List[str]:
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)
    if os.path.isdir(source_path):
        return create_dir(source_path, target_path)
    else:
        return create_file(source_path, target_path)

def create_file(source_path: str, target_path: str)-> List[str]:
    if os.path.exists(target_path) and not os.path.islink(target_path):
        raise os.error(f"File {target_path} exists")
    elif os.path.islink(target_path):
        link = os.path.abspath(os.readlink(target_path))
        abs_source = os.path.abspath(source_path)
        if link != abs_source:
            raise os.error(f"File {target_path} links to different source dir, {link} != {abs_source}")
        return [target_path]
    else:
        os.symlink(source_path, target_path)
        return [target_path]
def create_dir(source_path: str, target_path: str)-> List[str]:
    if not os.path.exists(target_path):
        os.symlink(source_path, target_path)
        return [target_path]
    else:
        if os.path.islink(target_path):
            link = os.path.abspath(os.readlink(target_path))
            abs_source = os.path.abspath(source_path)
            if link != abs_source:
                raise os.error(f"Dir {target_path} links to different source dir, {link} != {abs_source}")
            return [target_path]
        elif os.path.isdir(target_path):
            return merge_dirs(source_path, target_path)
        else:
            raise os.error(f"Dir exists: {source_path}")
def merge_dirs(source_path, target_path) -> List[str]:
    tr = []
    for item in os.listdir(source_path):
        tr += create(
            os.path.join(source_path, item),
            os.path.join(target_path, item)
        )
    return tr
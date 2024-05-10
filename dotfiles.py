import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from typing import List

import plugins
from stow import create


def create_symlink_tree(symlinkdir: str, files: List[tuple[str, str]]):
    # make sure every file only get's written once, duplicates will be merged
    files_final = {}
    for (filename, filecontent) in files:
        files_final[filename] = files_final.get(filename, "") + filecontent
    if os.path.exists(symlinkdir):
        shutil.rmtree(symlinkdir)
    os.mkdir(symlinkdir)
    for filename, filecontent in files_final.items():
        name = os.path.join(symlinkdir, filename)
        os.makedirs(os.path.dirname(name), exist_ok=True)
        with open(name, "w") as f:
            f.write(filecontent)


def generate_mise_file(mise_packages: List[str]) -> List[tuple[str, str]]:
    s = """
[settings]
experimental = true

[tools]
"cargo:cargo-binstall" = "latest"
"""
    for package in mise_packages:
        s += package
        s += "\n"
    return [(".config/mise/config.toml", s)]


def generate_brew_file(brew_packages: List[str]) -> List[tuple[str, str]]:
    return [(".brewfile", "\n".join(brew_packages))]


def install_mise_packages(update=False):
    if shutil.which('cargo') is None:
        os.system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    if shutil.which('mise') is None:
        print("installing mise")
        os.system("curl https://mise.run | sh")
    else:
        if update:
            print("updating mise")
            subprocess.run(["mise", "self-update"])
    print("updating mise tools")
    subprocess.run(["mise", "up"])


def install_brew_packages(update=False):
    if shutil.which('brew') is None:
        print("installing brew")
        os.system(
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    bf = subprocess.run(["brew", "file"], capture_output=True)
    if bf.returncode != 0:
        subprocess.run(["brew", "install", "rcmdnk/file/brew-file"])
    brewfile_path = os.path.abspath(
        os.path.join(os.getenv("HOME"), ".brewfile"))
    if update:
        print("updating brew packages")
        subprocess.run(["brew", "file", "-f", brewfile_path, "update"])
    else:
        print("installing brew packages")
        subprocess.run(["brew", "file", "-f", brewfile_path, "install"])


def cleanup(symlinkdir: str):
    file_list = []
    with open(os.path.join(symlinkdir, "files.json"), "r") as f:
        file_list = json.loads(f)
    for file in file_list:
        if os.path.exists(file) and os.path.islink(file):
            os.unlink(file)


def main():
    parser = argparse.ArgumentParser(
        prog="xyno-dotfiles",
        description="xyno's Dotfile installer")
    parser.add_argument('-s', '--symlinkdir', default=os.path.join(os.getenv("HOME"), ".xyno-dotfiles"),
                        help='dir that serves as symlink sources, default: $HOME/.xyno-dotfiles')
    parser.add_argument('-f', '--flag', action='append',
                        help='extra flags to give to plugins, default: [sys.platform, platform.machine()]', default=[sys.platform, platform.machine()])
    args = parser.parse_args()
    symlinkdir = os.path.abspath(args.symlinkdir)
    initialized_plugins = [p(args.flag, symlinkdir) for p in plugins.plugins]

    files = []
    mise_packages = []
    brew_packages = []
    aliases = []

    for p in initialized_plugins:
        files += p.files()
        mise_packages += p.mise_packages()
        brew_packages += p.brew_packages()
        aliases += p.aliases()
    files += generate_mise_file(mise_packages)
    files += generate_brew_file(brew_packages)

    print(files)
    print(mise_packages)
    print(brew_packages)
    print(aliases)
    create_symlink_tree(symlinkdir, files)

    files = create(symlinkdir, os.getenv("HOME"))
    with open(os.path.join(symlinkdir, "files.json"), "w") as f:
        f.write(json.dumps(files))
    install_mise_packages()
    install_brew_packages()
    for p in initialized_plugins:
        print(f"running scripts for {p.name}")
        p.script()


if __name__ == "__main__":
    main()

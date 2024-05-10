from abc import ABC
from typing import List


class Plugin(ABC):
    name = "changeme"
    def __init__(self, flags: List[str], symlinkdir: str):
        self.flags = flags
        self.symlinkdir = symlinkdir
    """
    returns list of (path relative to $HOME, content)
    """
    def files(self) -> List[tuple[str, str]]:
        return []
    def aliases(self) -> List[tuple[str, str]]:
        return []
    def mise_packages(self) -> List[str]:
        return []
    def brew_packages(self) -> List[str]:
        return []
    def script(self):
        # get's run after symlinks are created and mise/brew packages are installed
        pass
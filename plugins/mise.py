import os
import subprocess
from typing import List
from plugins.plugin import Plugin
from plugins.nushell import nu_config_path, nu_env_path


class Mise(Plugin):
    name = "Mise Package Manager"
    def files(self) -> List[tuple[str, str]]:
        return [
            (nu_config_path(self.flags), """
use ~/.cache/mise.nu
"""),
            (nu_env_path(self.flags), """
let mise_path =  "~/.cache/mise.nu"
^mise activate nu | save $mise_path --force
""")
        ]
    def script(self):
        with open(os.path.join(self.symlinkdir,"mise.nu"), "wb") as f:
            print("Writing activate script for nushell")
            process = subprocess.run(["mise", "activate", "nu"], capture_output=True)
            f.write(process.stdout)

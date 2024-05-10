
import os
from typing import List
from plugins.plugin import Plugin
from plugins.nushell import nu_config_path, nu_env_path


class Starship(Plugin):
    name = "Starship prompt"
    def files(self) -> List[tuple[str, str]]:
        with open(os.path.join(os.path.dirname(__file__),"starship.toml"), "r") as f:
            return [
            (nu_config_path(self.flags), """
use ~/.cache/starship/init.nu
"""),
            (nu_env_path(self.flags), """
mkdir ~/.cache/starship
starship init nu | save -f ~/.cache/starship/init.nu
"""),
            (".config/starship.toml", f.read() ),
        ]
    def brew_packages(self) -> List[str]:
        return ['brew starship']
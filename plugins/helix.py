from typing import List

from plugins.nushell import nu_env_path
from plugins.plugin import Plugin


class Helix(Plugin):
    name = "Helix Editor"
    def files(self) -> List[tuple[str, str]]:
        return [
            (".config/helix/config.toml", """
theme = "gruvbox"
"""),
            (nu_env_path(self.flags), """
$env.EDITOR = "hx"
$env.VISUAL = "hx"
"""),
        ]
    def brew_packages(self) -> List[str]:
        return ['brew helix']

from typing import List
from plugins.plugin import Plugin
from plugins.nushell import nu_env_path


class Brew(Plugin):
    name = "Brew"
    def files(self) -> List[tuple[str, str]]:
        mac_string = """# macOS ARM64 (Apple Silicon)
$env.PATH = ($env.PATH | split row (char esep) | prepend '/opt/homebrew/bin')
"""
        linux_string = """# Linux
$env.PATH = ($env.PATH | split row (char esep) | prepend '/home/linuxbrew/.linuxbrew/bin')
"""
        return [
            (nu_env_path(self.flags), f"""
{mac_string if "darwin" in self.flags else ""}
{linux_string if "linux" in self.flags else ""}
"""),
        ]
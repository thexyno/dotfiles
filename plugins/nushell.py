from typing import List

from plugins.plugin import Plugin

def nu_config_path(flags: List[str]):
    return "Library/Application Support/nushell/config.nu" if "darwin" in flags else ".config/nushell/config.nu"
def nu_env_path(flags: List[str]):
    return "Library/Application Support/nushell/env.nu" if "darwin" in flags else ".config/nushell/env.nu"

class NuShell(Plugin):
    name = "Nu Shell"
    def files(self) -> List[tuple[str, str]]:
        return [
            (nu_config_path(self.flags), """
$env.config = {
  edit_mode: vi,
  table: {
      mode: rounded
  }
}

alias no = open
alias open = ^open
alias l = ls -al
alias ll = ls -l
alias ga = git add
alias gaa = git add -A
alias gd = git diff
alias gc = git commit
alias gp = git push
alias gpl = git pull
"""),
            (nu_env_path(self.flags), """
$env.PATH = ($env.PATH | prepend $"($env.HOME)/.local/bin")
$env.PATH = ($env.PATH | prepend $"($env.HOME)/.cargo/bin")
"""),
        ]
    def mise_packages(self) -> List[str]:
        return ['"cargo:nu" = "latest"']
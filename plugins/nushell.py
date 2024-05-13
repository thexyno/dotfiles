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
let carapace_completer = {|spans|
    carapace $spans.0 nushell ...$spans | from json
}
let fish_completer = {|spans|
    fish --command $'complete "--do-complete=($spans | str join " ")"'
    | $"value(char tab)description(char newline)" + $in
    | from tsv --flexible --no-infer
}
let external_completer = {|spans|
    let expanded_alias = scope aliases
    | where name == $spans.0
    | get -i 0.expansion

    let spans = if $expanded_alias != null {
        $spans
        | skip 1
        | prepend ($expanded_alias | split row ' ' | take 1)
    } else {
        $spans
    }

    match $spans.0 {
        git => $fish_completer
        _ => $carapace_completer
    } | do $in $spans
}
$env.config = {
  edit_mode: vi
  table: {
      mode: rounded
  }
  completions: {
        quick: true
        partial: true
        external: {
            enable: true
            completer: $external_completer
        }
    }
}

source ~/.cache/carapace/init.nu


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
$env.CARAPACE_BRIDGES = 'zsh,fish,bash,inshellisense' # optional
mkdir ~/.cache/carapace
carapace _carapace nushell | save --force ~/.cache/carapace/init.nu
$env.PATH = ($env.PATH | prepend $"($env.HOME)/.local/bin")
$env.PATH = ($env.PATH | prepend $"($env.HOME)/.cargo/bin")
"""),
        ]
    def brew_packages(self) -> List[str]:
        return ['tap rsteube/homebrew-tap', 'brew rsteube/tap/carapace']
    def mise_packages(self) -> List[str]:
        return ['"cargo:nu" = "latest"']
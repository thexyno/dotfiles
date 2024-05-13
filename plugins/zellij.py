from typing import List
import os

from plugins.nushell import nu_env_path
from plugins.plugin import Plugin


class Zellij(Plugin):
    name = "Zellij Tmux Thing"
    def files(self) -> List[tuple[str, str]]:
        config_path = "Library/Application Support/org.Zellij-Contributors.Zellij/config.kdl" if 'darwin' in self.flags else ".config/zellij/config.kdl"
        shell_path = os.environ.get("HOME", "") + "/.local/share/mise/installs/cargo-nu/latest/bin/nu"
        
        return [
            (config_path, """
theme "gruvbox-dark"

default_shell """+'"'+shell_path+'"' +"""

themes {
	// example of how to set a theme in RGB format
 	gruvbox-light {
 		fg 60 56 54
        bg 251 82 75
        black 40 40 40
        red 205 75 69
        green 152 151 26
        yellow 215 153 33
        blue 69 133 136
        magenta 177 98 134
        cyan 104 157 106
        white 213 196 161
        orange 214 93 14
 	}

 	// example of how to set a theme in HEX format
 	gruvbox-dark {
 		fg "#D5C4A1"
 		bg "#282828"
 		black "#3C3836"
 		red "#CC241D"
 		green "#98971A"
 		yellow "#D79921"
 		blue "#3C8588"
 		magenta "#B16286"
 		cyan "#689D6A"
 		white "#FBF1C7"
 		orange "#D65D0E"
 	}
}
""")
        ]
    def mise_packages(self) -> List[str]:
        return ['"cargo:zellij" = "latest"']

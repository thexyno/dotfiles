from typing import List
from plugins.plugin import Plugin


class Wezterm(Plugin):
    name = "Wezterm Terminal"
    def files(self) -> List[tuple[str, str]]:
        return [(".config/wezterm/wezterm.lua", """
local wezterm = require 'wezterm'

-- This will hold the configuration.
local config = wezterm.config_builder()
-- Spawn a fish shell in login mode

config.default_prog = { '/Users/xyno/.local/share/mise/installs/cargo-nu/latest/bin/nu', '-l' }

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme = 'Gruvbox Dark (Gogh)'

-- and finally, return the configuration to wezterm
return config
""")]
    def brew_packages(self) -> List[str]:
        return ['cask wezterm']

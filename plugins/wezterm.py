from typing import List
from plugins.plugin import Plugin


class Wezterm(Plugin):
    name = "Wezterm Terminal"
    def files(self) -> List[tuple[str, str]]:
        return [(".config/wezterm/wezterm.lua", """
local wezterm = require 'wezterm'

-- This will hold the configuration.
local config = wezterm.config_builder()

local zellij_path = os.getenv("HOME") .. "/.local/share/mise/installs/cargo-zellij/latest/bin/zellij"

config.default_prog = { zellij_path, 'attach', '-c' }
config.hide_tab_bar_if_only_one_tab = true
config.max_fps = 120

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme = 'Gruvbox Dark (Gogh)'

-- and finally, return the configuration to wezterm
return config
""")]
    def brew_packages(self) -> List[str]:
        return ['cask wezterm']

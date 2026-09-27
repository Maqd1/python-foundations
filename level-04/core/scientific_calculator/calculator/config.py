"""Calculator configuration: precision, angle mode, history size, theme."""
import json

DEFAULT_CONFIG = {
    "precision": 4,
    "angle_mode": "DEG",  # or "RAD"
    "history_size": 100,
    "theme": "default",
}


class CalculatorConfig:
    def __init__(self):
        self.settings = DEFAULT_CONFIG.copy()

    def set_precision(self, places):
        self.settings["precision"] = places

    def set_angle_mode(self, mode):
        mode = mode.upper()
        if mode not in ("DEG", "RAD"):
            raise ValueError("Angle mode must be 'DEG' or 'RAD'.")
        self.settings["angle_mode"] = mode

    def set_history_size(self, size):
        self.settings["history_size"] = size

    def set_theme(self, theme):
        self.settings["theme"] = theme

    def save(self, filename="config.json"):
        with open(filename, "w") as f:
            json.dump(self.settings, f, indent=2)

    def load(self, filename="config.json"):
        with open(filename, "r") as f:
            self.settings = json.load(f)

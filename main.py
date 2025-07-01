import yaml
import logging

log = logging.getLogger(__name__)

from src.place_holder import main as gui

def main() -> None:
    with open("config.yaml") as f:
        cfg = yaml.safe_load(f)
    
    gui(cfg)

if __name__ == "__main__":
    main()
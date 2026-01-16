# Import necessary modules
import os  # For interacting with the operating system (e.g., file paths)
from configobj import ConfigObj  # For reading structured configuration files

# Determine the absolute path of the current script's directory
BASE = os.path.dirname(os.path.abspath(__file__))

# Load the configuration file 'config.cfg' located in the same directory
CONFIG = ConfigObj(os.path.join(BASE, 'config.cfg'))

# Extract specific configuration sections for easy access
API_CONFIG = CONFIG['api']
VSIM_CONFIG = CONFIG['vsim']
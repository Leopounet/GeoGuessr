import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from enum import Enum

class LoginMethod(Enum):
    """
    List of implemented login methods so far.
    """

    CLASSIC = "classic"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    UNKNOWN = "unknown"
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class Flag:

    """
    This class is used to list all the possible flags in a command (non
    positional arguments).
    """

    def __init__(self):
        
        """
        Creates a new list of flags.
        """
        
        # list of possible flags linked to the number of expected arguments
        # for example if the flag is "-n" and the expected number is 2
        # then: !!command <stuff> ... -n [arg1] [arg2]
        self.flags = {}

    def add_flag(self, flag, nb_args):
        """
        Adds the given flag to the list of flags and sets its number of expected arguments.
        This command fails if the flag is already in the list.

        :param flag: The flag to add.

        :param nb_args: The number of expected arguments for this flag.

        :return: True if the flag was successfully added, false otherwise.
        """
        if not self.exist_flag(flag):
            self.flags[flag] = nb_args
            return True
        return False

    def exist_flag(self, flag):
        """
        Checks if a given flag is already in the list.

        :param flag: The flag to check the existence of.

        :return: True if the flag is in the list, False otherwise.
        """
        if flag in self.flags:
            return True
        return False

    def get_number_of_args(self, flag):
        """
        Returns the expected number of arguments bound to this flag.

        :param flag: The flag to get the number of arguments of.

        :return: The number of arguments expected for this flag if is in the list, -1 otherwise.
        """
        if self.exist_flag(flag):
            return self.flags[flag]
        return -1
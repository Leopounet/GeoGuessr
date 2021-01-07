import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class ArgumentList:

    """
    This class lists all of the arguments read from a command.
    There are three types of arguments:
    - Positional -> these are mandatory arguments for the command
    - Non positional -> these are given via the use of flags
    - Junk -> these are invalid arguments

    Example:
    Let's have a command 'command' that needs 1 positional argument and
    can have two non positional arguments set by the flags -a and -b.

    `!!command hello`

    This above is a valid use and will yield [hello] [] [] (resp. pos, non pos and junk).

    `!!command hello -a hi -b what`

    Still valid, will yield [hello] [(-a, hi), (-b, what)] [].

    `!!command -a hello hi`

    Still valid, will yield [hi] [(-a, hello)] []

    `!!command hello hi`

    Invalid, but still will yield something usebale [hello] [] [hi].
    """

    def __init__(self):
        """
        Creates a new list of arguments (empty).
        """
        
        # the list of positional arguments
        self.pos = []

        # the list of non positional arguments
        # actually a dictionnary for fast access
        # this is a string to list dict
        # for example if the flag is -n and requires 2 args
        # !!command -n hello hi
        # then self.non_pos = {"-n":["hello", "hi"]}
        self.non_pos = {}

        # the list of junk arguments
        self.junk = []

    def is_flag_set(self, flag):
        """
        Checks if the given flag is already set.

        :param flag: The flag to check the existence of.

        :return: True if the flag is already set, False otherwise.
        """
        if flag in self.non_pos:
            return True
        return False

    def get_nb_pos(self):
        """
        Returns the number of positional arguments.

        :return: The current number of positional arguments.
        """
        return len(self.pos)

    def add_pos(self, arg):
        """
        Adds a new positional argument to the list of arguments.

        :param arg: The argument to add to the list.
        """
        self.pos.append(arg)

    def add_non_pos(self, flag, arg):
        """
        Adds a new non positional argument and binds it to its corresponding flag. It
        does not add the argument if the flag is already set.

        :param flag: The flag of this argument.

        :param arg: The argument to add.

        :return: True if the flag was not already set, False otherwise.
        """
        if not self.is_flag_set(flag):
            self.non_pos[flag] = arg
            return True
        return False

    def add_junk(self, arg):
        """
        Adds a new junk argument to the list of junk.

        :param arg: The argument to add.
        """
        self.junk.append(arg)

    def get_pos(self, index):
        """
        Return the positional argument at the given index.

        :param index: The index of the positional argument to return.

        :return: The value of the positional argument at the given index, None if the index \
        is invalid.
        """
        if 0 <= index < len(self.pos):
            return self.pos[index]
        return None

    def get_non_pos(self, flag):
        """
        Returns the list of arguments bound to the given flag.

        :param flag: The flag to consider.

        :return: A list of argument if the flag is valid, None otherwise.
        """
        if self.is_flag_set(flag):
            return self.non_pos[flag]
        return None

    def get_junk(self, index):
        """
        Return the junk argument at the given index.

        :param index: The index of the junk argument to return.

        :return: The value of the junk argument at the given index, None if the index \
        is invalid.
        """
        if 0 <= index < len(self.junk):
            return self.junk[index]
        return None

class ArgumentReader:

    """
    This class is used to read the arguments of a command. It parses all the different
    arguments and stores them depending on their position or the flag they are bound to.
    """

    @classmethod
    def read(self, arguments, flags, expected_pos):

        """
        Returns a new ArgumentList object created from the given arguments and flags.

        :param arguments: The list of arguments to read.

        :param flags: The list of valid flags.

        :param expected pos: The expected number of positional arguments. Once that number \
        of positional arguments is read, the following positional arguments will be set as junk.

        :return: A new ArgumentList object.
        """

        # current index in the command (used to shift)
        index = 0

        # the result created by this method
        res = ArgumentList()

        # the number of given arguments
        nb_args = len(arguments)

        # while there arguments to read
        while index < nb_args:
            
            # get the current argument
            arg = arguments[index]

            # if this is a valid flag
            if flags.exist_flag(arg):

                # get the number of expected arguments for this flag
                expected_nb_args = flags.get_number_of_args(arg)
                index += 1

                # if there are not enough remaining arguments, skip
                if index + expected_nb_args - 1 >= nb_args:
                    continue

                # get all the arguments
                flags_args = []
                
                # read "expected_nb_args" of arguments
                while expected_nb_args > 0:
                    flags_args.append(arguments[index])
                    expected_nb_args -= 1
                    index += 1

                # add it to the Argument List
                res.add_non_pos(arg, flags_args.copy())

            # if this was not a valid flag, then it must be a positional argument
            elif expected_pos > 0:
                res.add_pos(arg)
                expected_pos -= 1
                index += 1

            # if all the positional arguments are supposedly read, then it is junk
            else:
                res.add_junk(arg)
                index +=1

        return res
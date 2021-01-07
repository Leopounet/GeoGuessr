import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class Queue:

    """
    Simple queue class.
    """

    def __init__(self, size):

        """
        Creates a new queue object with a maximum size. Once the maximum size
        is reached, adding a new object will remove the oldest object added.

        :param size: The maximum size of this Queue.
        """

        # The list
        self.queue = []

        # The max size
        self.size = size

        # Current nb of elements
        self.current = 0

    def add(self, value):
        """
        Adds a new element to the Queue.

        :param value: The element to add.
        """

        # If the maximum size has not been reached yet
        if self.current < self.size:
            self.queue.append(value)
            self.current += 1

        # if the maximum size has been reached, remove the oldest object
        else:
            self.queue = self.queue[1:]
            self.queue.append(value)

    def get(self, index):
        """
        Returns the element at the given index.

        :param index: The index of the element to get.

        :return: The corresponding value, None if the index is invalid.
        """
        if 0 <= index < self.current:
            return self.queue[index]
        return None

from abc import ABC, abstractmethod


class Problem(ABC):
    """
    This abstract base class defines the interface for a problem that will be used in the algorithms.
    Subclasses should implement the methods to define the specific problem domain,
    such as the Traveling Salesman Problem.
    """

    @abstractmethod
    def get_random_future_state(self):
        """
        Generate a random state from the space of possible states. This state does not need to be a neighbor of the
        current state.

        Returns:
            The randomly generated future state.
        """
        pass

    @abstractmethod
    def validate_state(self, state):
        """
        Check if a given state is valid within the problem domain.

        Parameters:
            state: The state to validate.

        Returns:
            A boolean indicating whether the state is valid (True) or invalid (False).
        """
        pass

    @abstractmethod
    def is_solution(self, state):
        """
        Check if a given state is a valid solution

        Parameters:
            state: The state to validate.

        Returns:
            A boolean indicating whether the state is solution (True) or invalid (False).
        """
        pass

    @abstractmethod
    def get_cost(self, state):
        """
        Calculate and return the cost associated with a given state.

        Parameters:
            state: The state for which the cost is to be calculated.

        Returns:
            The cost associated with the state.
        """
        pass

    @abstractmethod
    def heuristic(self, state):
        """
        Compute and return a heuristic estimate of the cost to reach the goal from the given state.
        This method is used for heuristic-based search algorithms.

        Parameters:
            state: The state from which to estimate the cost to the goal.

        Returns:
            The heuristic estimated cost to the goal.
        """
        pass

    @abstractmethod
    def get_initial_state(self):
        """
        Get the initial state for the problem.

        Returns:
            The initial state of the problem.
        """
        pass

    @abstractmethod
    def get_current_state(self):
        """
        Retrieve the current state of the problem.

        Returns:
            The current state of the problem.
        """
        pass

    @abstractmethod
    def update_current_state(self, state):
        """
        Update the problem's current state to the given state.

        Parameters:
            state: The new state to which the current state will be updated.
        """
        pass

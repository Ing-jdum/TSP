from abc import ABC, abstractmethod


class Problem(ABC):

    @abstractmethod
    def get_random_future_state(self):
        pass

    @abstractmethod
    def validate_state(self, state):
        pass

    @abstractmethod
    def get_cost(self, state):
        pass

    @abstractmethod
    def heuristic(self, state):
        pass

    @abstractmethod
    def get_initial_state(self):
        pass

    @abstractmethod
    def get_current_state(self):
        pass

    @abstractmethod
    def update_current_state(self, state):
        pass



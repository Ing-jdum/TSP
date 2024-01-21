from TSP import TSP


class TSPWithEV(TSP):
    def __init__(self, graph_data, battery_capacity=100):
        super().__init__(graph_data)
        self.battery_capacity = battery_capacity
        self.current_battery_level = battery_capacity

    def is_charging_station(self, node):
        return node.startswith("ChargingStation")

    def validate_state(self, sequence):
        battery_level = self.battery_capacity
        for i in range(len(sequence) - 1):
            start, end = sequence[i], sequence[i + 1]

            # Use parent class's method to check if route exists
            if not super().validate_state([start, end]):
                return False

            # Battery level check
            distance = self.distance_dict.get((start, end), self.distance_dict.get((end, start)))
            battery_level -= distance
            if battery_level < 0:
                return False

            if self.is_charging_station(start) or self.is_charging_station(end):
                battery_level = self.battery_capacity

        return True

    def get_cost(self, state):
        total_distance = 0
        battery_level = self.battery_capacity
        for i in range(len(state)):
            start = state[i]
            end = state[(i + 1) % len(state)]

            # Check if the connection exists using parent class's method
            if (start, end) in self.distance_dict:
                distance = self.distance_dict[(start, end)]
                battery_level -= distance
                if battery_level < 0:
                    return float('inf')
                total_distance += distance*5
            else:
                return super().get_cost(state)

            if self.is_charging_station(start) or self.is_charging_station(end):
                battery_level = self.battery_capacity

        return total_distance

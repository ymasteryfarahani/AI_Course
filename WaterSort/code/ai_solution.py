class GameSolution:
    def __init__(self, game):
        self.ws_game = game
        self.moves = []
        self.tube_numbers = game.NEmptyTubes + game.NColor
        self.solution_found = False
        self.visited_tubes = set()

    def solve(self, current_state):
        from collections import deque
        
        def is_solved(state):
            # Check if the game is solved
            return all(len(set(tube)) <= 1 for tube in state if tube)
        
        def get_next_states(state):
            # Generate all possible next states from the current state
            next_states = []
            for i in range(self.tube_numbers):
                for j in range(self.tube_numbers):
                    if i != j and state[i] and (not state[j] or state[i][-1] == state[j][-1]):
                        if len(state[j]) < self.ws_game.tube_capacity:
                            new_state = [tube[:] for tube in state]
                            new_state[j].append(new_state[i].pop())
                            next_states.append((new_state, (i, j)))
            return next_states

        queue = deque([(current_state, [])])
        self.visited_tubes.add(tuple(tuple(tube) for tube in current_state))
        
        while queue:
            state, path = queue.popleft()
            
            if is_solved(state):
                self.solution_found = True
                self.moves = path
                return
            
            for next_state, move in get_next_states(state):
                state_tuple = tuple(tuple(tube) for tube in next_state)
                if state_tuple not in self.visited_tubes:
                    self.visited_tubes.add(state_tuple)
                    queue.append((next_state, path + [move]))

    def optimal_solve(self, current_state):
        import heapq

        def is_solved(state):
            return all(len(set(tube)) <= 1 for tube in state if tube)
        
        def get_next_states(state):
            next_states = []
            for i in range(self.tube_numbers):
                for j in range(self.tube_numbers):
                    if i != j and state[i] and (not state[j] or state[i][-1] == state[j][-1]):
                        if len(state[j]) < self.ws_game.tube_capacity:
                            new_state = [tube[:] for tube in state]
                            new_state[j].append(new_state[i].pop())
                            next_states.append((new_state, (i, j)))
            return next_states

        def heuristic(state):
            return sum(len(set(tube)) - 1 for tube in state if tube)  # heuristic function

        pq = [(heuristic(current_state), 0, current_state, [])]
        self.visited_tubes.add(tuple(tuple(tube) for tube in current_state))

        while pq:
            _, cost, state, path = heapq.heappop(pq)
            
            if is_solved(state):
                self.solution_found = True
                self.moves = path
                return
            
            for next_state, move in get_next_states(state):
                state_tuple = tuple(tuple(tube) for tube in next_state)
                if state_tuple not in self.visited_tubes:
                    self.visited_tubes.add(state_tuple)
                    heapq.heappush(pq, (cost + 1 + heuristic(next_state), cost + 1, next_state, path + [move]))

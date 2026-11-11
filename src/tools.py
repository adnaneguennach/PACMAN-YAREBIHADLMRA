from collections import deque
from src.maze import Maze


class Tools:
    @staticmethod
    def next_step_bfs(start, goal, maze: Maze):
        if start == goal:
            return None

        queue = deque([start])
        d = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            neighbors = maze.reachable_neighbors(*current)
            for neighbor in neighbors:
                if neighbor not in d:
                    d[neighbor] = current
                    queue.append(neighbor)

        if goal not in d:
            return None

        next_step = goal

        while d[next_step] != start:
            next_step = d[next_step]
        return next_step

    @staticmethod
    def shortest_path(start, goal, maze: Maze):
        if start == goal:
            return None

        queue = deque([start])
        d = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            neighbors = maze.reachable_neighbors(*current)
            for neighbor in neighbors:
                if neighbor not in d:
                    d[neighbor] = current
                    queue.append(neighbor)

        if goal not in d:
            return None

        path = [goal]

        while d[path[-1]] != start:
            path.append(d[path[-1]])

        return path

from collections import deque
from src.maze import Maze
from src.player import Player


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

    @staticmethod
    def _touching_player(ghost, player: Player):
            dx = ghost.px - player.px
            dy = ghost.py - player.py
            dist = (dx**2 + dy**2) ** 0.5
            return dist <= ghost.maze.cell_size // 2

    @staticmethod
    def _player_in_zone(ghost, player: Player):
        if (player.x, player.y) in ghost.range:
            ghost.player_detectet_in_zone = True
        else:
            ghost.player_detectet_in_zone = False

    @staticmethod
    def _update_range(ghost):
        ghost.range = []
        for i in range(
            ghost.y - (ghost.maze.height // 4),
            ghost.y + (ghost.maze.height // 4),
        ):
            for j in range(
                ghost.x - (ghost.maze.width // 4),
                ghost.x + (ghost.maze.width // 4),
            ):
                if i < 0 or j < 0:
                    continue
                ghost.range.append((j, i))

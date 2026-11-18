"""Event management: maps pygame event types to handler callbacks."""

import pygame

# Custom game events
PLAYER_DIED = pygame.USEREVENT + 1
LEVEL_CLEARED = pygame.USEREVENT + 2


class EventManager:
    def __init__(self):
        self._handlers = {}

    def on(self, event_type, handler):
        self._handlers.setdefault(event_type, []).append(handler)

    def process(self):
        """Pull every pending event and dispatch it to its handlers."""
        for event in pygame.event.get():
            for handler in self._handlers.get(event.type, []):
                handler(event)

    @staticmethod
    def post(event_type, **attrs):
        pygame.event.post(pygame.event.Event(event_type, **attrs))

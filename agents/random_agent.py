from agents.base_agent import BaseAgent
from random import choice


class RandAgent(BaseAgent):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):
        if not board.is_game_over():
            return choice([move for move in board.legal_moves])
        else:
            return None

import chess
from datetime import datetime
from tqdm import tqdm
from os import getcwd
from utils.trans_table_utils import *
from utils.history_utils import *

from utils.heuristics import combined

from agents.alpha_beta_agent import AlphaBetaAgent
from agents.alpha_beta_agent_trans import AlphaBetaAgentTrans
from agents.combined_agent import CombinedAgent
from agents.history_agent import OrderedAgent
from agents.minimax_agent import MiniMaxAgent
from agents.pv_agent import PVAgent
from agents.random_agent import RandAgent
from agents.random_agent_trans import RandAgentTrans
from agents.history_agent_trans import OrderedAgentTrans


class ChessGame:
    def __init__(self, white_agent_name, white_agent, black_agent_name, black_agent):
        self.white_agent_name = white_agent_name
        self.black_agent_name = black_agent_name
        self.white_agent = white_agent
        self.black_agent = black_agent
        self.white_agent_depth = white_agent.maximum_depth if hasattr(white_agent, 'maximum_depth') else 0
        self.black_agent_depth = black_agent.maximum_depth if hasattr(black_agent, 'maximum_depth') else 0
        self.white_agent_num_moves = 0
        self.black_agent_num_moves = 0
        self.white_agent_decision_time = 0
        self.black_agent_decision_time = 0
        self.white_agent_result = 0
        self.black_agent_result = 0
        self.board = chess.Board()

    def play_game(self, display=False):

        while not self.board.is_game_over() or self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition():
            self.play_round(display=display)
        result = self.board.result()
        if result == '0-1':
            self.white_agent_result = -1
            self.black_agent_result = 1
        elif result == '1-0':
            self.white_agent_result = 1
            self.black_agent_result = -1

        return {
            'white_agent_name': self.white_agent_name,
            'black_agent_name': self.black_agent_name,
            'white_agent_depth': str(self.white_agent_depth),
            'black_agent_depth': str(self.black_agent_depth),
            'white_agent_num_moves': str(self.white_agent_num_moves),
            'black_agent_num_moves': str(self.black_agent_num_moves),
            'white_agent_decision_time': str(self.white_agent_decision_time),
            'black_agent_decision_time': str(self.black_agent_decision_time),
            'white_agent_result': str(self.white_agent_result),
            'black_agent_result': str(self.black_agent_result)
        }

    def play_round(self, display=False):
        start = datetime.utcnow()
        self.play_move(self.white_agent)
        self.white_agent_decision_time += (datetime.utcnow() - start).total_seconds()
        self.white_agent_num_moves += 1
        if display:
            print(self.board.unicode(borders=True))

        start = datetime.utcnow()
        self.play_move(self.black_agent)
        self.black_agent_decision_time += (datetime.utcnow() - start).total_seconds()
        self.black_agent_num_moves += 1
        if display:
            print(self.board.unicode(borders=True))

    def play_move(self, agent):
        chosen_move = agent.get_move(self.board.copy())
        if chosen_move is not None:
            self.board.push_uci(chosen_move.uci())


def generate_data(white_agent_name, black_agent_name, white_agent, black_agent, path, num_runs=100, display=False):
    with open(path, 'w') as f:
        f.write('game_number\tagent_type\tagent_color\tagent_depth\tagent_num_moves\tagent_decision_time\tgame_result\n')

        for g_n in tqdm(range(num_runs)):
            g = ChessGame(white_agent_name, black_agent_name, white_agent, black_agent).play_game(display=display)
            f.write(str(g_n) + '\t' + g['white_agent_name'] + '\t' + 'white' + '\t' + g['white_agent_depth'] + '\t' + g['white_agent_num_moves'] + '\t' + g['white_agent_decision_time'] + '\t' + g['white_agent_result'] + '\n')
            f.write(str(g_n) + '\t' + g['black_agent_name'] + '\t' + 'black' + '\t' + g['black_agent_depth'] + '\t' + g['black_agent_num_moves'] + '\t' + g['black_agent_decision_time'] + '\t' + g['black_agent_result'] + '\n')

            # TODO: This is stupid hard-coded. Remove this you dummies. Love you
            write_trans_table(black_agent.trans_table, getcwd() + '/data/history_agent/trans_table.pickle')
            write_history_table(black_agent)


def main():
    # Base
    # generate_data('random', RandAgent(chess.WHITE), 'random', RandAgent(chess.BLACK), getcwd()[:-5] + 'data/RvR.csv')
    # generate_data('random', RandAgent(chess.WHITE), 'alphabeta2', AlphaBetaAgent(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/RvA2.csv')
    # generate_data('minimax2', MiniMaxAgent(chess.WHITE, combined, 2), 'alphabeta2', AlphaBetaAgent(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/M2vA2.csv')
    # generate_data('alphabeta2', AlphaBetaAgent(chess.WHITE, combined, 2), 'alphabeta2', AlphaBetaAgent(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/A2vA2.csv')

    # Transposition Tables
    # generate_data('alphabeta2', AlphaBetaAgent(chess.WHITE, combined, 2), 'alphabeta2_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/A2vA2T_1.csv', 300)

    # History tables
    # generate_data('history2', OrderedAgent(chess.WHITE, combined, 2), 'history2', OrderedAgent(chess.BLACK, combined, 2, True), getcwd()[:-5] + 'data/H2vH2.csv')
    # generate_data('pv2', PVAgent(chess.WHITE, combined, 2), 'pv2', PVAgent(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/P2vP2.csv')
    # generate_data('combined2', CombinedAgent(chess.WHITE, combined, 2), 'combined2', CombinedAgent(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/C2vC2.csv')

    # Depth
    # generate_data('alphabeta1', AlphaBetaAgent(chess.WHITE, combined, 1), 'alphabeta2', AlphaBetaAgent(chess.BLACK, combined, 2), getcwd()[:-5] + 'data/A1vA2.csv')
    # generate_data('alphabeta1', AlphaBetaAgent(chess.WHITE, combined, 1), 'alphabeta3', AlphaBetaAgent(chess.BLACK, combined, 3), getcwd()[:-5] + 'data/A1vA3.csv')
    # generate_data('alphabeta2', AlphaBetaAgent(chess.WHITE, combined, 2), 'alphabeta3', AlphaBetaAgent(chess.BLACK, combined, 3), getcwd()[:-5] + 'data/A2vA3.csv')


    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_1', 300)
    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_2', 300)
    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_3', 300)
    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_4', 300)
    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_5', 300)
    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_6', 300)
    # generate_data('random', RandAgent(chess.WHITE), 'random_trans', RandAgentTrans(chess.BLACK), getcwd()[:-5] + 'data/RvRT_7', 300)
    #
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_1', 300)
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_2', 300)
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_3', 300)
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_4', 300)
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_5', 300)
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_6', 300)
    # generate_data('greedy', AlphaBetaAgent(chess.WHITE, combined, 1), 'greedy_trans', AlphaBetaAgentTrans(chess.BLACK, combined, 1), getcwd()[:-5] + 'data/AvAT_7', 300)

    agent1, agent2 = [OrderedAgent(chess.WHITE, combined, 2), OrderedAgentTrans(chess.BLACK, combined, 3)]
    generate_data('ordered_history2', agent1, 'ordered_history2_trans', agent2, getcwd()[:-5] + 'data/H2vHT2.csv', 1, display=True)
    write_trans_table(agent2.trans_table, getcwd()[:-5] + 'data/history_agent/trans_table.pickle')
    write_history_table(agent2)


if __name__ == '__main__':
    main()

from typing import List, Optional, Type

from board import Board
from player import Player


class Game:
    def __init__(
        self,
        player_classes: List[Type[Player]],
        init_pieces_per_grid: int = 3,
        grids_per_player: int = 3,
        grids_between_players: int = 1,
        max_turns: int = 100,
    ):
        if not len(player_classes) > 1:
            raise ValueError("Players should be more than 2.")
        players = [player_class(player_id=i) for i, player_class in enumerate(player_classes)]
        players_num = len(players)
        self.players_num = players_num
        self.init_pieces_per_grid = init_pieces_per_grid
        self.grids_per_player = grids_per_player
        self.grids_between_players = grids_between_players
        self.max_turns = max_turns
        self.board = Board(
            players_num=players_num,
            init_pieces_per_grid=init_pieces_per_grid,
            grids_per_player=grids_per_player,
            grids_between_players=grids_between_players,
        )
        self.players = players

    def run(self) -> Optional[int]:
        turn_n = 1
        while True:
            print(f"Turn {turn_n}")
            for player in self.players:
                print(self.board)
                print(f"Player {player.player_id}")
                while True:
                    index = player.act(self.board)
                    print(f"Action {index}")
                    act_again = self.board.move(index=index)
                    if not act_again:
                        break

                if self.board.does_player_win(player.player_id):
                    print(f"Player {player.player_id} wins!")
                    print(self.board)
                    return player.player_id
            turn_n += 1
            if turn_n >= self.max_turns:
                print("Draw...")
                return


if __name__ == "__main__":
    from player import Human, MinMaxPlayer, RandomPlayer

    game = Game(player_classes=[MinMaxPlayer, MinMaxPlayer], grids_between_players=2)

    winner = game.run()
    print(f"winner: {winner}")

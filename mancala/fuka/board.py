from typing import Dict

INITIAL_PIECES_FOR_GRIDS_BETWEEN_PLAYERS = 0


class Board:
    def __init__(
        self,
        players_num: int = 2,
        init_pieces_per_grid: int = 3,
        grids_per_player: int = 3,
        grids_between_players: int = 1,
    ):
        self.players_num = players_num
        self.init_pieces_per_grid = init_pieces_per_grid
        self.grids_per_player = grids_per_player
        self.grids_between_players = grids_between_players
        self.data = (
            [init_pieces_per_grid] * grids_per_player
            + [INITIAL_PIECES_FOR_GRIDS_BETWEEN_PLAYERS] * grids_between_players
        ) * players_num
    
    def __str__(self):
        return "|".join([str(i) for i in self.data])
    
    def __eq__(self, other):
        return self.players_num == other.players_num and \
        self.init_pieces_per_grid == other.init_pieces_per_grid and \
        self.grids_per_player == other.grids_per_player and \
        self.grids_between_players == other.grids_between_players and \
        self.data == other.data
        
    def __hash__(self):
        val = 1
        for player_ix in range(self.players_num) :
            for hi in range(self.grids_per_player) :
                val += self.pirces_per_grid
                val += self.data[player_ix][hi]
        return val
        
    def move(self, index: int) -> bool:
        """Move the pieces which are in the grid of the given index.

        :params
        index: int: which grid to be moved

        :return
        whether you can move again or not.
        """
        if index >= len(self.data):
            raise ValueError(f"Invalid index: {index}. index should satisfy index < {len(self.data)}")
        if self._is_grid_between_players(index):
            raise ValueError(f"Invalid index: {index}. The index points grids between players.")

        pieces = self.data[index]

        if pieces == 0:
            raise ValueError(f"The grid with index={index} has no pieces.")

        for i in range(1, pieces + 1):
            index_to_be_incremented = self._add_index(index, i)
            self.data[index_to_be_incremented] += 1

        self.data[index] = 0

        return self._is_grid_between_players(self._add_index(index, pieces))

    def _add_index(self, index, diff):
        return (index + diff) % len(self.data)

    def _is_grid_between_players(self, index: int):
        return index % (self.grids_per_player + self.grids_between_players) >= self.grids_per_player

    def get_players_grids(self, player_id: int) -> Dict[int, int]:
        start_index = self.get_player_start_index(player_id=player_id)
        return {index: self.data[index] for index in range(start_index, start_index + self.grids_per_player)}

    def get_player_start_index(self, player_id: int) -> int:
        return player_id * (self.grids_per_player + self.grids_between_players)

    def get_players_movable_grids(self, player_id: int) -> Dict[int, int]:
        players_grids = self.get_players_grids(player_id=player_id)
        return {key: value for key, value in players_grids.items() if value > 0}

    def does_player_win(self, player_id: int) -> bool:
        movable_grids = self.get_players_movable_grids(player_id=player_id)
        return len(movable_grids) == 0

    def print_board(self):
        for i in range(self.players_num):
            player_start_grid = self.get_player_start_index(i)
            player_last_grid = player_start_grid + self.grids_per_player
            print(self.data[player_start_grid:player_last_grid])
            print(self.data[player_last_grid : player_last_grid + self.grids_between_players])

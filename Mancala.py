# Author: Aline Murillo
# GitHub Username: ahleeneh
# Date: 23-November-2022
# Description: A game of mancala represented by class Player and class Mancala.
#     class Player: data member - name.
#     class Mancala: data members - players, board, list, winner, extra_turn;
#     methods: create_player, print_board, play_game, setup_board, make_move,
#         last_move, check_game_status, set_winner, and return_winner.


class Player:
    """
    A class used to represent a Player to be included in a Mancala game.
    Used by class Mancala.

    Attributes:
        name (str): Name of a Player.
    """

    def __init__(self, name):
        self._name = name

    def get_name(self):
        """Returns the name of a Player."""
        return self._name


class Mancala:
    """
    A class used to represent a game of Mancala with Players.

    Attributes:
        _players (list): List of Player items [p1_item, p2_item]
        _board (list): List containing the number of seeds in each pit.
            [p1 pit1, p1 pit2, p1 pit3, p1 pit4, p1 pit5, p1 pit6, p1 store,
            p2 pit1, p2 pit2, p2 pit3, p2 pit4, p2 pit5, p2 pit6, p2 store]
        _winner (str): String stating that a tie has been found or stating
            the winner of a Mancala game if a winner has been found.
        _extra_turn (int): Set to 1 if a player has earned an extra turn.
    """

    def __init__(self):
        self._players = []
        self._board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self._winner = None
        self._extra_turn = None

    def create_player(self, name):
        """
        Creates a Player item and adds this Player item to a Mancala's players
        list.

        Args:
            name (str): Name of a Player.

        Returns:
            object: Player that has been created.
        """
        new_player = Player(name)
        self._players.append(new_player)
        return new_player

    def print_board(self):
        """
        Displays the current board information to the user in the following
        format: player 1, number of seeds in player 1's store, number of seeds
        in player 1's pit 1-6 as a list, player 2, number of seeds in player
        2's store, and number of seeds in player 2's pit 1-6 as a list.
        """
        print("player1:")
        print(f"store: {self._board[6]}")
        print(self._board[:6])
        print("player2:")
        print(f"store: {self._board[13]}")
        print(self._board[7:13])

    def play_game(self, player_num, pit_num):
        """
        Follows the standard and special rules of Mancala and updates the
        number of seeds in each pit for a specified player and pit index.
        Additionally, performs data validation to ensure a pit index is valid.
        After a player's turn, checks to see if the game has finished. If so,
        the number of seeds in each players' pit and store is updated.

        Args:
            player_num (int): Player 1 or Player 2.
            pit_num (int): Number of pit to make the first move from.

        Returns:
            _board (list): List containing the number of seeds in each pit.
            [p1 pit1, p1 pit2, p1 pit3, p1 pit4, p1 pit5, p1 pit6, p1 store,
            p2 pit1, p2 pit2, p2 pit3, p2 pit4, p2 pit5, p2 pi6, p2 store]
        """
        if pit_num > 6 or pit_num <= 0:
            return "Invalid number for pit index"
        elif self._winner is not None:
            return "Game is ended"
        else:
            self.setup_board(player_num, pit_num)   # initialize board
            if self._extra_turn is not None:        # determine if extra turn
                print(f"player {player_num} take another turn")
                self._extra_turn = None
            self.check_game_status()
        return self._board

    def setup_board(self, player_num, pit_num):
        """
        Helper method for play_game(). If a move has been deemed valid, creates
        a new list where indices 0-6 are the specified player's pits and
        indices 7-13 are the opposing player's pits.

        Args:
            player_num (int): Player 1 or Player 2.
            pit_num (int): Number of pit to make the first move from.
        """
        if player_num == 1:
            board = self._board
            self.make_move(pit_num, board, board[pit_num - 1])
            self._board = board
        else:
            board = self._board[7:] + self._board[:7]
            self.make_move(pit_num, board, board[pit_num - 1])
            self._board = board[7:] + board[:7]

    def make_move(self, pit_num, board, num_of_moves):
        """
        Helper method for setup_board(). Follows the standard rules of Mancala
        and updates the number of seeds in each pit accordingly.

        Args:
            pit_num (int): Index of board to make a move from.
            board (list): List containing the number of seeds in each pit
                with the first 7 pits belonging to the current Player.
            num_of_moves (int): Number of moves a Player can make.
        """
        for move in range(num_of_moves):
            # on the first move, "pick up" all the seeds from the starting pit
            if move == 0:
                board[pit_num - 1] = 0
            if pit_num == 13:                       # skip an opponent's store
                pit_num = 0
            if move == num_of_moves - 1:            # check for special rules
                self.last_move(pit_num, board, board[pit_num])
            else:                                   # "sow" seeds to the right
                board[pit_num] += 1
                pit_num += 1

    def last_move(self, pit_num, board, seeds_in_pit):
        """
        Helper method for make_move(). Follows the special rules of Mancala and
        updates the number of seeds in each pit accordingly.

        Special Rule 1:
            If the last seed lands in a current Player's own empty pit, capture
            all the seeds in the other Player's opposite pit, as well as the
            last seed, and put those seeds in the current Player's own store.

        Special Rule 2:
            If the last seed lands in a Player's own store, take another turn.

        Args:
            pit_num (int): Index of board the last move landed on.
            board (list): List containing the number of seeds in each pit
                with the first 7 pits belonging to the current Player.
            seeds_in_pit (int): Number of seeds the pit at pit_num holds.
        """
        opposite_pit = 12 - pit_num
        if 0 <= pit_num < 6 and seeds_in_pit == 0 and board[opposite_pit] != 0:
            board[6] += board[opposite_pit] + 1     # special rule 1
            board[opposite_pit] = 0
        else:
            if pit_num == 6:                        # special rule 2
                self._extra_turn = 1                # set extra_turn to an int
            board[pit_num] += 1

    def check_game_status(self):
        """
        Helper method for play_game(). Determines if either Player's pits are
        completely empty. If so, the opposing Player takes the seeds remaining
        in their own pits and places these seeds in their own store.
        """
        sum_p1_pits = sum(self._board[:6])
        sum_p2_pits = sum(self._board[7:13])
        if sum_p1_pits == 0:
            new_p2_list = [0, 0, 0, 0, 0, 0, self._board[13] + sum_p2_pits]
            self._board = self._board[:7] + new_p2_list
            self.set_winner()
        elif sum_p2_pits == 0:
            new_p1_list = [0, 0, 0, 0, 0, 0, self._board[6] + sum_p1_pits]
            self._board = new_p1_list + self._board[7:14]
            self.set_winner()

    def set_winner(self):
        """
        Helper method for check_game_status(). Determines which Player has the
        most seeds in their store once a game has finished and sets _winner to
        the appropriate string once a winner or tie has been found.
        """
        if self._board[6] > self._board[13]:
            self._winner = f"Winner is player 1: {self._players[0].get_name()}"
        elif self._board[6] < self._board[13]:
            self._winner = f"Winner is player 2: {self._players[1].get_name()}"
        else:
            self._winner = "It's a tie"

    def return_winner(self):
        """
        Returns _winner (str) if a winner or tie has been found. Otherwise,
        returns a string stating that the Mancala game has not finished.
        """
        if self._winner is not None:
            return self._winner
        return "Game has not ended"


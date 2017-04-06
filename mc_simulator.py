from engine import Point
from collections import Counter

class TennisMonteCarloSimulator:
    """
    Monte-Carlo simulator for a tennis match. Should not be re-used to simulate
    another tennis match after calling simulate()!
    """

    def __init__(self, surface, player_a_label, player_b_label, sets_in_match=3):
        """
            Creates a simulator
            :param surface: The surface the match is played on
            :param player_a_label: The label for player a
            :param player_b_label: The label for player b
            :param sets_in_match: The number of sets in a match. Default is 3.
        """
        self.player_a_label = player_a_label
        self.player_b_label = player_b_label
        self.sets_in_match = sets_in_match
        # By tennis rules, must win at least 6 games to win a set
        self.min_games_to_win_set = 6
        self.surface = surface
        self.point = Point(surface)
        self.debug_enabled = False
    
    def simulate(self):
        """
        Runs the monte-carlo simulation for a match.
        :param player_a_label: The string to return if player a wins
        :param player_b_label: The string to return if player b wins
        :return: The value passed as player_a_label or player_b_label as the
        winner. Does not return any game statistics. (future option?)
        """
        # Instantiates a new point with player A having initiative (serve).
        server = self.player_a_label
        player_a_games = 0
        player_b_games = 0
        player_a_sets = 0
        player_b_sets = 0
        self.points_won = Counter()

        while True:
            # Get the result of the next game
            game_winner = self.get_next_game_winner(server)
            if game_winner is self.player_a_label:
                player_a_games += 1
                if player_a_games >= self.min_games_to_win_set and player_a_games - player_b_games >= 2:
                    if self.debug_enabled:
                        print 'set winner', self.player_a_label, player_a_games, player_b_games
                    player_a_sets += 1
                    # if player has won enough sets
                    if player_a_sets >= self.sets_in_match // 2 + 1:
                        print 'match winner', self.player_a_label, str(player_a_sets), 'to', str(player_b_sets), 'with', self.points_won[self.player_a_label], 'points to', self.points_won[self.player_b_label]
                        return self.player_a_label
                    # reset for the next set
                    player_a_games = 0
                    player_b_games = 0
            else:
                player_b_games += 1
                if player_b_games >= self.min_games_to_win_set and player_b_games - player_a_games >= 2:
                    if self.debug_enabled:
                        print 'set winner', self.player_b_label, player_b_games, player_a_games
                    player_b_sets += 1
                    # if player has won enough sets
                    if player_b_sets >= self.sets_in_match // 2 + 1:
                        print 'match winner', self.player_b_label, str(player_b_sets), 'to', str(player_a_sets), 'with', self.points_won[self.player_b_label], 'points to', self.points_won[self.player_a_label]
                        return self.player_b_label
                    # reset for the next set
                    player_a_games = 0
                    player_b_games = 0
            # Flip the server each game
            server = self.player_b_label if server is self.player_a_label else self.player_a_label

    def get_next_game_winner(self, server):
        """
            Uses get_next_point_winner to assign points to players until a
            player wins the game
            :param server: The label of the player that is the server
            :return: The label of the player that won the game
        """
        player_a_points = 0
        player_b_points = 0
        
        # All games start by serving from the right
        serve_left = False
        while True:
            if self.get_next_point_winner(server, serve_left) is self.player_a_label:
                self.points_won[self.player_a_label] += 1
                player_a_points += 1
                if self.debug_enabled:
                    print 'point winner', self.player_a_label, player_a_points, player_b_points, 'served by', server
                if player_a_points >= 4 and player_a_points - player_b_points >= 2:
                    if self.debug_enabled:
                        print 'game winner', self.player_a_label, player_a_points, player_b_points, 'served by', server
                    return self.player_a_label
            else:
                self.points_won[self.player_b_label] += 1
                player_b_points += 1
                if self.debug_enabled:
                    print 'point winner', self.player_b_label, player_a_points, player_b_points, 'served by', server
                if player_b_points >= 4 and player_b_points - player_a_points >= 2:
                    if self.debug_enabled:
                        print 'game winner', self.player_b_label, player_b_points, player_a_points, 'served by', server
                    return self.player_b_label
            # switch serve side
            serve_left = not serve_left

    def get_next_point_winner(self, server, serve_left=True):
        """
            Uses the two player objects self.player_a and self.player_b to
            simulate a point.
            :param server: The label of the player that is the server
            :param serve_left: boolean of whether the server serves from the left.
            :return: The label of the player that won the point
        """
        
        if server is self.player_b_label:
            self.point.player1 = self.player_b_label
            self.point.player2 = self.player_a_label
        else:
            self.point.player1 = self.player_a_label
            self.point.player2 = self.player_b_label
        
        self.point.serveSide = 'adv' if serve_left else 'deuce'
        return self.point.serve()

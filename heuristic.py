class Heuristic:
    attackScore = [0, 3, 24, 192, 1536, 12288, 98304]
    defenseScore = [0, 1, 9, 81, 729, 6561, 59049]

    def __init__(self, board, turn):
        self.board = board



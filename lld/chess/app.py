class AbstractFactory:
    def create_obj(self, board):
        pass

    def get_obj(self, piece: str):
        pass

class AbstractMoveStrategy:
    def can_move(self, board: "Board", start_row: int, start_col: int, end_row: int, end_col: int):
        pass

class StraightMoveStrategy(AbstractMoveStrategy):
    def can_move(self, board: "Board", start_row: int, start_col: int, end_row: int, end_col: int):
        row_delta = start_row -end_row
        col_delta = end_row -end_col
        if row_delta == 0 and col_delta == 0:
            return False
        i = 0 
        j = start_col -1 if col_delta <0 else start_col +1
        if col_delta == 0:
            i = start_row -1 if row_delta <0 else start_row +1
            j = 0
        while i != end_row and j != end_col:
            if board.get_piece(i, j) != None:
                return False
            i = 0 
            j = j -1 if col_delta <0 else j +1
            if col_delta == 0:
                i = i -1 if row_delta <0 else i +1
                j = 0

        return True

class DiagonalMoveStrategy(AbstractMoveStrategy):
    def can_move(self, board: "Board", start_row: int, start_col: int, end_row: int, end_col: int):
        row_delta = start_row -end_row
        col_delta = end_row -end_col
        if row_delta != col_delta:
            return False
        i = start_row -1 if row_delta <0 else start_row +1
        j = start_col -1 if col_delta <0 else start_col +1
        while i != end_row and j != end_col:
            if board.get_piece(i, j) != None:
                return False
            i = i -1 if row_delta <0 else i +1
            j = j -1 if col_delta <0 else j +1

        return True

class PieceFactory(AbstractFactory):
    def __init__(self):
        super().__init__()
        self.identifier_to_cls_mapping = {
            "K": lambda col, identifier: King(col, identifier),
            "P": lambda col, identifier: Pawn(col, identifier),
            "H": lambda col, identifier: Knight(col, identifier),
            "B": lambda col, identifier: ChessPiece(col, identifier, [DiagonalMoveStrategy()]),
            "R": lambda col, identifier: ChessPiece(col, identifier, [StraightMoveStrategy()]),
            "Q": lambda col, identifier: ChessPiece(col, identifier, [StraightMoveStrategy(), DiagonalMoveStrategy()]),
        }

    def create_obj(self, state):
        color, identifier = list(state)
        return self.identifier_to_cls_mapping[
            identifier
        ](color, identifier)

class ChessPiece:
    def __init__(self, color, identifier, move_strategies = []):
        self.color = color
        self.identifier = identifier
        self.move_strategies = move_strategies

    def can_move(self, board, start_row: int, start_col: int, end_row: int, end_col: int):
        for move in self.move_strategies:
            if move.can_move(board, start_row, start_col, end_row, end_col):
                return True
        return False
    
    def __repr__(self):
        return f"{self.color}{self.identifier}"

class King(ChessPiece):
    def can_move(self, board, start_row: int, start_col: int, end_row: int, end_col: int):
        step_row = abs(start_row -end_row)
        step_col = abs(start_col -start_row)
        return step_row <= 1 and step_col <= 1

class Pawn(ChessPiece):
    def can_move(self, board, start_row: int, start_col: int, end_row: int, end_col: int):
        step_row = start_row -end_row
        step_col = start_col -end_col
        start_piece = board.get_piece(start_row, start_col)
        if start_piece.color == "W" and step_row >0: 
            return False
        if start_piece.color == "B" and step_row <0: 
            return False
        if abs(step_row) == 1:
            if abs(step_col) == 1:
                return board.state[end_row][end_col] != ""
            elif step_col == 0:
                return True
        return False

class Knight(ChessPiece):
    def can_move(self, board, start_row: int, start_col: int, end_row: int, end_col: int):
        row_delta = abs(end_row - start_row)
        col_delta = abs(end_col - start_col)
        return (row_delta == 2 and col_delta == 1) or (row_delta == 1 and col_delta == 2)

class Board:
    def __init__(self, state):
        self.state = [[None for _ in range(len(state[0]))] for _ in range(len(state))]
        self.piece_factory = PieceFactory()
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != "":
                    self.state[i][j] = self.piece_factory.create_obj(
                        state[i][j]
                    )
    
    def valid(self, row, col):
        return 0 <= row < len(self.state) and 0 <= col < len(self.state[0])

    def get_piece(self, row, col):
        if self.valid(row, col):
            return self.state[row][col]
        return None
    
    def move(self, start_row: int, start_col: int, end_row: int, end_col: int):
        if not (self.valid(start_row, start_col) and self.valid(end_row, end_col)):
            return "invalid", False
        start_piece = self.get_piece(start_row, start_col)
        end_piece = self.get_piece(end_row, end_col)
        if not start_piece: return "invalid", False
        if start_piece is end_piece: return "invalid", False
        if end_piece is not None and start_piece.color == end_piece.color: return "invalid", False

        if start_piece.can_move(board=self, start_row=start_row, start_col=start_col, end_row=end_row, end_col=end_col):
            self.state[start_row][start_col] = None
            self.state[end_row][end_col] = start_piece
            if end_piece:
                result = f"{end_piece.color}{end_piece.identifier}, {start_piece.color}{start_piece.identifier} moves from {start_row}, {start_col} to {end_row}, {end_col} and kills {end_piece.color}{end_piece.identifier}" 
            else:
                result = f"'', {start_piece.color}{start_piece.identifier} moves from {start_row}, {start_col} to {end_row}, {end_col}"
            if isinstance(end_piece, King):
                return result, True
            return result, False
        return "invalid", False

class Chess:
    def __init__(self):
        self.board = Board(
            [
                ["WR","WH","WB","WQ","WK","WB","WH","WR"],
                ["WP","WP","WP","WP","WP","WP","WP","WP"],
                ["","","","","","","",""],
                ["","","","","","","",""],
                ["","","","","","","",""],
                ["","","","","","","",""],
                ["BP","BP","BP","BP","BP","BP","BP","BP"],
                ["BR","BH","BB","BQ","BK","BB","BH","BR"]
            ]
        )
        self.next_turn = 0  # white
        self.state = 0  # in progress

    def move(self, start_row: int, start_col: int, end_row: int, end_col: int):
        result, game_over = self.board.move(start_row, start_col, end_row, end_col)
        if result == "invalid": return result
        self.next_turn ^= 1
        if game_over:
            self.state = 1 if self.next_turn == 1 else 2
            self.next_turn = -1
            return f"{result}, {['W', 'B'][self.state -1]} has won"
        return f"{result}, continue"
    
    def get_next_turn(self) -> int:
        return self.next_turn

    def get_game_state(self) -> int:
        return self.state

chess = Chess()

for i in [
    (1, 5, 2, 5),
    (6, 6, 5, 6),
    (2, 5, 3, 5),
    (6, 2, 5, 2),
    (0, 1, 2, 2),
    (6, 4, 5, 4),
    (1, 7, 2, 7),
    (7, 6, 5, 7),
    (2, 2, 3, 4),
    (6, 5, 5, 5),
    (3, 4, 5, 5),
    (6, 0, 5, 0),
    (5, 5, 7, 4)
    # (7, 7, 6, 6)
]:
    print(i)
    print(chess.move(*i))
    print(chess.get_next_turn())
    print(chess.get_game_state())
    print("+++++++++")
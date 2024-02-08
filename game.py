from flask import Flask, jsonify

app = Flask(__name__)

# You'll need a 'Game' class with the current board state and functionality
# to update it based on a player move (similar to your JavaScript logic).
class Game:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = self._create_board()  # Initialize an empty board
        self.current_player = 1  # Player 1 starts

    def _create_board(self):
        """Creates an empty Connect Four board"""
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def make_move(self, col):
        """Drops a piece in the specified column, if possible"""
        for row in range(self.rows - 1, -1, -1):  # Start from the bottom
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.switch_player()

                # Reward logic
                if self.check_winner() == self.current_player:
                    return 1  # Reward for winning 
                elif self.is_board_full():
                    return 0  # A small reward or 0 for a draw
                else:
                    return -0.1  # Slight negative reward for non-winning moves 

        # Handle the case where the column is full
        raise ValueError("Column is full") 


        
    

    def switch_player(self):
        """Switches to the next player"""
        self.current_player = 2 if self.current_player == 1 else 1

    def check_winner(self):
        """Checks for horizontal, vertical, and diagonal wins"""
        # Horizontal check
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] != 0 and \
                   self.board[row][col] == self.board[row][col + 1] == \
                   self.board[row][col + 2] == self.board[row][col + 3]:
                    return self.board[row][col]  # Return the winning player

        # Vertical check
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if self.board[row][col] != 0 and \
                   self.board[row][col] == self.board[row + 1][col] == \
                   self.board[row + 2][col] == self.board[row + 3][col]:
                    return self.board[row][col]

        # Diagonal checks \ (downward slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if self.board[row][col] != 0 and \
                   self.board[row][col] == self.board[row + 1][col + 1] == \
                   self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                    return self.board[row][col]

        # Diagonal checks / (upward slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] != 0 and \
                   self.board[row][col] == self.board[row - 1][col + 1] == \
                   self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
                    return self.board[row][col]

        return None  # No winner found

    def is_board_full(self):
        """Checks if the board is full (stalemate)"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    return False  # Found an empty cell
        return True  # No empty cells left

    def print_board(self):
        """Displays the board state in the console (for debugging)"""
        for row in self.board:
            print(row) 

current_game = Game() 

@app.route('/get_ai_move', methods=['POST'])
def get_ai_move():
    # 1. Receive the board state from the frontend's POST request
    # 2. (Future Work) Call your reinforcement learning agent to calculate move
    # 3. For now, maybe return a random valid move for testing
    # 4. Return the AI's calculated move in JSON format 
    return jsonify({'move': 2}) # Replace '2' with actual AI move

if __name__ == '__main__':
    app.run(debug=True)



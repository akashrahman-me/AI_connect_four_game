Let's review the full code of this project.

index.html

```html
<!DOCTYPE html>
<html>
   <head>
      <title>Connect Four</title>
      <link rel="stylesheet" href="style.css" />
   </head>
   <body>
      <h1>Connect Four</h1>
      <div id="game-board"></div>
      <div id="status"></div>
      <button onclick="createBoard(); renderBoard()">Reset Game</button>

      <script src="script.js"></script>
   </body>
</html>
```

style.css

```css
#game-board {
   display: grid;
   grid-template-columns: repeat(7, 50px); /* 7 columns */
   grid-template-rows: repeat(6, 50px); /* 6 rows */
   border-collapse: collapse;
}

#game-board > div {
   /* Each cell of the board */
   width: 50px;
   height: 50px;
   border: 1px solid black;
   border-radius: 50%; /* Create circular pieces */
   background-color: white; /* Initially empty */
}

#status {
   text-align: center;
}
```

script.js

```js
// Constants
const COLS = 7;
const ROWS = 6;
let board = []; // Our 2D array to represent the game board

// Initialize the board with empty values
function createBoard() {
   for (let row = 0; row < ROWS; row++) {
      board[row] = []; // Create a new array for each row
      for (let col = 0; col < COLS; col++) {
         board[row][col] = 0; // 0 represents an empty cell
      }
   }
}

// A simple function to render the board on the HTML initially
function renderBoard() {
   const gameBoardDiv = document.getElementById("game-board");
   gameBoardDiv.innerHTML = ""; // Clear any existing content

   for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS; col++) {
         const cell = document.createElement("div");
         gameBoardDiv.appendChild(cell);
      }
   }
}

let currentPlayer = 1; // Start with player 1
const statusDiv = document.getElementById("status");

function handleClick(column) {
   // Find the lowest available row in the clicked column
   for (let row = ROWS - 1; row >= 0; row--) {
      if (board[row][column] === 0) {
         board[row][column] = currentPlayer; // Place the piece
         renderBoard(); // Update the display
         checkWinner(); // Check if the move resulted in a win
         switchPlayer(); // Move to the next player
         break;
      }
   }
}

async function getAIMove() {
   const response = await fetch("/get_ai_move", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({board: board}),
   });

   if (response.ok) {
      const data = await response.json();
      const aiMove = data.move;
      handleClick(aiMove); // Reuse your handleClick logic
   } else {
      // Handle error
   }
}

function switchPlayer() {
   currentPlayer = currentPlayer === 1 ? 2 : 1;
   statusDiv.textContent = `Player ${currentPlayer}'s turn`;

   if (currentPlayer === 2) {
      // Assuming Player 2 is the AI
      getAIMove();
   }
}

// Very basic win-checking (we'll improve this later)
function checkWinner() {
   if (currentPlayer === 1) {
      statusDiv.textContent = "Player 1 wins!";
   } else {
      statusDiv.textContent = "Player 2 wins!";
   }
}

// Add click event listeners to the columns
function addClickListeners() {
   const gameBoardDiv = document.getElementById("game-board");
   for (let col = 0; col < COLS; col++) {
      // We use closures to capture the correct column index
      gameBoardDiv.children[col].addEventListener("click", () => handleClick(col));
   }
}

function checkHorizontalWin() {
   for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS - 3; col++) {
         // Check sequences of 4
         if (
            board[row][col] !== 0 &&
            board[row][col] === board[row][col + 1] &&
            board[row][col] === board[row][col + 2] &&
            board[row][col] === board[row][col + 3]
         ) {
            return board[row][col]; // Return the winning player
         }
      }
   }
   return null; // No horizontal win
}

function checkVerticalWin() {
   for (let col = 0; col < COLS; col++) {
      for (let row = 0; row < ROWS - 3; row++) {
         if (
            board[row][col] !== 0 &&
            board[row][col] === board[row + 1][col] &&
            board[row][col] === board[row + 2][col] &&
            board[row][col] === board[row + 3][col]
         ) {
            return board[row][col];
         }
      }
   }
   return null; // No vertical win
}

function checkDiagonalWin() {
   // Check for diagonals sloping up (/)
   for (let col = 0; col < COLS - 3; col++) {
      for (let row = 0; row < ROWS - 3; row++) {
         if (
            board[row][col] !== 0 &&
            board[row][col] === board[row + 1][col + 1] &&
            board[row][col] === board[row + 2][col + 2] &&
            board[row][col] === board[row + 3][col + 3]
         ) {
            return board[row][col];
         }
      }
   }

   // Check for diagonals sloping down (\)
   for (let col = 0; col < COLS - 3; col++) {
      for (let row = 3; row < ROWS; row++) {
         if (
            board[row][col] !== 0 &&
            board[row][col] === board[row - 1][col + 1] &&
            board[row][col] === board[row - 2][col + 2] &&
            board[row][col] === board[row - 3][col + 3]
         ) {
            return board[row][col];
         }
      }
   }

   return null; // No diagonal wins
}

function isBoardFull() {
   for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS; col++) {
         if (board[row][col] === 0) {
            return false; // There's at least one empty cell
         }
      }
   }
   return true; // The board is completely full
}

// Update the checkWinner function
function checkWinner() {
   let winner = checkHorizontalWin() || checkVerticalWin() || checkDiagonalWin();

   if (winner) {
      statusDiv.textContent = `Player ${winner} wins!`;
   }

   if (isBoardFull()) {
      statusDiv.textContent = "It's a draw!";
   }
}

// Start the game
createBoard();
renderBoard();
addClickListeners(); // Add click functionality
statusDiv.textContent = `Player ${currentPlayer}'s turn`;
```

app.py

```python
from flask import Flask, jsonify, request
from stable_baselines3 import DQN
import numpy as np

from game import Game

app = Flask(__name__)

current_game = Game()
ai_model = DQN.load("connect_four_rl_agent") # Load your trained AI model

@app.route('/get_ai_move', methods=['POST'])
def get_ai_move():
    data = request.get_json()
    board_state = data['board']

    # Optional: Ensure board_state is a NumPy array for compatibility
    # with some RL libraries
    board_state = np.array(board_state)

    action, _ = ai_model.predict(board_state)
    return jsonify({'move': int(action)})  # Ensure action is sent as an integer

```

game.py

```python
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

```

train_rl_agent.py

```python
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback

from game import Game  # Import your Game class

# Assuming you already have your 'Game' class defined
env = make_vec_env(lambda: Game(), n_envs=1)  # Create training environment

model = DQN('MlpPolicy', env, verbose=1)  # Configure the DQN model
model.learn(total_timesteps=100000)  # Train the agent train_rl_agent.py

# Constants (Adjust as needed)
TOTAL_TRAINING_TIMESTEPS = 500000
SAVE_MODEL_INTERVAL = 10000  # Save the model every 10000 training steps

# Create the training environment (single environment at a time for now)
env = make_vec_env(lambda: Game(), n_envs=1)

# Create the DQN model with a suitable network architecture ('MlpPolicy' is common)
model = DQN('MlpPolicy', env, verbose=1, tensorboard_log="./tensorboard/")

# Checkpoint callback to save your model during training
checkpoint_callback = CheckpointCallback(save_freq=SAVE_MODEL_INTERVAL,
                                         save_path='./models/',
                                         name_prefix='connect_four_ai')

# Train the agent!
model.learn(total_timesteps=TOTAL_TRAINING_TIMESTEPS, callback=checkpoint_callback)

# Save the final trained model
model.save("connect_four_rl_agent")

```

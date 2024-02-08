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

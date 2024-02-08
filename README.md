# AI-Powered Connect Four Game

Play Connect Four against a reinforcement learning-trained AI! This project combines classic game logic with cutting-edge AI techniques.

## Project Overview

-  **Frontend:** HTML, CSS, and JavaScript create the visual game board and gameplay interaction.
-  **Backend:** A Python Flask server handles API communication and houses the trained AI model.
-  **Reinforcement Learning:** Stable Baselines3 was used to train a Deep Q-Network (DQN) agent to play Connect Four strategically.

## Prerequisites

-  **Python 3.x:** Ensure you have Python installed. Check by running `python --version` in your terminal.
-  **Required Libraries:**
   -  Flask
   -  Stable Baselines3
   -  NumPy
-  **(Optional for Retraining the AI):** Tensorboard

## How to Install Dependencies

1. Open your terminal or command prompt.
2. Navigate to the project's root directory:
   ```bash
   cd /path/to/your/project
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Game

1. **Start the Backend Server:**
   bash
   python app.py

   ```
   This will typically start the Flask server on `http://127.0.0.1:5000/`.

   ```

2. **Open the Game in Your Browser:**  
   Open `index.html` in your web browser.

## How to Retrain the AI (Optional)

1. Run `train_rl_agent.py`:

   ```bash
   python train_rl_agent.py
   ```

   Be aware that training AI agents can be computationally intensive and time-consuming.

2. **(If Using TensorBoard):** Start TensorBoard to monitor the learning process.

   ```bash
   tensorboard --logdir=./tensorboard

   ```

## Project Structure

-  `index.html`: Main HTML file for the game interface.
-  `style.css`: Styling for the Connect Four board.
-  `script.js`: JavaScript code for frontend game logic and AI communication.
-  `app.py`: Python Flask backend, loads the AI model, and handles the `/get_ai_move` endpoint.
-  `game.py`: Contains the Python `Game` class representing the game board and rules.
-  `train_rl_agent.py`: Script for training (or re-training) the reinforcement learning model.
-  `requirements.txt` (Optional): A file listing the required Python libraries.

## Notes

-  The backend is set up to use a pre-trained model. Make sure the path in `app.py` corresponds to where you have your `connect_four_rl_agent` model saved.
-  Adjust paths in the instructions if your file organization differs.

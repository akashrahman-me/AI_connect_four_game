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

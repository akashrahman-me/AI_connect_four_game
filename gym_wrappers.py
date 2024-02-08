import gym 
import numpy as np
from game import Game

class ConnectFourGymEnv(gym.Env):
    def __init__(self):
        self.game = Game()  # Initialize your Game class
        self.action_space = gym.spaces.Discrete(self.game.cols)  # Actions = Number of columns
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=(self.game.rows, self.game.cols), dtype=np.uint8)

    def reset(self):
        self.game.reset_game()  # Assuming your Game class has a reset function
        return self.game.board  # Return the NumPy board directly as observation

    def step(self, action):
        self.game.make_move(action)  

        observation = self.game.board 
        reward = self.calculate_reward()
        done = self.game.is_board_full() or self.game.check_winner()  
        info = {}  # You might include additional information here

        return observation, reward, done, info

    def calculate_reward(self):
        """Simple reward function - adjust as needed"""
        if self.game.check_winner() == self.game.current_player:
            return 1  # Reward for winning
        elif self.game.is_board_full():
            return 0  # Small reward or 0 for a draw
        else:
            return -0.1  # Slight negative reward for non-winning moves 
        
    def seed(self, seed=None):
        pass  # For Connect Four, seeding might not be directly relevant


from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback 
from gym_wrappers import ConnectFourGymEnv

env = make_vec_env(lambda: ConnectFourGymEnv(), n_envs=1) 

model = DQN('MlpPolicy', env, verbose=1)  # Configure the DQN model
model.learn(total_timesteps=100000)  # Train the agent train_rl_agent.py

# Constants (Adjust as needed)
TOTAL_TRAINING_TIMESTEPS = 500000
SAVE_MODEL_INTERVAL = 10000  # Save the model every 10000 training steps


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

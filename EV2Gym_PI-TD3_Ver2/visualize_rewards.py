import re
import matplotlib.pyplot as plt
import numpy as np
import os

def visualize_log(log_file='output.log'):
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found. Please ensure it is in the same directory.")
        return

    time_steps = []
    rewards = []
    eval_steps = []
    eval_rewards = []

    # Regex patterns
    episode_pattern = re.compile(r"Total T: (\d+) .* Reward: ([-\d.]+)")
    eval_pattern = re.compile(r"Evaluation over \d+ episodes: ([-\d.]+)")

    current_step = 0

    print(f"Parsing {log_file}...")
    with open(log_file, 'r') as f:
        for line in f:
            # Check for training episodes
            match_ep = episode_pattern.search(line)
            if match_ep:
                step = int(match_ep.group(1))
                reward = float(match_ep.group(2))
                time_steps.append(step)
                rewards.append(reward)
                current_step = step
                continue

            # Check for evaluation blocks
            # Note: The evaluation line usually follows the training logs.
            # We assume it corresponds to the most recent 'Total T' seen or slightly after.
            match_eval = eval_pattern.search(line)
            if match_eval:
                eval_reward = float(match_eval.group(1))
                eval_steps.append(current_step)
                eval_rewards.append(eval_reward)

    print(f"Parsed {len(time_steps)} training episodes and {len(eval_steps)} evaluation points.")

    if not time_steps:
        print("No training data found in log file.")
        return

    # Cumulative average helper
    def cumulative_average(data):
        return np.cumsum(data) / np.arange(1, len(data) + 1)

    plt.figure(figsize=(12, 6))

    # Plot raw training rewards (scatter or faint line)
    plt.plot(time_steps, rewards, label='Episode Reward', color='lightblue', alpha=0.3)

    # Plot cumulative average of training rewards
    cum_rewards = cumulative_average(rewards)
    plt.plot(time_steps, cum_rewards, label='Cumulative Avg (All-time)', color='blue')

    # Plot evaluation rewards (points + line)
    if eval_rewards:
        plt.plot(eval_steps, eval_rewards, label='Evaluation Avg', color='red', marker='o', linewidth=2)

    plt.xlabel('Total Time Steps (T)')
    plt.ylabel('Reward')
    plt.title('Training and Evaluation Reward Trends')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    output_image = 'training_plot.png'
    plt.savefig(output_image)
    print(f"Plot saved to {output_image}")
    plt.show()

if __name__ == "__main__":
    visualize_log()

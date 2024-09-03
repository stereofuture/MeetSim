import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress

from agent import Agent
from occupation import Occupation
from scheduling import schedule_meetings

def parse_args():
    parser = argparse.ArgumentParser(description="Run meeting simulations.")
    parser.add_argument('-n', '--num_simulations', type=int, default=1, help="Number of simulations to run.")
    return parser.parse_args()

def run_simulation(agents):
    meetings = schedule_meetings(agents)
    
    # Debugging meeting times
    debug_meeting_times(agents)
    
    results = {}
    for agent in agents:
        results[agent.id] = agent.count_meeting_time()
    return results

def run_multiple_simulations(num_simulations, occupation_counts):
    agents = []
    agent_id = 1
    
    for occupation, count in occupation_counts.items():
        for _ in range(count):
            agents.append(occupation.generate_agent(agent_id))
            agent_id += 1

    aggregate_results = {agent.id: [] for agent in agents}
    
    for simulation_number in range(num_simulations):
        simulation_results = run_simulation(agents)
        for agent_id, time_spent in simulation_results.items():
            aggregate_results[agent_id].append(time_spent)
        print(f"Simulation {simulation_number} Complete. Clearing Schedules")
        for agent in agents:
            agent.clear_calendar()
        
    
    mean_meeting_times = {agent_id: np.mean(times) for agent_id, times in aggregate_results.items()}
    return agents, mean_meeting_times

def plot_correlations(agents, mean_meeting_times, plot_name):
    """Plot correlations between agent characteristics and the mean time spent in meetings."""

    # Create a dictionary to store agent characteristics and mean meeting times
    data = {
        "Meeting Proclivity": [agent.meeting_proclivity for agent in agents],
        "Meeting Expansiveness": [agent.meeting_expansiveness for agent in agents],
        "Meeting Depth": [agent.meeting_depth for agent in agents],
        "Pay": [agent.pay for agent in agents],
        "Mean Meeting Time": [mean_meeting_times[agent.id] for agent in agents]
    }

    # Convert the dictionary to a Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Set up the figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid of subplots
    axs = axs.flatten()  # Flatten the 2x2 array of axes into a 1D array for easy iteration
    
    characteristics = ["Meeting Proclivity", "Meeting Expansiveness", "Meeting Depth", "Pay"]

    # Plot each characteristic against Mean Meeting Time in a subplot
    for i, characteristic in enumerate(characteristics):
        x = df[characteristic]
        y = df["Mean Meeting Time"]

        # Calculate the correlation coefficient
        corr = np.corrcoef(x, y)[0, 1]

        # Calculate linear regression (trendline)
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        trendline = slope * x + intercept

        # Plot scatterplot
        sns.scatterplot(ax=axs[i], x=x, y=y)

        # Plot trendline
        axs[i].plot(x, trendline, color='red', linestyle='--')

        # Set titles and labels
        axs[i].set_title(f"{characteristic} vs Mean Meeting Time\n"
                         f"Correlation: {corr:.2f}, Variance: {np.var(y):.2f}")
        axs[i].set_xlabel(characteristic)
        axs[i].set_ylabel("Mean Meeting Time")
    
    # Adjust layout and save the figure
    plt.tight_layout()  # Adjust subplots to fit in the figure area
    plt.savefig(f"{plot_name}.png")  # Save the entire figure as a single PNG file
    plt.close()  # Close the figure to free up memory

def debug_meeting_times(agents):
    for agent in agents:
        printed_meetings = []
        print(f"Agent {agent.id} - Checking calendar...")
        total_meeting_time = 0
        for day, day_slots in agent.calendar.items():
            for time_slot, meeting in day_slots:
                if meeting and meeting.id not in printed_meetings:
                    # print(f"  {day}, {time_slot}, {meeting.id} : Meeting Duration = {meeting.duration} minutes")
                    total_meeting_time += meeting.duration
                    printed_meetings.append(meeting.id)
        if total_meeting_time > 0:
            print(f"Total Meeting Time for Agent {agent.id}: {total_meeting_time} minutes")
        else:
            print(f"No meetings scheduled for Agent {agent.id}")


# Define occupations
developer = Occupation("Developer", (0.2, 0.1), (0.2, 0.1), (0.2, 0.1), (100000, 20000))
manager = Occupation("Manager", (0.5, 0.1), (0.5, 0.1), (0.5, 0.1), (125000, 25000))
executive = Occupation("Executive", (0.7, 0.1), (0.6, 0.1), (0.2, 0.1), (200000, 50000))

# Define the number of agents per occupation
occupation_counts = {
    developer: 10,
    manager: 5,
    executive: 2
}

if __name__ == "__main__":
    args = parse_args()
    agents, mean_meeting_times = run_multiple_simulations(args.num_simulations, occupation_counts)
    plot_correlations(agents, mean_meeting_times, "primary_correlations_plot")

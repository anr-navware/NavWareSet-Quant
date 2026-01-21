# THIS PYTHON SCRIPT GOES THROUGH ALL TRACK FILES IN A DIRECTORY AND PLOTS THEM USING MATPLOTLIB
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_track_data(filepath):
    """
    Load track data from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with the track data
    """
    return pd.read_csv(filepath)

def plot_single_track_detailed(ax, df, track_filename):
    """
    Plot a single track with both robot and participant(s) trajectories.
    Handles two CSV formats:
    1. Column-based: timestamp, x, y, column, robot_x, robot_y, robot_yaw_rad
    2. Multi-participant: timestamp, robot_x, robot_y, robot_yaw_rad, x1, y1, x2, y2, ...
    
    Args:
        ax: Matplotlib axes object
        df: DataFrame containing the track data
        track_filename: Name of the track file
    """
    # Plot robot trajectory
    robot_x = df["robot_x"].values
    robot_y = df["robot_y"].values
    ax.plot(robot_x, robot_y, 'b-', linewidth=2, label='Robot', alpha=0.8)
    ax.scatter(robot_x[0], robot_y[0], color='blue', s=100, marker='o', zorder=5, label='Robot start')
    ax.scatter(robot_x[-1], robot_y[-1], color='blue', s=100, marker='x', zorder=5, label='Robot end')
    
    colors = ['red', 'green', 'orange', 'purple', 'brown']
    
    # Format 1: Column-based (x, y, column columns)
    if "x" in df.columns and "y" in df.columns and "column" in df.columns:
        participants = sorted(df["column"].unique())
        for idx, participant_id in enumerate(participants):
            participant_data = df[df["column"] == participant_id]
            part_x = participant_data["x"].values
            part_y = participant_data["y"].values
            
            color = colors[idx % len(colors)]
            ax.plot(part_x, part_y, color=color, linewidth=2, linestyle='--', 
                   label=f'Participant {int(participant_id)}', alpha=0.8)
            ax.scatter(part_x[0], part_y[0], color=color, s=100, marker='s', zorder=5)
            ax.scatter(part_x[-1], part_y[-1], color=color, s=100, marker='^', zorder=5)
    
    # Format 2: Multi-participant columns (x1, y1, x2, y2, ...)
    elif any(col.startswith('x') and col[1:].isdigit() for col in df.columns):
        # Extract participant columns
        participant_cols = {}
        for col in df.columns:
            if col.startswith('x') and col[1:].isdigit():
                participant_num = col[1:]
                if participant_num not in participant_cols:
                    participant_cols[participant_num] = {}
                participant_cols[participant_num]['x'] = col
            elif col.startswith('y') and col[1:].isdigit():
                participant_num = col[1:]
                if participant_num not in participant_cols:
                    participant_cols[participant_num] = {}
                participant_cols[participant_num]['y'] = col
        
        # Plot each participant
        for idx, (participant_id, cols) in enumerate(sorted(participant_cols.items())):
            if 'x' in cols and 'y' in cols:
                part_x = df[cols['x']].values
                part_y = df[cols['y']].values
                
                # Skip if all NaN
                if np.isnan(part_x).all() or np.isnan(part_y).all():
                    continue
                
                color = colors[idx % len(colors)]
                ax.plot(part_x, part_y, color=color, linewidth=2, linestyle='--', 
                       label=f'Participant {participant_id}', alpha=0.8)
                ax.scatter(part_x[0], part_y[0], color=color, s=100, marker='s', zorder=5)
                ax.scatter(part_x[-1], part_y[-1], color=color, s=100, marker='^', zorder=5)

def plot_each_track_individually(root_dir="selected_tracks", output_dir="plots"):
    """
    Plot each track file individually with robot and participant(s) trajectories.
    Saves all plots to PNG files in the output directory.
    
    Args:
        root_dir: Root directory containing pose subdirectories
        output_dir: Directory to save the plots
    """
    root_path = Path(root_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Collect all CSV files
    all_files = sorted(root_path.rglob("*.csv"))
    
    if not all_files:
        print(f"No CSV files found in {root_dir}")
        return
    
    total_files = len(all_files)
    print(f"Found {total_files} track files. Saving plots to '{output_dir}/'...")
    
    # Plot each track file and save
    for file_idx, track_file in enumerate(all_files, 1):
        try:
            df = load_track_data(track_file)
            
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_single_track_detailed(ax, df, track_file.name)
            
            ax.set_xlabel("X (m)")
            ax.set_ylabel("Y (m)")
            ax.set_title(f"{track_file.name}\n({file_idx}/{total_files})")
            ax.grid(True, alpha=0.3)
            ax.axis("equal")
            ax.legend(loc='best')
            
            plt.tight_layout()
            
            # Save the plot
            output_filename = output_path / f"{file_idx:04d}_{track_file.stem}.png"
            plt.savefig(output_filename, dpi=150, bbox_inches='tight')
            
            if file_idx % 50 == 0 or file_idx == total_files:
                print(f"[{file_idx}/{total_files}] Saved: {output_filename.name}")
            
            plt.close()
            
        except Exception as e:
            print(f"Error loading {track_file}: {e}")
    
    print(f"\nFinished! All {total_files} plots saved to '{output_dir}/' directory.")

if __name__ == "__main__":
    print("Plotting each track individually with robot and participant trajectories...")
    plot_each_track_individually()

# NavWareSet-Quant

Quantitative analysis of 541 robot tracks from the NavWareSet dataset. This project implements a comprehensive framework for evaluating robot social navigation behavior through kinematic and distance-based metrics.

## Overview

This repository analyzes robot navigation behavior in human-populated environments across 5 distinct scenarios. The analysis computes 6 key metrics for each of 20 scenario-robot-behavior combinations (5 scenarios × 2 robots × 2 behaviors), providing quantitative insights into navigation performance and social compliance.

## Project Structure

```
NavWareSet-Quant/
├── NavWareSet_Quantitative_Analysis.ipynb    # Main analysis notebook
├── plot_all_tracks.py                         # Visualization script for individual tracks
├── NavWareSet_Quantitative_Analysis_Results.csv  # Output results table
├── selected_tracks/                           # Track data directory
│   ├── 01_poses/                             # Frontal Approach tracks
│   ├── 02_poses/                             # Pedestrian Obstruction tracks
│   ├── 03_poses/                             # Blind Corner tracks
│   ├── 04_poses/                             # Perpendicular Crossing tracks
│   ├── 05_poses/                             # Circular Crossing tracks
│   └── ... (additional scenario directories)
└── README.md                                  # This file
```

## Data Formats

The project handles two different CSV track formats seamlessly:

### Format 1: Column-Based Format
Used for multi-participant scenarios where each row represents a single human participant at a given timestamp.

```csv
timestamp,x,y,column,robot_x,robot_y,robot_yaw_rad
1730817548102506496,0.5,1.2,1,2.1,3.5,-0.52
1730817548102506496,0.8,0.9,2,2.1,3.5,-0.52
1730817548202506496,0.5,1.3,1,2.2,3.6,-0.50
```

**Columns:**
- `timestamp`: Unix nanosecond timestamp
- `x, y`: Human participant coordinates (meters)
- `column`: Participant identifier (1-5)
- `robot_x, robot_y`: Robot position (meters)
- `robot_yaw_rad`: Robot orientation (radians)

### Format 2: XY-Pairs Format
Used for fixed human position scenarios with up to 5 human participants.

```csv
timestamp,robot_x,robot_y,robot_yaw_rad,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5
1730818675992630528,1.5,2.0,-0.25,0.2,1.0,0.9,1.5,1.8,0.5,2.1,1.1,2.5,0.9
1730818675992730528,1.6,2.1,-0.23,0.2,1.0,0.9,1.5,1.8,0.5,2.1,1.1,2.5,0.9
```

**Columns:**
- `timestamp`: Unix nanosecond timestamp
- `robot_x, robot_y`: Robot position (meters)
- `robot_yaw_rad`: Robot orientation (radians)
- `x1-x5, y1-y5`: Coordinates of up to 5 fixed human participants (meters)

## Metrics

The analysis calculates 6 quantitative metrics for robot social navigation evaluation:

### 1. **Vavg** - Average Velocity (m/s)
Global average speed across all robot tracks. Computed as total distance traveled divided by total time.

### 2. **Aavg** - Average Acceleration (m/s²)
Time-weighted average of instantaneous acceleration changes. Indicates smoothness and aggressiveness of motion.

### 3. **Javg** - Average Jerk (m/s³)
Time-weighted average of rate of acceleration change. Measures motion comfort and predictability.

### 4. **PLavg** - Average Path Length (m)
Mean total distance traveled across all tracks in a scenario. Indicates navigation efficiency.

### 5. **PSC** - Personal Space Compliance (%)
Percentage of timestamps where the robot maintains minimum safe distance (default 0.5m) from all humans. Higher values indicate better social awareness.

### 6. **DHmin** - Average Minimal Distance (m)
Average of the closest approach distance achieved in each track. Directly measures human-robot proximity.

## Scenarios

The analysis covers 5 distinct navigation scenarios:

1. **Frontal Approach** (01_poses): Robot approaches human from front
2. **Pedestrian Obstruction** (02_poses): Robot navigates around obstructing human
3. **Blind Corner** (03_poses): Robot encounters human at hallway corner
4. **Perpendicular Crossing** (04_poses): Robot crosses perpendicular to human path
5. **Circular Crossing** (05_poses): Robot and human perform circular trajectories

## Robot and Behavior Types

- **Robots**: HSR (Humanoid Service Robot), Jackal (wheeled platform)
- **Behaviors**: Compliant (socially-aware navigation), Non-compliant (minimal social awareness)

This creates 5 × 2 × 2 = 20 unique scenario combinations.

## Usage

### Running the Analysis

1. **Open the Jupyter notebook:**
   ```bash
   jupyter notebook NavWareSet_Quantitative_Analysis.ipynb
   ```

2. **Execute all cells** to:
   - Load all tracks from the `selected_tracks/` directory
   - Calculate metrics for each scenario combination
   - Generate results table
   - Export results to CSV

### Visualizing Individual Tracks

To plot detailed visualizations of robot-human interactions for a specific track:

```bash
python plot_all_tracks.py
```

This script:
- Auto-detects CSV format
- Plots robot trajectory (blue line)
- Plots human positions (red points or circles based on format)
- Shows robot and human relative motion
- Works with both CSV formats

### Interpreting Results

Results are saved to `NavWareSet_Quantitative_Analysis_Results.csv` with columns:
- `Scenario`: Navigation scenario name
- `Robot`: Robot type (HSR/Jackal)
- `Robot Behavior`: Compliant/Non-compliant
- `Vavg[1]`: Average velocity (m/s)
- `Aavg[1]`: Average acceleration (m/s²)
- `Javg[1]`: Average jerk (m/s³)
- `PLavg (avg) [1]`: Average path length (m)
- `PSC [2]`: Personal Space Compliance (%)
- `DHmin avg [3]`: Average minimal distance (m)

## Implementation Details

### Format Detection

All metric functions include automatic format detection:
```python
if 'column' in df.columns:
    # Format 1: Column-based (multiple rows per timestamp)
else:
    # Format 2: XY-pairs format
```

### Key Functions

- `global_average_speed(scene_list)`: Computes kinematic velocity
- `global_average_acceleration(scene_list)`: Time-weighted acceleration
- `global_average_jerk(scene_list)`: Rate of acceleration change
- `global_average_path_length(scene_list)`: Mean path length
- `global_average_personal_space_compliance(scene_list, threshold=0.5)`: Safety distance compliance
- `global_average_minimal_distance(scene_list)`: Closest approach distance

### Custom Thresholds

Modify the Personal Space Compliance threshold by editing the function call:
```python
# Default: 0.5m threshold
psc = global_average_personal_space_compliance(scene_list, threshold=0.5)

# Custom: 0.3m threshold
psc = global_average_personal_space_compliance(scene_list, threshold=0.3)
```

## Dependencies

- Python 3.8+
- pandas: Data manipulation and analysis
- numpy: Numerical computations
- pathlib: File path operations
- matplotlib: Visualization (for plotting script)

Install dependencies:
```bash
pip install pandas numpy matplotlib
```

## Files Description

| File | Purpose |
|------|---------|
| `NavWareSet_Quantitative_Analysis.ipynb` | Main analysis pipeline with all metric calculations |
| `plot_all_tracks.py` | Standalone visualization script for individual tracks |
| `NavWareSet_Quantitative_Analysis_Results.csv` | Generated results table (output) |
| `selected_tracks/` | Track data organized by scenario |

## Results Summary

The analysis processes **545 hand-selected robot tracks** across all scenario combinations and generates a **20-row results table** with 6 metrics each, enabling comparison of:
- Robot types (HSR vs Jackal)
- Navigation behaviors (Compliant vs Non-compliant)
- Scenario difficulty (kinematic vs distance-based metrics)
- Social awareness effectiveness (PSC metric)

## Notes

- Timestamps are in Unix nanoseconds; division by 1e9 converts to seconds
- PSC values >90% indicate strong social compliance; <50% indicates poor compliance
- Path lengths are cumulative distances; shorter paths indicate more efficient navigation
- All distances are in meters; all times are in seconds
- The framework automatically detects CSV format, ensuring robustness across dataset variations

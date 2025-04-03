import time
import subprocess
import math
 

# Global variables
current_yaw = 0.0
current_pitch = 0.0
sinkid = 0 

# Smoothed volume
smooth_left_volume = 0.5
smooth_right_volume = 0.5

# Execute the command
command = "wpctl status | grep -A 5 'Sinks:'"
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Display the output on the screen
if result.returncode == 0:
    print("Command output:\n", result.stdout)
else:
    print(f"Error executing the command: {result.stderr}")

sinkid = input("Introduce sink id ")

def update_audio_values(yaw, pitch):
    """Updates yaw and pitch values in the system."""
    global current_yaw, current_pitch
    current_yaw = yaw
    current_pitch = pitch

def get_current_audio_sink_id():
    """Returns the default audio sink ID."""
    return sinkid

def set_audio_sink_volume(sink_id, left_volume, right_volume):
    """Adjusts the left and right channel volumes in PipeWire."""
    try:
        command = f'pw-cli set-param {sink_id} Props {{"channelVolumes": [{left_volume:.6f}, {right_volume:.6f}]}}'
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass  # Ignore errors to prevent crashes

def smooth_transition(current_value, target_value, smoothing_factor=0.2):
    """Fast interpolation for more instantaneous changes."""
    return current_value + (target_value - current_value) * smoothing_factor

def change_audio_channels_based_on_head_movement():
    """Changes audio channels in real time based on head movement."""
    global smooth_left_volume, smooth_right_volume

    current_sink_id = get_current_audio_sink_id()

    while True:
        yaw = current_yaw

        # Map yaw from -45 to 45 degrees to a range of -1 to 1
        x_pos = max(-1, min(1, yaw / 45))

        # Compute volumes in a non-linear way for a more realistic effect
        target_left_volume = max(0.1, (1 - x_pos) / 2)
        target_right_volume = max(0.1, (1 + x_pos) / 2)

        # Fast smoothing
        smooth_left_volume = smooth_transition(smooth_left_volume, target_left_volume)
        smooth_right_volume = smooth_transition(smooth_right_volume, target_right_volume)

        # Apply rapid changes
        set_audio_sink_volume(current_sink_id, smooth_left_volume, smooth_right_volume)

        time.sleep(0.002)  # Low latency for near-instantaneous changes

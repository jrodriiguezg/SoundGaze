from track import facetracker
import threading
import time
import audio  # Import the audio.py module
import subprocess

# Global variables to store movement data
global_movimiento_yaw = "Center"
global_movimiento_pitch = "Center"
global_yaw = 0.0
global_pitch = 0.0
original_volume = None  # Variable to store the original volume

def get_current_volume():
    """
    Gets the current volume of the default audio sink.
    """
    try:
        result = subprocess.run(["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"], capture_output=True, text=True)
        if result.returncode == 0:
            volume_str = result.stdout.strip().split(" ")[1]  # Extract the volume value
            return float(volume_str)  # Return the volume as a float
    except Exception as e:
        print(f"Error retrieving volume: {e}")
    return 0.8  # Default value if the volume cannot be obtained

def set_volume(volume):
    """
    Restores the original volume.
    """
    try:
        subprocess.run(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", str(volume)], check=True)
        print(f"Volume restored to {volume}")
    except Exception as e:
        print(f"Error restoring volume: {e}")

def update_movement_variables(yaw, pitch, movimiento_yaw, movimiento_pitch):
    """
    Updates the global movement variables.
    """
    global global_movimiento_yaw
    global global_movimiento_pitch
    global global_yaw
    global global_pitch
    global_movimiento_yaw = movimiento_yaw
    global_movimiento_pitch = movimiento_pitch
    global_yaw = yaw
    global_pitch = pitch
    audio.update_audio_values(yaw, pitch)

def facetracker_wrapper():
    """
    Wraps the facetracker function to pass the callback function.
    """
    facetracker(update_movement_variables)

if __name__ == "__main__":
    # Save the original volume before starting
    original_volume = get_current_volume()

    # Start the facetracker in a separate thread
    tracker_thread = threading.Thread(target=facetracker_wrapper)
    tracker_thread.daemon = True  # Allows the thread to terminate when the main program ends
    tracker_thread.start()

    # Start the audio functions in a separate thread
    audio_thread = threading.Thread(target=audio.change_audio_channels_based_on_head_movement)
    audio_thread.daemon = True
    audio_thread.start()

    try:
        while True:
            # Access the global movement variables
            print(f"Main - Yaw: {global_yaw:.2f} degrees, Pitch: {global_pitch:.2f} degrees, Movement Yaw: {global_movimiento_yaw}, Movement Pitch: {global_movimiento_pitch}")
            time.sleep(0.5)  # Wait a bit before reading the variables again
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        print("Restoring original volume...")
        set_volume(original_volume)  # Restore the original volume

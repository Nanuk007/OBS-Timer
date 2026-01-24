import obspython as obs
import subprocess
import os
import sys
import requests
import threading

# Global variables
timer_process = None
script_dir = ""
server_running = False

# Description shown in OBS Scripts
def script_description():
    return """<h2>OBS Countdown Timer</h2>
    <p>This script manages a countdown timer with circular progress display.</p>
    <p><b>Controls:</b></p>
    <ul>
        <li>Start/Stop/Reset the timer</li>
        <li>Add or remove time</li>
        <li>Set custom time</li>
    </ul>
    <p><b>Usage:</b></p>
    <ol>
        <li>Click "Start Server" to launch the timer backend</li>
        <li>Add a Browser Source to your scene with URL: http://localhost:5000/?obs=true</li>
        <li>Use the controls below or your Stream Deck to control the timer</li>
    </ol>
    """

# Called when script is loaded
def script_load(settings):
    global script_dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    obs.script_log(obs.LOG_INFO, f"Timer script loaded from: {script_dir}")

# Called when script is unloaded
def script_unload():
    stop_server()

# Define script properties (UI controls)
def script_properties():
    props = obs.obs_properties_create()
    
    # Server control
    obs.obs_properties_add_button(props, "start_server", "🟢 Start Server", start_server_button)
    obs.obs_properties_add_button(props, "stop_server", "🔴 Stop Server", stop_server_button)
    obs.obs_properties_add_text(props, "status", "Status:", obs.OBS_TEXT_DEFAULT)
    
    # Timer controls
    obs.obs_properties_add_button(props, "timer_start", "▶ Start Timer", timer_start_button)
    obs.obs_properties_add_button(props, "timer_stop", "⏸ Stop Timer", timer_stop_button)
    obs.obs_properties_add_button(props, "timer_reset", "⏹ Reset Timer", timer_reset_button)
    
    # Time adjustment
    obs.obs_properties_add_int(props, "seconds_input", "Seconds:", 1, 3600, 1)
    obs.obs_properties_add_button(props, "add_time", "+ Add Time", add_time_button)
    obs.obs_properties_add_button(props, "remove_time", "- Remove Time", remove_time_button)
    obs.obs_properties_add_button(props, "set_time", "⏱ Set Time", set_time_button)
    
    return props

# Server management functions
def start_server_button(props, prop):
    start_server()
    return True

def stop_server_button(props, prop):
    stop_server()
    return True

def start_server():
    global timer_process, server_running, script_dir
    
    if server_running:
        obs.script_log(obs.LOG_WARNING, "Server is already running")
        return
    
    try:
        timer_py = os.path.join(script_dir, "timer.py")
        
        if not os.path.exists(timer_py):
            obs.script_log(obs.LOG_ERROR, f"timer.py not found at {timer_py}")
            return
        
        # Start the Flask server in background
        timer_process = subprocess.Popen(
            [sys.executable, timer_py],
            cwd=script_dir,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        server_running = True
        obs.script_log(obs.LOG_INFO, "Timer server started successfully")
        obs.script_log(obs.LOG_INFO, "Add Browser Source with URL: http://localhost:5000/?obs=true")
        
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"Failed to start server: {str(e)}")

def stop_server():
    global timer_process, server_running
    
    if timer_process:
        timer_process.terminate()
        timer_process = None
        server_running = False
        obs.script_log(obs.LOG_INFO, "Timer server stopped")

# Timer control functions
def api_request(endpoint, data=None):
    try:
        url = f"http://localhost:5000/api/{endpoint}"
        if data:
            response = requests.post(url, json=data, timeout=2)
        else:
            response = requests.post(url, timeout=2)
        
        if response.status_code == 200:
            obs.script_log(obs.LOG_INFO, f"Command sent: {endpoint}")
            return True
        else:
            obs.script_log(obs.LOG_WARNING, f"Command failed: {endpoint}")
            return False
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"Failed to send command: {str(e)}")
        return False

def timer_start_button(props, prop):
    api_request("start")
    return True

def timer_stop_button(props, prop):
    api_request("stop")
    return True

def timer_reset_button(props, prop):
    api_request("reset")
    return True

def add_time_button(props, prop):
    settings = obs.obs_properties_get_settings(props)
    seconds = obs.obs_data_get_int(settings, "seconds_input")
    api_request("add", {"seconds": seconds})
    obs.obs_data_release(settings)
    return True

def remove_time_button(props, prop):
    settings = obs.obs_properties_get_settings(props)
    seconds = obs.obs_data_get_int(settings, "seconds_input")
    api_request("remove", {"seconds": seconds})
    obs.obs_data_release(settings)
    return True

def set_time_button(props, prop):
    settings = obs.obs_properties_get_settings(props)
    seconds = obs.obs_data_get_int(settings, "seconds_input")
    api_request("set", {"seconds": seconds})
    obs.obs_data_release(settings)
    return True

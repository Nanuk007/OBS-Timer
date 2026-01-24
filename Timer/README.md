# OBS Timer with Bitfocus Companion Integration

A professional countdown timer with circular progress visualization for OBS, controllable via Bitfocus Companion on Stream Deck.

## Features

- ⏱️ **Countdown Timer** with hours:minutes:seconds display
- 🎨 **Circular Progress Ring** with color-coded status
- 🔴 **OBS Browser Source** ready (transparent background)
- 🎮 **Stream Deck Control** via Bitfocus Companion
- 🌐 **HTTP API** for remote control
- 🔄 **Real-time Updates** via WebSocket

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the timer server:
```bash
python timer.py
```

The server will start on `http://localhost:5000`

## OBS Setup

1. In OBS, add a **Browser Source**
2. Set URL to: `http://localhost:5000/?obs=true`
3. Set Width: **800** and Height: **600** (or adjust as needed)
4. ✅ Check "Shutdown source when not visible"
5. ✅ Check "Refresh browser when scene becomes active"

The `?obs=true` parameter hides the control buttons.

## Bitfocus Companion Setup

### HTTP Request Configuration

Create buttons in Companion with these HTTP requests:

#### Start Timer
- **Method:** POST
- **URL:** `http://localhost:5000/api/start`

#### Stop/Pause Timer
- **Method:** POST
- **URL:** `http://localhost:5000/api/stop`

#### Reset Timer
- **Method:** POST
- **URL:** `http://localhost:5000/api/reset`

#### Set Timer to 5 Minutes
- **Method:** POST
- **URL:** `http://localhost:5000/api/set`
- **Headers:** `Content-Type: application/json`
- **Body:** `{"minutes": 5}`

#### Add 1 Minute
- **Method:** POST
- **URL:** `http://localhost:5000/api/add`
- **Headers:** `Content-Type: application/json`
- **Body:** `{"seconds": 60}`

#### Remove 1 Minute
- **Method:** POST
- **URL:** `http://localhost:5000/api/remove`
- **Headers:** `Content-Type: application/json`
- **Body:** `{"seconds": 60}`

#### Set Custom Time
- **Method:** POST
- **URL:** `http://localhost:5000/api/set`
- **Headers:** `Content-Type: application/json`
- **Body:** `{"hours": 0, "minutes": 10, "seconds": 30}`

## API Reference

### Endpoints

All endpoints return JSON with status and timer information.

#### GET /api/status
Get current timer status
```json
{
  "remaining_seconds": 300,
  "total_seconds": 300,
  "initial_seconds": 300,
  "running": false,
  "time_display": "00:05:00",
  "progress": 100
}
```

#### POST /api/start
Start the timer

#### POST /api/stop
Stop/pause the timer

#### POST /api/reset
Reset timer to initial time

#### POST /api/set
Set timer duration
```json
// Option 1: Seconds
{"seconds": 300}

// Option 2: Minutes
{"minutes": 5}

// Option 3: Full time
{"hours": 1, "minutes": 30, "seconds": 0}
```

#### POST /api/add
Add time to timer
```json
{"seconds": 60}
```

#### POST /api/remove
Remove time from timer
```json
{"seconds": 30}
```

## Visual Indicators

The circular progress ring changes color based on remaining time:

- 🟢 **Green** (>50%): Plenty of time
- 🟡 **Orange** (20-50%): Time running low
- 🔴 **Red** (<20%): Almost finished

## Customization

### Change Initial Time
Edit `timer.py` line 207:
```python
timer.set_time(300)  # 300 seconds = 5 minutes
```

### Change Colors
Edit `templates/timer.html` in the gradient section (around line 180)

### Change Size
Modify the canvas size and container dimensions in the HTML

## Troubleshooting

**Timer not visible in OBS?**
- Make sure the server is running
- Check the URL is correct
- Try refreshing the browser source

**Companion buttons not working?**
- Verify the server is running on port 5000
- Check firewall settings
- Ensure Content-Type header is set for POST requests with body

**Timer jumps or skips?**
- This is normal WebSocket behavior
- The timer updates every second on the server

## Advanced Usage

### Running on Different Port
```python
socketio.run(app, host='0.0.0.0', port=8080, debug=False)
```

### Running on Network
The server binds to `0.0.0.0`, so it's accessible from other devices on your network.
Use your computer's IP address: `http://192.168.1.XXX:5000/`

## License

Free to use and modify for your streaming needs!

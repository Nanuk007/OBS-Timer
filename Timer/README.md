# OBS Timer with Stream Deck / Bitfocus Companion Integration

A production-ready countdown timer for **OBS Studio** with a circular canvas
progress ring, real-time WebSocket sync, and a full HTTP REST API designed for
**Bitfocus Companion** and **Stream Deck** control.

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![Socket.IO](https://img.shields.io/badge/Socket.IO-realtime-orange)

---

## Features

| Feature | Description |
|---------|-------------|
| ⏱ Countdown Timer | Accurate server-side countdown (no drift) |
| 🎨 Circular Progress Ring | HTML5 Canvas with color-coded status |
| 🟢🟡🔴 Status Colors | Green (running), Orange (≤ 10 s warning), Red (finished/paused) |
| 🔴 Finish Flash | Time display flashes red when timer reaches 00:00 |
| 🌐 Multi-Client Sync | All connected browsers update simultaneously via WebSocket |
| 🎮 Stream Deck Ready | HTTP REST API for Bitfocus Companion buttons |
| 📡 WebSocket API | Socket.IO commands for advanced integrations |
| 🖥 OBS Browser Source | Transparent background mode (`?transparent=true`) |
| ⌨ Keyboard Shortcuts | Space (start/stop), R (reset), ↑↓ (±10 s) |
| 🕐 Time Presets | 1, 2, 5, 10, 15 minute quick-set buttons |
| 🔄 Auto-Reconnect | WebSocket reconnects automatically on disconnect |
| 📐 Responsive | Fully responsive design — works at any size from mobile to 4K |

---

## Quick Start Guide

### 1. Install Dependencies

```bash
cd Timer
pip install -r requirements.txt
```

### 2. Launch the Server

**Option A: With Console Window**
```bash
python app.py
```

**Option B: Double-click** `start_timer.bat` (Windows)

**Option C: Silent Background** - Run `start_timer_silent.vbs` (Windows)

The server starts on **http://localhost:5000**.

### 3. Control the Timer

**Option A: Web Browser**
- Open `http://localhost:5000` in your browser
- Use buttons or keyboard shortcuts (Space=Start/Stop, R=Reset, ↑↓=Adjust)

**Option B: OBS + Stream Deck**
- Follow the detailed integration guides below

---

## OBS Studio Integration (Step-by-Step)

### Step 1: Start the Timer Server

1. Navigate to the `Timer` folder
2. Run **`start_timer.bat`** (or `python app.py`)
3. Wait for the message: `Running on http://127.0.0.1:5000`
4. **Leave this window open** while streaming/recording

> **Silent Mode:** Use `start_timer_silent.vbs` to run the server in the background without a console window.

### Step 2: Add Browser Source to OBS

1. Open **OBS Studio**
2. In your **Scene**, click the **+** button under **Sources**
3. Select **Browser**
4. Name it (e.g., "Countdown Timer") → Click **OK**

### Step 3: Configure Browser Source Properties

In the **Browser Source** properties window, configure:

| Setting | Value | Notes |
|---------|-------|-------|
| **URL** | `http://localhost:5000/?transparent=true` | The `?transparent=true` hides controls |
| **Width** | `400` | Recommended: 300-600 for overlay |
| **Height** | `400` | Same as width for perfect circle |
| **FPS** | `30` | Default is fine |
| **Custom CSS** | *(leave empty)* | Not needed |
| ☑ **Shutdown source when not visible** | **CHECKED** | Saves resources |
| ☑ **Refresh browser when scene becomes active** | **CHECKED** | Ensures fresh connection |
| ☐ Control audio via OBS | Unchecked | Timer has no audio |

4. Click **OK**

### Step 4: Position and Resize

1. In the OBS preview, **click and drag** the timer to position it
2. **Drag corners** to resize (hold Shift to maintain aspect ratio)
3. Right-click → **Transform** for precise positioning:
   - **Center to Screen** - Centers the timer
   - **Fit to Screen** - Full-screen countdown
   - **Stretch to Screen** - Fill entire canvas (not recommended)

### Step 5: Test the Timer

1. Open a **web browser** and go to `http://localhost:5000` (without `?transparent=true`)
2. Click **"Set Time"** → Enter `01:00` → Click OK
3. Click **"▶ Start"**
4. **Check OBS preview** — the timer should count down in real-time
5. Click **"⏸ Stop"** to pause, **"⏹ Reset"** to clear

> **The OBS overlay shows only the timer ring and digits.** Control it using the browser window or Stream Deck (see below).

### Common OBS Configurations

#### Small Corner Overlay (Lower-Right)
- **Size:** 300×300
- **Position:** Align to bottom-right corner
- Use for minimalist countdown in corner of stream

#### Large Center Timer (Full Attention)
- **Size:** 800×800 or 1920×1080
- **Position:** Centered on canvas
- Use for "Starting Soon" screens or intermission countdowns

#### Thin Bar Timer (Top of Screen)
- **Size:** 1920×200
- **Position:** Top center
- Timer automatically adjusts to fit width

---

## Bitfocus Companion Integration (Stream Deck Control)

### Prerequisites

1. **Bitfocus Companion** installed and running
   - Download from: https://bitfocus.io/companion
2. **OBS Timer Server** running (`start_timer.bat`)
3. **Stream Deck** connected (or using web buttons interface)

### Step 1: Add Generic HTTP Connection

1. Open **Companion** web interface (`http://localhost:8000`)
2. Go to the **Connections** tab (left sidebar)
3. Click **"+ Add Connection"**
4. Search for **"Generic HTTP"** (or scroll to find it)
5. Click **"Generic HTTP"** to add it
6. **Label it:** `OBS Timer` (optional)
7. Click **"Save"**

### Step 2: Configure Stream Deck Buttons

#### Button 1: START TIMER

1. In Companion, click on a **Stream Deck button slot**
2. Under **"Button Actions"**, click **"+ Add action"**
3. Select **Connection:** `Generic HTTP` (or your label)
4. Select **Action:** `Generic: HTTP Request`
5. Configure:

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/start` |
| **Method** | `POST` |
| **Headers** | *(leave empty)* |
| **Body** | *(leave empty)* |

6. Under **"Button Styling"**:
   - **Text:** `START`
   - **Background Color:** Green (`#00FF00`)
   - **Text Color:** Black (`#000000`)
7. Click **"Save"**

#### Button 2: STOP TIMER

1. Click another **button slot**
2. Add action → **Generic HTTP: HTTP Request**
3. Configure:

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/stop` |
| **Method** | `POST` |

4. Styling:
   - **Text:** `STOP`
   - **Background:** Orange (`#FF9800`)
5. **Save**

#### Button 3: RESET TIMER

1. Add action → **Generic HTTP: HTTP Request**
2. Configure:

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/reset` |
| **Method** | `POST` |

3. Styling:
   - **Text:** `RESET`
   - **Background:** Red (`#FF0000`)
4. **Save**

#### Button 4: SET 1 MINUTE

1. Add action → **Generic HTTP: HTTP Request**
2. Configure:

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/set?minutes=1&seconds=0` |
| **Method** | `POST` |

3. Styling:
   - **Text:** `1 MIN`
   - **Background:** Blue (`#2196F3`)
4. **Save**

#### Button 5: SET 5 MINUTES

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/set?minutes=5&seconds=0` |
| **Method** | `POST` |
| **Text** | `5 MIN` |
| **Background** | Blue |

#### Button 6: SET 10 MINUTES

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/set?minutes=10&seconds=0` |
| **Method** | `POST` |
| **Text** | `10 MIN` |
| **Background** | Blue |

#### Button 7: ADD 10 SECONDS

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/add?seconds=10` |
| **Method** | `POST` |
| **Text** | `+10s` |
| **Background** | Green |

#### Button 8: SUBTRACT 10 SECONDS

| Field | Value |
|-------|-------|
| **URL** | `http://localhost:5000/api/timer/subtract?seconds=10` |
| **Method** | `POST` |
| **Text** | `-10s` |
| **Background** | Orange |

### Step 3: Test Your Buttons

1. Make sure **OBS Timer server is running**
2. Press **"1 MIN"** button on Stream Deck
3. Check OBS preview — timer should show `01:00`
4. Press **"START"** button
5. Timer should begin counting down
6. Press **"STOP"** to pause
7. Press **"RESET"** to zero

### Recommended Stream Deck Layout

```
Page 1: OBS Timer Control
┌──────────┬──────────┬──────────┬──────────┐
│  1 MIN   │  2 MIN   │  5 MIN   │  10 MIN  │  ← Preset times
├──────────┼──────────┼──────────┼──────────┤
│  START   │   STOP   │  RESET   │  +1 MIN  │  ← Main controls
├──────────┼──────────┼──────────┼──────────┤
│  +10 s   │  -10 s   │  +30 s   │  -30 s   │  ← Fine adjustments
└──────────┴──────────┴──────────┴──────────┘
```

### Advanced: Add Button Feedback (Optional)

To show the current timer value on your Stream Deck button:

1. Add a **second Generic HTTP** action to the button (feedback request)
2. Configure:
   - **URL:** `http://localhost:5000/api/timer/status`
   - **Method:** `GET`
3. Add **Feedback** using the response (requires Companion 3.0+)
4. Set update interval to 1 second

> **Note:** This is advanced — the basic setup above works perfectly without feedback.

### Troubleshooting Companion Connection

| Problem | Solution |
|---------|----------|
| **"Connection failed"** | Ensure timer server is running (`start_timer.bat`) |
| **Buttons don't work** | Check URL is `http://localhost:5000` (not `https://`) |
| **Firewall blocking** | Add exception for Python or disable firewall temporarily |
| **Wrong port** | Verify server shows "Running on http://127.0.0.1:5000" |
| **Timer not updating in OBS** | Refresh the OBS Browser Source |

---

## Complete Workflow Example

### Scenario: "Starting Soon" Stream Countdown

1. **Before stream:**
   - Start timer server (`start_timer.bat`)
   - Ensure OBS Browser Source is added to "Starting Soon" scene

2. **5 minutes before going live:**
   - Press **"5 MIN"** on Stream Deck
   - Switch to "Starting Soon" scene in OBS
   - Press **"START"** on Stream Deck

3. **Timer counts down 5:00 → 0:00**
   - Timer turns orange at 10 seconds
   - Timer flashes red at 0:00

4. **When timer hits 0:00:**
   - Switch to main stream scene
   - Begin stream content

5. **Between segments (optional):**
   - Press **"2 MIN"** for break timer
   - Press **"START"**
   - Display "Back in 2 minutes" scene

6. **End of stream:**
   - Press **"RESET"** to clear timer
   - Close server window (or leave running for next stream)

---

## Control Methods Overview

### Web Browser UI

Open **http://localhost:5000** for the full control interface with:

- **6 Control Buttons:** Start, Stop, Reset, +10s, -10s, Set Time
- **5 Preset Buttons:** 1, 2, 5, 10, 15 minutes
- **Keyboard Shortcuts:**

| Key | Action |
|-----|--------|
| `Space` | Start / Stop (toggle) |
| `R` | Reset to 00:00 |
| `↑` | Add 10 seconds |
| `↓` | Subtract 10 seconds |

### Stream Deck / Bitfocus Companion

Control remotely via HTTP API (see detailed guide above). Example buttons:

- **START:** `POST http://localhost:5000/api/timer/start`
- **STOP:** `POST http://localhost:5000/api/timer/stop`  
- **RESET:** `POST http://localhost:5000/api/timer/reset`
- **SET 5 MIN:** `POST http://localhost:5000/api/timer/set?minutes=5&seconds=0`

### Custom Scripts / Automation

Use any HTTP client (curl, Postman, Python requests, etc.):

```bash
# Set timer to 3 minutes
curl -X POST "http://localhost:5000/api/timer/set?minutes=3&seconds=0"

# Start countdown
curl -X POST "http://localhost:5000/api/timer/start"

# Check status
curl "http://localhost:5000/api/timer/status"
```

---

## HTTP REST API - Quick Reference

All endpoints return JSON: `{"success": true, "status": "RUNNING", "display": "05:00", ...}`

### Control Endpoints (All POST)
### Control Endpoints (All POST)

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/api/timer/start` | Start/resume timer | `POST http://localhost:5000/api/timer/start` |
| `/api/timer/stop` | Pause timer | `POST http://localhost:5000/api/timer/stop` |
| `/api/timer/reset` | Reset to 00:00 | `POST http://localhost:5000/api/timer/reset` |
| `/api/timer/set` | Set time | `POST http://localhost:5000/api/timer/set?minutes=5&seconds=30` |
| `/api/timer/add` | Add seconds | `POST http://localhost:5000/api/timer/add?seconds=10` |
| `/api/timer/subtract` | Remove seconds | `POST http://localhost:5000/api/timer/subtract?seconds=10` |

### Status Endpoint (GET)

```bash
GET http://localhost:5000/api/timer/status
```

**Response:**
```json
{
  "success": true,
  "status": "RUNNING",
  "remainingSeconds": 125,
  "initialSeconds": 300,
  "display": "02:05",
  "progress": 41.67
}
```

---

## WebSocket API (Socket.IO)

For real-time bidirectional communication:

```javascript
const socket = io("http://localhost:5000");

// Send commands
socket.emit("command", { action: "start" });
socket.emit("command", { action: "stop" });
socket.emit("command", { action: "reset" });
socket.emit("command", { action: "addTime", seconds: 10 });
socket.emit("command", { action: "subtractTime", seconds: 10 });
socket.emit("command", { action: "setTime", minutes: 5, seconds: 30 });

// Receive real-time updates
socket.on("timer_update", (data) => {
    console.log(data);
    // { status: "RUNNING", display: "04:55", remainingSeconds: 295, ... }
});
```

### Events Reference

**Client → Server:**
- `command` - Send timer commands (see examples above)

**Server → Client:**
- `timer_update` - Broadcast state (every second while running, on any change)
- `error` - Error message
- `command_ok` - Command acknowledgement

---

## Visual Status Indicators

| Timer State | Ring Color | Status Text | Display |
|-------------|-----------|-------------|---------|
| **Running** (> 10s) | 🟢 Green | "RUNNING" (green) | White digits |
| **Running** (≤ 10s) | 🟡 Orange | "RUNNING" (orange) | Orange digits (warning) |
| **Paused** | ⚪ White | "PAUSED" (red) | White digits |
| **Finished** (00:00) | 🔴 Red | "FINISHED" (red) | Red flashing digits |

---

## Advanced Configuration

### Change Server Port

Edit the last line of `app.py`:

```python
socketio.run(app, host="0.0.0.0", port=8080, debug=False, allow_unsafe_werkzeug=True)
```

Then update OBS Browser Source URL to `http://localhost:8080/?transparent=true`

### Network Access (Control from Another Device)

The server binds to `0.0.0.0` (all network interfaces), so any device on your network can access it:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. On another device, use:
   - Control UI: `http://192.168.1.100:5000`
   - API calls: `http://192.168.1.100:5000/api/timer/start`

### Customize Colors

Edit CSS variables in `static/style.css`:

```css
:root {
    --color-running:  #4caf50;  /* Green (timer active) */
    --color-warning:  #ff9800;  /* Orange (≤10 seconds) */
    --color-finished: #f44336;  /* Red (finished/paused) */
    --color-bg:       #0e1117;  /* Dark background */
}
```

### Enable HTTPS (Optional)

For secure connections (required for some browsers):

1. Place your SSL certificate files in `certs/`:
   - `cert.pem` (certificate)
   - `key.pem` (private key)

2. Modify `app.py` to use SSL:
   ```python
   socketio.run(app, 
       host="0.0.0.0", 
       port=5000, 
       ssl_context=('certs/cert.pem', 'certs/key.pem')
   )
   ```

3. Update URLs to use `https://localhost:5000`

---

## Troubleshooting

### OBS Issues

| Problem | Solution |
|---------|----------|
| Timer not visible in OBS | 1. Verify server is running (`start_timer.bat`)<br>2. Right-click Browser Source → "Refresh"<br>3. Check URL is correct with `?transparent=true` |
| Timer shows controls/buttons | Add `?transparent=true` to the URL parameter |
| Timer is stretched/distorted | Use equal width and height (e.g., 400×400)<br>Hold Shift while resizing in OBS |
| Black screen in OBS | 1. Check server console for errors<br>2. Test URL in a regular browser first<br>3. Disable hardware acceleration in OBS settings |
| Timer not updating | 1. Refresh Browser Source<br>2. Check "Refresh when scene becomes active"<br>3. Restart OBS |

### Companion / Stream Deck Issues

| Problem | Solution |
|---------|----------|
| Buttons don't respond | 1. Ensure server is running<br>2. Verify URL is `http://localhost:5000` (not https)<br>3. Check Companion connection status (should be green) |
| "Connection Failed" error | 1. Confirm timer server shows "Running on http://127.0.0.1:5000"<br>2. Test URL in browser first: `http://localhost:5000/api/timer/status`<br>3. Check Windows Firewall isn't blocking port 5000 |
| Buttons work but timer doesn't update | 1. Check OBS Browser Source is in active scene<br>2. Refresh the Browser Source<br>3. Open `http://localhost:5000` in browser to verify timer updates there |
| Wrong method (GET/POST) | All control endpoints use **POST**<br>Only `/api/timer/status` uses GET |

### Server Issues

| Problem | Solution |
|---------|----------|
| "Port 5000 already in use" | 1. Close other applications using port 5000<br>2. Kill existing timer processes<br>3. Change port in `app.py` (see Advanced Configuration) |
| Server crashes on start | 1. Install dependencies: `pip install -r requirements.txt`<br>2. Check Python version (3.8+ required)<br>3. Check console for specific error messages |
| Timer drift/inaccurate | Timer uses `time.monotonic()` — no drift should occur<br>Report as bug if drift exceeds 1 second over 10 minutes |
| High CPU usage | Normal: ~1-2% when idle, ~5-10% when running<br>If higher, restart the server |

### Network/Firewall Issues

| Problem | Solution |
|---------|----------|
| Can't access from other devices | 1. Check firewall allows inbound on port 5000<br>2. Verify both devices on same network<br>3. Use computer's IP, not `localhost` |
| WebSocket disconnects frequently | 1. Check network stability<br>2. Client auto-reconnects — should recover<br>3. Fallback to HTTP polling if Socket.IO unavailable |

### Browser Issues

| Problem | Solution |
|---------|----------|
| Controls not clickable | 1. Clear browser cache<br>2. Try different browser<br>3. Check browser console (F12) for JavaScript errors |
| Canvas not rendering | 1. Ensure browser supports HTML5 Canvas<br>2. Update browser to latest version<br>3. Disable browser extensions that might block canvas |
| Socket.IO errors in console | Timer automatically falls back to HTTP polling<br>Functionality will work, just without real-time WebSocket updates |

---

## API Complete Reference

### HTTP Endpoints

| Method | Endpoint | Parameters | Description | Response |
|--------|----------|------------|-------------|----------|
| `POST` | `/api/timer/start` | — | Start/resume countdown | Timer state JSON |
| `POST` | `/api/timer/stop` | — | Pause countdown | Timer state JSON |
| `POST` | `/api/timer/reset` | — | Reset to 00:00 | Timer state JSON |
| `POST` | `/api/timer/add` | `?seconds=N` | Add N seconds (default: 10) | Timer state JSON |
| `POST` | `/api/timer/subtract` | `?seconds=N` | Remove N seconds (default: 10) | Timer state JSON |
| `POST` | `/api/timer/set` | `?minutes=M&seconds=S` | Set specific time | Timer state JSON |
| `GET`  | `/api/timer/status` | — | Get current state | Timer state JSON |

### Response Format (All Endpoints)

```json
{
  "success": true,
  "status": "RUNNING",           // RUNNING | PAUSED | FINISHED
  "remainingSeconds": 180,       // Time left (integer)
  "initialSeconds": 300,         // Original countdown value
  "display": "03:00",            // Formatted MM:SS
  "progress": 60.0               // Percentage remaining (0-100)
}
```

### Legacy Endpoints (Backward Compatible)

| Method | Endpoint | Body (JSON) | Notes |
|--------|----------|-------------|-------|
| `POST` | `/api/start` | — | Same as `/api/timer/start` |
| `POST` | `/api/stop` | — | Same as `/api/timer/stop` |
| `POST` | `/api/reset` | — | Same as `/api/timer/reset` |
| `POST` | `/api/set` | `{"minutes": 5}` or `{"seconds": 300}` | Old format |
| `POST` | `/api/add` | `{"seconds": 60}` | Old format |
| `POST` | `/api/remove` | `{"seconds": 60}` | Same as subtract |
| `GET`  | `/api/status` | — | Same as `/api/timer/status` |

---

## File Structure

```
Timer/
├── app.py                     # Main Flask server + Socket.IO + TimerEngine
├── requirements.txt           # Python dependencies (Flask, Socket.IO)
├── README.md                  # This file (complete documentation)
│
├── start_timer.bat            # Windows launcher (shows console)
├── start_timer_silent.vbs     # Windows launcher (background, no window)
│
├── certs/                     # SSL certificates (optional for HTTPS)
│   ├── cert.pem
│   └── key.pem
│
├── templates/
│   └── index.html             # Main timer page (HTML structure)
│
└── static/
    ├── style.css              # Timer styling, colors, responsive design
    └── timer.js               # Client-side logic, WebSocket, Canvas rendering
```

---

## Features Summary

✅ **Accurate Countdown** - Server-side timing with monotonic clock (no drift)  
✅ **Multi-Client Sync** - WebSocket broadcasts keep all viewers synchronized  
✅ **Dual Control** - Web UI with keyboard shortcuts + HTTP API for Stream Deck  
✅ **Visual Feedback** - Circular progress ring with color-coded status  
✅ **OBS Ready** - Transparent overlay mode, fully responsive sizing  
✅ **Resilient** - Auto-reconnect WebSocket, HTTP polling fallback  
✅ **Cross-Platform** - Works on Windows, Mac, Linux  
✅ **Network Control** - Control from any device on your network  
✅ **Zero Drift** - Wall-clock delta calculations prevent time drift  
✅ **Maximum Time** - Up to 99 minutes 59 seconds (5999 seconds)  

---

## Use Cases

- 🎥 **Live Streaming** - "Starting Soon" countdowns, break timers, segment limits
- 📹 **Recording** - Time limits for takes, Q&A sessions
- 🎤 **Presentations** - Speaker time limits with visual warnings
- 🎮 **Gaming** - Speedrun timers, challenge countdowns
- 🎪 **Events** - Scheduled countdown displays
- 📺 **Production** - Synchronized timing across multiple displays

---

## Support & Contributing

**Issues?** Check the Troubleshooting section above.

**Feature Requests?** The timer is designed to be minimal and focused — fork and customize for your needs!

**License:** Free to use and modify. No warranty provided.

---

## Version History

- **v3.0** - Complete rewrite with Socket.IO, circular canvas timer, dual API
- **v2.0** - Added Stream Deck support, HTTP API
- **v1.0** - Initial release with basic countdown

---

*Built for OBS Studio streamers and producers who need reliable, professional countdown timers.*

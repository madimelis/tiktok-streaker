# TikTok Streak Saver

A small Python script that keeps a TikTok streak alive by automatically sending a message to a chosen friend. It uses Selenium to control Firefox with your existing, already logged-in browser profile, so no password or API access is needed.

## How it works

1. Launches Firefox using your saved profile (so you are already logged in to TikTok).
2. Opens the TikTok messages page and waits for the chat list to load.
3. Searches the chat list for your friend's nickname and opens that chat.
4. Types a message into the input field and sends it.
5. Closes the browser.

## Requirements

- Python 3.8 or newer
- Mozilla Firefox
- A Firefox profile that is already logged in to TikTok
- Python packages: `selenium` and `webdriver-manager`

GeckoDriver is downloaded automatically by `webdriver-manager` on the first run.

## Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install selenium webdriver-manager
```

## Configuration

Open `tscript.py` and edit two values inside `send_tiktok_streak()`:

| Variable       | Description                                                    |
|----------------|----------------------------------------------------------------|
| `profile_path` | Full path to the Firefox profile that is logged in to TikTok.  |
| `friend_name`  | The nickname of your friend exactly as shown in the chat list. |

### Finding your Firefox profile path

1. Open Firefox and go to `about:profiles`.
2. Find the profile you use for TikTok.
3. Copy the path shown next to **Root Directory**.

Tip: use a dedicated Firefox profile for this script and log in to TikTok in it once manually. Do not use a profile that is currently open in another Firefox window, because Firefox locks a profile while it is running.

## Usage

```bash
python tscript.py
```

Console output will tell you which step the script is on and whether the message was sent successfully.

## Running automatically

To keep the streak alive every day, run the script on a schedule.

**Windows (Task Scheduler):** create a daily task that runs `python C:\path\to\tscript.py`.

**Linux / macOS (cron):**

```bash
0 12 * * * /usr/bin/python3 /path/to/tscript.py
```

The computer must be on and able to open a browser window at the scheduled time.

## Troubleshooting

- **Chat not found:** check that `friend_name` matches the displayed nickname exactly, including capitalization and spacing. Increase the initial wait time if your connection is slow.
- **Message input not found:** TikTok changes its page layout from time to time. Update the CSS selector used to locate the input field.
- **Profile in use error:** close all Firefox windows that use the same profile and try again.
- **Not logged in:** open Firefox with that profile manually and sign in to TikTok, then rerun the script.

## Limitations

- The script depends on TikTok's current web layout, so it may break when TikTok updates its site.
- Waiting times are fixed delays, not smart waits, so very slow connections may need larger values.
- It sends a single message to a single friend.

## Disclaimer

This project is for personal and educational use. Automating actions on TikTok may violate its Terms of Service, and your account could be restricted as a result. Use it at your own risk. The author is not affiliated with TikTok or ByteDance.


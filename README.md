# TikTok Streak Saver

A Python script that keeps a TikTok streak alive by automatically sending a message to a chosen friend. It uses Selenium to control Firefox with your existing, already logged-in browser profile, so no password or API access is needed.

By default it runs in headless mode (no visible browser window), skips the run if a message was already sent today, retries on failure, and keeps a log.

## Features

- Headless mode: runs in the background without opening a window.
- Smart waits: continues as soon as the page is ready instead of using long fixed delays.
- Exact chat matching: finds the chat by its full name, so short or unusual names (even a single character) work correctly.
- Once-per-day protection: remembers the date of the last successful send, so the script can safely be scheduled several times a day.
- Automatic retries: up to 3 attempts if something fails.
- Logging and debugging: writes a log file and saves a screenshot when an error occurs.

## Requirements

- Python 3.8 or newer
- Mozilla Firefox
- A Firefox profile that is already logged in to TikTok
- Python packages listed in `requirements.txt` (`selenium` and `webdriver-manager`)

GeckoDriver is downloaded automatically by `webdriver-manager` on the first run.

## Installation

```bash
git clone https://github.com/madimelis/tiktok-streaker.git
cd <tiktok-streaker>
pip install -r requirements.txt
```

## Configuration

All settings are at the top of `tscript.py`:

| Setting        | Description                                                              |
|----------------|--------------------------------------------------------------------------|
| `PROFILE_PATH` | Full path to the Firefox profile that is logged in to TikTok. Do not end the path with a backslash. |
| `FRIEND_NAME`  | The username of your friend exactly as shown in the chat list.           |
| `MESSAGE`      | The text to send. The default is a single emoji.                         |
| `HEADLESS`     | `True` runs without a visible window. Set to `False` to watch it work.   |
| `WAIT_TIMEOUT` | Maximum seconds to wait for each page element (default 30).              |
| `MAX_RETRIES`  | Number of attempts before giving up (default 3).                         |

### Finding your Firefox profile path

1. Open Firefox and go to `about:profiles`.
2. Find the profile you use for TikTok.
3. Copy the path shown next to **Root Directory**.

Tip: use a dedicated Firefox profile for this script and log in to TikTok in it once manually. Close any Firefox window that uses the same profile before running the script, because Firefox locks a profile while it is open.

## Usage

```bash
python tscript.py
```

For the first run, set `HEADLESS = False` so you can confirm that the correct chat opens and the message is sent. Once it works, switch back to `True`.

## Files created by the script

| File            | Purpose                                                  |
|-----------------|----------------------------------------------------------|
| `last_sent.txt` | Date of the last successful send, used to avoid duplicates. |
| `streak.log`    | Log of every run, including errors.                      |
| `error.png`     | Screenshot of the browser from the most recent failure.  |

To force a resend on the same day, delete `last_sent.txt`.

## Scheduling

Because the script skips days it has already handled, schedule it to run several times a day (for example at login, at noon and in the evening). If the computer was off at one time, a later run will catch up.

**Windows (Task Scheduler):**

- Create a task that runs `python C:\path\to\tscript.py`.
- Add triggers for daily times and for "At log on".
- Enable "Run task as soon as possible after a scheduled start is missed".
- Optionally enable "Wake the computer to run this task".

**Linux / macOS (cron):**

```bash
0 12,18 * * * /usr/bin/python3 /path/to/tscript.py
```

On Linux, `anacron` or a systemd timer with `Persistent=true` can also catch up after the machine was off.

For the most reliable result, run the script on a device that stays on, such as a mini PC or Raspberry Pi.

## Troubleshooting

- **Chat not found or timeout:** check that `FRIEND_NAME` matches the displayed nickname exactly, including capitalization and spacing. Look at `streak.log` and `error.png` for details.
- **Works with a window but not headless:** set `HEADLESS = False`. TikTok may behave differently in headless mode.
- **Message input not found:** TikTok changes its page layout from time to time. Update the CSS selector used to locate the input field in `tscript.py`.
- **Profile in use error:** close all Firefox windows that use the same profile and try again.
- **Not logged in:** open Firefox with that profile manually, sign in to TikTok, and rerun the script.
- **Syntax errors in an editor:** make sure `PROFILE_PATH` does not end with a backslash, since that escapes the closing quote.

## Limitations

- The script depends on TikTok's current web layout, so it may break when TikTok updates its site.
- It sends a single message to a single friend.
- The computer must be on and able to launch Firefox when the script runs.

## Disclaimer

This project is for personal and educational use. Automating actions on TikTok may violate its Terms of Service, and your account could be restricted as a result. Use it at your own risk. The author is not affiliated with TikTok or ByteDance.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

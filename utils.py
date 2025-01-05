import datetime
import time
import sys

def log_message(level, message):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if level == "INFO":
        print(f'\033[90m{now}\033[0m \033[1;94mINFO\033[0m     {message}')
    elif level == "WARNING":
        print(f'\033[90m{now}\033[0m \033[1;93mWARNING\033[0m  {message}')
    elif level == "ERROR":
        print(f'\033[90m{now}\033[0m \033[1;91mERROR\033[0m    {message}')
    elif level == "SUCCESS":
        print(f'\033[90m{now}\033[0m \033[1;92mSUCCESS\033[0m  {message}')

def animate_loading(message, duration=5):
    animation = [
        "⠋",
        "⠙",
        "⠹",
        "⠸",
        "⠼",
        "⠴",
        "⠦",
        "⠧",
        "⠇",
        "⠏"
    ]
    end_time = time.time() + duration
    idx = 0
    interval = 0.1

    while time.time() < end_time:
        sys.stdout.write(f"\r{animation[idx % len(animation)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(interval)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
    log_message("SUCCESS", f"{message}")
    sys.stdout.flush()
    time.sleep(2)  # Wait for 2 seconds
    sys.stdout.write("\r" + " " * 22 + "\r")  # Clear the success message
    sys.stdout.flush()

async def log_to_channel(bot, embed):
    """Helper function to send logs to a specific channel."""
    log_channel_id = int(bot.log_channel_id)  # Set your log channel ID here
    log_channel = bot.get_channel(log_channel_id)
    if not log_channel.permissions_for(log_channel.guild.me).send_messages:
        log_message("ERROR", "Bot doesn't have permissions to send messages in the log channel.")
        return
    await log_channel.send(embed=embed)
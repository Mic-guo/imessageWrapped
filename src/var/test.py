import sqlite3
from datetime import datetime, timezone, timedelta

def get_all_texts():
    """GET all texts by contacts."""
    con = sqlite3.connect(str('chat.db'))
    cur = con.cursor()

    res = cur.execute(
        "SELECT date, id, text "
        "FROM message "
        "LEFT JOIN handle "
        "ON message.handle_id = handle.ROWID "
        "ORDER BY date DESC"
        )
    time, contact, text = res.fetchone()
    print(time, contact, text)
    timestamp_seconds = time / 1e9  # Convert nanoseconds to seconds

    # Assuming the epoch is in January 1, 2001
    epoch_datetime = datetime(2001, 1, 1, tzinfo=timezone.utc)

    # Convert to local time
    local_datetime = epoch_datetime + timedelta(seconds=timestamp_seconds)
    local_datetime = local_datetime.astimezone()  # Convert to local timezone

    formatted_datetime = local_datetime.strftime("%B %d, %Y %H:%M:%S")

    print(formatted_datetime)

    cur.close()
    con.close()

get_all_texts()

# Most Contacted Person:

# Identify the contact with whom you exchanged the most messages during the year.
# Total Messages Sent/Received:

# Provide an overall count of the total number of messages you sent and received throughout the year.
# Average Response Time:

# Calculate the average time it took for you to respond to messages.
# Most Active Day/Time:

# Determine the day and time when you were most active in terms of sending and receiving messages.
# Favorite Emojis:

# Display the emojis you used the most frequently in your messages.
# Word Count:

# Calculate the total word count of all your messages or identify the longest message you sent.
# Sentiment Analysis:

# Analyze the sentiment of your messages to see if they were generally positive, negative, or neutral.
# Most Shared Media:

# Highlight the type of media (images, videos, etc.) that you shared the most.
# Top Keywords:

# Identify the most frequently used words or keywords in your messages.
# Messaging Patterns:

# Analyze your messaging patterns, such as the times you're most active, the length of your messages, and the types of content you share.
# New Contacts:

# Identify any new contacts you started messaging during the year.
# Conversation Topics:

# Categorize messages based on topics to see which topics were most frequently discussed.
# Late-Night Conversations:

# Identify messages sent or received during late-night hours to see if there are any patterns.
# Sticker and GIF Usage:

# Highlight the most frequently used stickers and GIFs in your messages.
# Longest Thread:

# Identify the conversation with the highest number of messages or the longest continuous thread.
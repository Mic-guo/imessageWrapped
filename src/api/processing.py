"""REST API for imessage data."""

import flask
import src
from datetime import datetime, timezone, timedelta


def get_all_texts():
    """GET all texts by contacts."""
    # timestamp_seconds = time / 1e9  # Convert nanoseconds to seconds

    # # Assuming the epoch is in January 1, 2001
    # epoch_datetime = datetime(2001, 1, 1, tzinfo=timezone.utc)

    # # Convert to local time
    # local_datetime = epoch_datetime + timedelta(seconds=timestamp_seconds)

    # print(local_datetime)
    pass
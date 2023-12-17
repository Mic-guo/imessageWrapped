import sqlite3
from datetime import datetime, timezone, timedelta

import sqlite3
from datetime import datetime, timezone, timedelta
import struct
import plistlib
import biplist

STREAMER_VERSION_CURRENT = 4

TAG_INTEGER_2 = -127
TAG_INTEGER_4 = -126
TAG_FLOATING_POINT = -125

FIRST_TAG = -128
LAST_TAG  = -111

SIGNATURE_LENGTH = len("typedstring")

SIGNATURE_TO_BYTE_ORDER_MAP = {
    'typedstream': "BE",
    'streamtyped': "LE"
}

def inTagRange(n: int) -> bool:
    if n is None:
        return False
    return n >= FIRST_TAG and n <= LAST_TAG


class TypedStreamReader:
    def __init__(self, blob) -> None:
        self.data = blob

    def readData(self):
        streamerVersion = self.readInteger(False)
        signatureLength = self.readInteger(False)

        if streamerVersion != streamerVersion:
            print(f"Invalid streamer version: {streamerVersion}")
            exit(1)

        if signatureLength != SIGNATURE_LENGTH:
            print(f"The signature string must be exactly {SIGNATURE_LENGTH} bytes long, not {signatureLength}")

        signature = self.readExact(signatureLength)
        self.byteOrder = SIGNATURE_TO_BYTE_ORDER_MAP[signature]

        self.systemVersion = self.readInteger(False)
        self.readAllValues()


    def readAllValues(self):
        pass


    def readInteger(self, signed: bool, head: int = None):
        head = self.readHeadByte(head)
        if not inTagRange(head):
            return head if signed else head & 0xff

        format_str = '<' if self.byteOrder == 'LE' else '>'

        if head == TAG_INTEGER_2:
            format_str += 'h' if signed else 'H'
            return struct.unpack(format_str, self.readExact(2))[0]
        elif head == TAG_INTEGER_4:
            format_str += 'i' if signed else 'I'
            return struct.unpack(format_str, self.readExact(4))[0]
        else:
            print(f"Invalid head tag in this context: {head} ({head & 0xff})")
            exit(1)


    def readExact(self, byteCount: int):
        res = self.data[self.pos : self.pos + byteCount]
        self.pos += byteCount
        return res



    def readHeadByte(self, head: int):
        if head is None:
            head = int.from_bytes(self.readExact(1), byteorder="little", signed=True)
        return head


    def readFloat(self, head: float = None):
        head = self.readHeadByte(head)
        if head == TAG_FLOATING_POINT:
            format_str = '<f' if self.byteOrder == 'LE' else '>f'  # 'f' for 4-byte float
            return struct.unpack(format_str, self.readExact(4))[0]
        else:
            return self.readInteger(True, head)


    def readDouble(self, head: float = None):
        head = self.readHeadByte(head)
        


class TextMessages:

    def __init__(self):
        self.path_for_adb = "AddressBook-v22.abcddb"
        self.chat_db = "chat.db"
        self.pos = 0
    
    def get_text_messages(self):
        with sqlite3.connect(self.chat_db) as con:
            con.execute(f"ATTACH DATABASE '{self.path_for_adb}' AS adb;")

            query = """
                    SELECT date, id, ZFIRSTNAME || ' ' || ZLASTNAME AS full_name, text, attributedBody
                    FROM message
                    LEFT JOIN handle ON message.handle_id = handle.ROWID
                    LEFT JOIN adb.ZABCDPHONENUMBER ON REPLACE(handle.id, ' ', '') LIKE '%' || SUBSTR(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(ZABCDPHONENUMBER.ZFULLNUMBER, ' ', ''), '(', ''), ')', ''), '-', ''), '+', ''), ' ', ''), 2)
                    LEFT JOIN adb.ZABCDRECORD ON ZABCDPHONENUMBER.ZOWNER = ZABCDRECORD.Z_PK
                    ORDER BY date DESC;
                    """
            cur = con.cursor()
            cur.execute(query)

            while True:
                batch = cur.fetchmany(100)  # Adjust the batch size as needed
                if not batch:
                    break

                for item in batch:
                    time, phone, name, text, blob = item
                    blob = memoryview(blob)

                    timestamp_seconds = time / 1e9  # Convert nanoseconds to seconds
                    epoch_datetime = datetime(2001, 1, 1, tzinfo=timezone.utc)
                    local_datetime = epoch_datetime + timedelta(seconds=timestamp_seconds)
                    local_datetime = local_datetime.astimezone()

                    formatted_datetime = local_datetime.strftime("%B %d, %Y %H:%M:%S")

                    print("Time:", formatted_datetime)
                    print("Phone Num: ", phone)
                    print("First Last:", name)
                    print("Text:", text)
                    if not text:
                        if blob:
                            streamReader = TypedStreamReader(blob)
                            # streamReader.
                # break
            cur.close()


allTexts = TextMessages()
allTexts.get_text_messages()

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
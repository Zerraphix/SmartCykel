from machine import Pin
from time import sleep
from mfrc522 import MFRC522

# Match these to your real wiring:
SCK = 18
MOSI = 23
MISO = 19
RST = 5
SDA = 33   # CS / SDA

reader = MFRC522(
    sck=SCK,
    mosi=MOSI,
    miso=MISO,
    rst=RST,
    cs=SDA,
)

ALLOWED_TAGS = [
    "058A0D02",
    "11223344",
]

def read_tag():
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            uid_hex = "".join("{:02X}".format(x) for x in uid)
            return uid_hex
    return None

def tag_is_allowed(tag):
    if not tag:
        return False
    return tag in ALLOWED_TAGS


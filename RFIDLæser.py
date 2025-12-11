# rc522_reader.py

from machine import Pin, SoftSPI
from time import sleep
from mfrc522 import MFRC522

# Pins til RC522
SCK = 18
MOSI = 13
MISO = 12
RST = 5
CS  = 21

# Soft-SPI
spi = SoftSPI(
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    sck=Pin(SCK),
    mosi=Pin(MOSI),
    miso=Pin(MISO),
)

# RFID-læser
reader = MFRC522(
    sck=SCK,
    mosi=MOSI,
    miso=MISO,
    rst=RST,
    cs=CS,
)

# Tilladte tags (skriv dine egne UID'er her, i HEX som fra testen)
ALLOWED_TAGS = [
    "058A0D02",  # eksempel
    "11223344",  # eksempel
]


def read_tag():
    """Returnerer UID som streng, fx 'A1B2C3D4', eller None hvis intet kort."""
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            uid_hex = "".join("{:02X}".format(x) for x in uid)
            sleep(0.1)
            return uid_hex

    return None


def tag_is_allowed(tag):
    """True hvis tag findes i ALLOWED_TAGS, ellers False."""
    if not tag:
        return False
    return tag in ALLOWED_TAGS

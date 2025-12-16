from mfrc522 import MFRC522

# RC522 pins
SCK_PIN  = 18
MOSI_PIN = 13
MISO_PIN = 12
RST_PIN  = 5
CS_PIN   = 21

# Her skriver du det tilladte kort:
ALLOWED_TAG = " "   # ← udskift med dit rigtige UID

rdr = MFRC522(
    sck=SCK_PIN,
    mosi=MOSI_PIN,
    miso=MISO_PIN,
    rst=RST_PIN,
    cs=CS_PIN
)

def read_tag():
    stat, _ = rdr.request(MFRC522.REQIDL)

    if stat == MFRC522.OK:
        stat, uid = rdr.anticoll()
        if stat == MFRC522.OK:
            tag = "{:02X}{:02X}{:02X}{:02X}".format(
                uid[0], uid[1], uid[2], uid[3]
            )
            rdr.select_tag(uid)
            return tag

    return None

def tag_is_allowed():
    tag = read_tag()
    if tag:
        return tag == ALLOWED_TAG
    return False

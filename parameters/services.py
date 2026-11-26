from datetime import date

from parameters.catalog import ROOT, read_pinned

REVISION = "sn-services-01"
DIGEST = "c2a4a48becc5ba21d4b1f57a4b2c9adb12c8a7a869da762199bee3c34a68e948"
PERIOD = date(2027, 3, 1)


def load_rules():
    return read_pinned(ROOT / "data" / f"{REVISION}.json", DIGEST)

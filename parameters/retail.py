"""Complete the pinned retail edition with the 2027–28 Annex I allocation table."""
from parameters.catalog import DIGESTS, ROOT, CatalogError, read_pinned, resolve

REVISION = "sn-retail-2027-01"
DIGEST = "ad66937ec83bfd3c177dc1101ced8524373e98e215aa41c93788e4685cc3e9ec"
BASE = "sn-03-02"


def load_retail(period):
    edition = read_pinned(ROOT / "data" / f"{REVISION}.json", DIGEST)
    catalog, rules, _ = resolve(BASE, period)
    if (edition["extends"] != BASE or edition["revision"] != REVISION
            or not edition["start"] <= period.isoformat() <= edition["end"]):
        raise CatalogError("Complemento do Anexo I incompatível com a vigência ou edição.")
    bands = edition["additional_bands"] + rules["bands"]
    reference = next(band["shares"] for band in bands if band["number"] == 4)
    for band in bands:
        if "shares" not in band:
            changes = edition["share_overrides_from_band_4"][str(band["number"])]
            band["shares"] = reference | changes
    return dict(bands=bands, annual_sublimit=rules["annual_sublimit"],
                source=dict(base=catalog["sources"], table=edition["source"], url=edition["url"],
                            base_revision=BASE, base_sha256=DIGESTS[BASE], consulted=edition["consulted"],
                            validity=[edition["start"], edition["end"]]))

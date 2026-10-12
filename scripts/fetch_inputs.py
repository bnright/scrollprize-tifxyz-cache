"""Retrieve the two public source meshes anonymously and verify every byte.

No account, registration, form submission or terms checkbox is used. Original
data remain private local research copies; do not include them in a code release.
"""
import hashlib
import json
from urllib.request import urlopen
from source_loader import ROOT

DIRECTORIES = {
    "PHerc0139": "PHerc0139-w025-9.362um.tifxyz",
    "PHerc0800": "PHerc0800-auto-grown-8.64um.tifxyz",
}


def main():
    for manifest in sorted((ROOT / "docs").glob("*-provenance.json")):
        data = json.loads(manifest.read_text(encoding="utf-8-sig"))
        directory = ROOT / "private-data" / DIRECTORIES[data["scroll"]]
        directory.mkdir(parents=True, exist_ok=True)
        for item in data["files"]:
            destination = directory / item["file"]
            if destination.exists():
                contents = destination.read_bytes()
            else:
                with urlopen(item["url"], timeout=60) as response:
                    contents = response.read(item["bytes"] + 1)
            if len(contents) != item["bytes"] or hashlib.sha256(contents).hexdigest() != item["sha256"]:
                raise ValueError(f"Size/hash mismatch: {item['url']}")
            if not destination.exists():
                destination.write_bytes(contents)
            print(f"Verified {data['scroll']}/{item['file']}: {len(contents)} bytes")


if __name__ == "__main__":
    main()

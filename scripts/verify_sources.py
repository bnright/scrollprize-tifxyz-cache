"""Verify the immutable official-source snapshot against its manifest."""
import hashlib
import json
from source_loader import ROOT


def main():
    manifest = json.loads((ROOT / "docs" / "source-manifest.json").read_text(encoding="utf-8-sig"))
    for item in manifest["files"]:
        contents = (ROOT / "upstream" / item["file"]).read_bytes()
        if len(contents) != item["bytes"] or hashlib.sha256(contents).hexdigest() != item["sha256"]:
            raise ValueError(f"Upstream snapshot mismatch: {item['file']}")
        blob = b"blob " + str(len(contents)).encode() + b"\0" + contents
        if hashlib.sha1(blob).hexdigest() != item["git_blob_sha1"]:
            raise ValueError(f"Official Git blob mismatch: {item['file']}")
    print(f"PASS: {len(manifest['files'])} official source files match revision {manifest['revision']}")


if __name__ == "__main__":
    main()

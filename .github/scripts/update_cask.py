#!/usr/bin/env python3
"""Synchronize the cask with the upstream stable native release."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request


REPOSITORY = "originalmagneto/chevron7"
VERSION = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
CASK = Path("Casks/chevron7.rb")


def release_asset(release):
    if release.get("draft") is not False or release.get("prerelease") is not False:
        raise ValueError("Expected a published stable release")
    tag = release.get("tag_name", "")
    if not isinstance(tag, str) or not re.fullmatch("native-v" + VERSION, tag):
        raise ValueError("Expected a native-vMAJOR.MINOR.PATCH release tag")
    version = tag.removeprefix("native-v")
    assets = [asset for asset in release["assets"] if asset.get("name") == "Chevron7.dmg"]
    if len(assets) != 1:
        raise ValueError("Expected exactly one Chevron7.dmg release asset")
    asset = assets[0]
    url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/Chevron7.dmg"
    digest = asset.get("digest", "")
    if not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("The DMG must have a GitHub SHA-256 digest")
    if asset.get("browser_download_url") != url or asset.get("state") != "uploaded":
        raise ValueError("Unexpected DMG URL or upload state")
    if type(asset.get("size")) is not int or asset["size"] <= 0:
        raise ValueError("The DMG must have a positive byte size")
    return version, digest.removeprefix("sha256:"), url, asset["size"]


def updated_cask(source, version, digest):
    versions = re.findall(r'^  version "([^"]+)"$', source, re.MULTILINE)
    hashes = re.findall(r'^  sha256 "([0-9a-f]{64})"$', source, re.MULTILINE)
    if len(versions) != 1 or len(hashes) != 1 or not re.fullmatch(VERSION, versions[0]):
        raise ValueError("Expected a single version and SHA-256 in the cask")
    if tuple(map(int, version.split("."))) < tuple(map(int, versions[0].split("."))):
        raise ValueError("Refusing to downgrade the cask")
    source = re.sub(r'^  version "[^"]+"$', f'  version "{version}"', source, flags=re.MULTILINE)
    return re.sub(r'^  sha256 "[0-9a-f]{64}"$', f'  sha256 "{digest}"', source, flags=re.MULTILINE)


def main():
    release = json.loads(subprocess.check_output([
        "gh", "api", f"repos/{REPOSITORY}/releases/latest",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
    ], text=True))
    version, digest, url, size = release_asset(release)
    source = CASK.read_text()
    updated = updated_cask(source, version, digest)
    if updated == source:
        print(f"Chevron7 {version} is already current")
        return
    checksum = hashlib.sha256()
    downloaded = 0
    with urllib.request.urlopen(url, timeout=60) as response:
        while chunk := response.read(1024 * 1024):
            downloaded += len(chunk)
            if downloaded > size:
                raise ValueError("Downloaded DMG exceeds the published size")
            checksum.update(chunk)
    if downloaded != size or checksum.hexdigest() != digest:
        raise ValueError("Downloaded DMG does not match the published size and SHA-256")
    CASK.write_text(updated)
    print(f"Updated Chevron7 to {version} with verified SHA-256 {digest}")


if __name__ == "__main__":
    main()

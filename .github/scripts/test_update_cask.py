import copy
import unittest

from update_cask import release_asset, updated_cask


class UpdateCaskTests(unittest.TestCase):
    def setUp(self):
        self.digest = "a" * 64
        self.url = "https://github.com/originalmagneto/chevron7/releases/download/native-v1.14.3/Chevron7.dmg"
        self.release = {
            "tag_name": "native-v1.14.3", "draft": False, "prerelease": False,
            "assets": [{"name": "Chevron7.dmg", "state": "uploaded", "size": 123,
                        "digest": f"sha256:{self.digest}", "browser_download_url": self.url}],
        }
        self.cask = f'cask "chevron7" do\n  version "1.9.0"\n  sha256 "{"b" * 64}"\n  app "Chevron7.app"\nend\n'

    def test_stable_asset(self):
        self.assertEqual(release_asset(self.release), ("1.14.3", self.digest, self.url, 123))

    def test_rejects_invalid_releases(self):
        for key, value in [("draft", True), ("prerelease", True), ("tag_name", "native-v1.14.3-rc.1"),
                           ("tag_name", "native-v01.14.3"), ("tag_name", "v1.14.3"),
                           ("assets", []), ("assets", self.release["assets"] * 2)]:
            with self.subTest(key=key, value=value):
                release = dict(self.release, **{key: value})
                with self.assertRaises(ValueError):
                    release_asset(release)

    def test_rejects_invalid_assets(self):
        for key, value in [("digest", None), ("digest", "sha256:invalid"),
                           ("browser_download_url", "https://example.com/Chevron7.dmg"),
                           ("state", "new"), ("size", 0), ("size", True)]:
            with self.subTest(key=key, value=value):
                release = copy.deepcopy(self.release)
                release["assets"][0][key] = value
                with self.assertRaises(ValueError):
                    release_asset(release)

    def test_only_version_and_digest_change_and_repeat_is_noop(self):
        updated = updated_cask(self.cask, "1.14.3", self.digest)
        self.assertEqual(updated, self.cask.replace('"1.9.0"', '"1.14.3"').replace("b" * 64, self.digest))
        self.assertEqual(updated_cask(updated, "1.14.3", self.digest), updated)

    def test_rejects_downgrade_and_ambiguous_cask(self):
        with self.assertRaises(ValueError):
            updated_cask(self.cask, "1.8.9", self.digest)
        for source in [self.cask.replace("sha256", "other"), self.cask + '  version "1.9.0"\n']:
            with self.assertRaises(ValueError):
                updated_cask(source, "1.14.3", self.digest)


if __name__ == "__main__":
    unittest.main()

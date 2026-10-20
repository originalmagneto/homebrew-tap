# Chevron7 Homebrew tap

Install [Chevron7](https://github.com/originalmagneto/chevron7), the macOS electronic document signing app, on Apple Silicon running macOS 27 or later. [Homebrew](https://brew.sh) is required.

```sh
brew install --cask originalmagneto/tap/chevron7
```

The cask installs `Chevron7.app` from the project's GitHub release DMG. It does not install smart-card drivers. Install any drivers required by your signing card separately.

## Updates

Chevron7 updates itself through Sparkle. To explicitly update it through Homebrew instead:

```sh
brew update
brew upgrade --cask --greedy originalmagneto/tap/chevron7
```

`--greedy` includes this self-updating app. The tap's **Update Chevron7 cask** GitHub Actions workflow checks for stable native releases every six hours (00:17, 06:17, 12:17 and 18:17 UTC; GitHub may delay runs). It checks the downloaded DMG's size and SHA256 against GitHub's release metadata before updating the cask. Maintainers can also run it manually from the Actions tab.

## Uninstall

```sh
brew uninstall --cask originalmagneto/tap/chevron7
```

This removes the app, not your documents, signing evidence or app data. The cask has no `zap` stanza.

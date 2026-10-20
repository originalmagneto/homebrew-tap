cask "chevron7" do
  version "1.14.3"
  sha256 "ad5eb0a1614cdd8bb33879cb2801aae80b5584cd5c71a1f8fd27291b11016e58"

  url "https://github.com/originalmagneto/chevron7/releases/download/native-v#{version}/Chevron7.dmg"
  name "Chevron7"
  desc "Electronic document signing for macOS"
  homepage "https://github.com/originalmagneto/chevron7"

  livecheck do
    url :url
    regex(/^native-v(\d+(?:\.\d+)+)$/i)
    strategy :github_latest
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :any

  app "Chevron7.app"

  # shortcut: Homebrew has no macOS 27 symbol yet; use depends_on when it does.
  preflight_steps do
    run "/bin/sh", args: ["-c", <<~'SH']
      version=$(/usr/bin/sw_vers -productVersion) && [ "${version%%.*}" -ge 27 ] || {
        echo "Chevron7 requires macOS 27 or later." >&2
        exit 1
      }
    SH
  end
end

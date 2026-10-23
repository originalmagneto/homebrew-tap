cask "chevron7" do
  version "1.16.0"
  sha256 "dfc5d2d97ac31d9e4411643bcd6f0a5ffe50391308de25b977004b4d0fc0ae29"

  url "https://github.com/originalmagneto/chevron7/releases/download/native-v#{version}/Chevron7.dmg"
  name "Chevron7"
  desc "Electronic document signing"
  homepage "https://github.com/originalmagneto/chevron7"

  livecheck do
    url :url
    regex(/^native-v(\d+(?:\.\d+)+)$/i)
    strategy :github_latest
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :golden_gate

  app "Chevron7.app"
end

cask "chevron7" do
  version "1.19.0"
  sha256 "66e87293a0ba3862c7ea7fe2e8bccffe391b0b510953e2181999dfa21cff81cc"

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

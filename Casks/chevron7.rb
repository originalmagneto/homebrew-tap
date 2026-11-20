cask "chevron7" do
  version "1.21.6"
  sha256 "ebe43092a1962c5028399c712bb74ab08061ff086b391efc443343cc58a17d65"

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

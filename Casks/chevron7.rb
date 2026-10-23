cask "chevron7" do
  version "1.18.0"
  sha256 "09f57a4fc39b1128254722040f6be0cb857fcf5292b097e911b91a1439dcbda9"

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

[app]

title = Guess Master
package.name = guessmaster
package.domain = org.guessmaster

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.accept_sdk_license = True
android.api = 35
android.minapi = 21
android.ndk = 28c
android.ndk_api = 21
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 0

[app]

title = Detecteur Spam
package.name = detecteurspam
package.domain = org.detecteurspam

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 36
android.minapi = 24
android.ndk = 28c

android.accept_sdk_license = True

p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1

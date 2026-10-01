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

android.api = 33
android.minapi = 21

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1

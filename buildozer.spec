[app]

# (str) Title of your application
title = Guess Master

# (str) Package name
package.name = guessmaster

# (str) Package domain (needed for android packaging)
package.domain = org.game

# (str) Source code directory (where your main.py is)
source.dir = .

# (str) Application versioning
version = 0.1

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
requirements = python3,kivy,android

# (str) Supported orientations
orientation = portrait

# (bool) Accept android SDK licenses automatically (هذا هو السطر الجديد المهم لحل مشكلة التوقف)
android.accept_sdk_license = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug command)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

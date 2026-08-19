[app]

# (str) Title of your application
title = Guess Master

# (str) Package name
package.name = guessmaster

# (str) Package domain (needed for android packaging)
package.domain = org.game

# (str) Source code directory (where your main.py is)
source.dir = .

# (str) Application versioning (add this line)
version = 0.1

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
requirements = python3,kivy,android

# (str) Supported orientations
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

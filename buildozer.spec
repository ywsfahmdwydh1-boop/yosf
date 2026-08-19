[app]

# (str) Title of your application
title = Guess Master

# (str) Package name
package.name = guessmaster

# (str) Package domain (needed for android packaging)
package.domain = org.game

# (list) Source files to include (let it include your python files and assets)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application requirements
requirements = python3,kivy,android

# (str) Supported orientations
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

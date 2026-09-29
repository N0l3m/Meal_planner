[app]

# title of your application
title = MealPlanner

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = main.py

# directory where the executable output is generated
exec_directory = .

# path to the project file relative to project_dir
project_file = 

# application icon
icon = /home/francsix/Documents/Programming/Meal_planner/android-venv/lib/python3.11/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg

[python]

# python path
python_path = /home/francsix/Documents/Programming/Meal_planner/android-venv/bin/python3.11

# python packages to install
packages = Nuitka==4.1.1

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
qml_files = 

# excluded qml plugin binaries
excluded_qml_plugins = 

# qt modules used. comma separated
modules = Gui,Widgets,Core

# qt plugins used by the application. only relevant for desktop deployment
plugins = 

[android]

# path to pyside wheel
wheel_pyside = /home/francsix/Documents/Programming/Meal_planner/android-wheels/pyside6-6.11.2-6.11.2-cp311-cp311-android_aarch64.whl

# path to shiboken wheel
wheel_shiboken = /home/francsix/Documents/Programming/Meal_planner/android-wheels/shiboken6-6.11.2-6.11.2-cp311-cp311-android_aarch64.whl

# plugins to be copied to libs folder of the packaged application
plugins = platforms_qtforandroid

# android sdk
sdk_path = /home/francsix/Android/Sdk

# android ndk
ndk_path = /home/francsix/Android/Sdk/ndk/26.1.10909125

[nuitka]

# usage description for permissions requested by the app
macos.permissions = 

# mode of using nuitka
mode = onefile

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir = /home/francsix/Documents/Programming/Meal_planner/app/src/deployment/recipes

# path to pyside6 jars
jars_dir = /home/francsix/Documents/Programming/Meal_planner/app/src/deployment/jar/PySide6/jar

# android ndk
ndk_path = /home/francsix/Android/Sdk/ndk/26.1.10909125

# android sdk
sdk_path = /home/francsix/Android/Sdk

# local libraries
local_libs = plugins_platforms_qtforandroid

# architecture
arch = aarch64


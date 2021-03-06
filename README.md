# Description

A simple cross-platform python-based launcher to be used with Legends of Equestria.

# Main Features

* Launching the game
* Version checking, so you know when a new version is available

# Dependencies

* [Python 3](https://www.python.org/downloads/)

# Running

## From a terminal/command line
On Linux:
> ./launcher.py

On Linux or Mac, if you have the Python 3 executable in your path (It is possible the executable for Python 3 may be python instead of python3):
> python3 launcher.py

On Windows:
> launcher.bat

## From a file manager
On Linux, with most file managers, you should be able to double-click launcher.py to run it.

On Windows, double click on launcher.bat

# Usage
On first run, the launcher will have you select the game directory. It must be the directory that contains loe_Data. The main dialog allows you to switch this directory later. On later runs, if the game directory is moved or deleted, the launcher will ask for a new game directory.

The main dialog displays the current game directory, the installed version, and the available version.

The versions will start being fetched after the dialog opens. The installed version check should be nearly instantaneous. The available version check requires a web request, but it is a pretty small json file, so it should normally be very fast.

Note: The launcher does not force you to wait for the versions to be checked.

When you press launch, the launcher will look for the executable appropriate for your system and launch it. The launcher should exit afterwards.

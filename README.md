# KLayout Duplicate Shape Detection and Deletion Scripts
This repository contains Python scripts for KLayout designed to detect and optionally delete overlapping duplicate shapes in GDS layouts. These tools help in ensuring layout integrity by identifying and removing redundant shapes that may cause fabrication or simulation issues.
Features

* Detection Only Mode: Identify overlapping duplicate shapes across all layers or specific layers.
* Automatic Deletion: Optionally delete duplicates to keep only one instance of each shape.
* Flexible Layer Selection: Check all layers by default or specify individual layers and datatypes for targeted analysis.

Usage

* Install the Script: Add the script to your KLayout macros or import it directly.
* Run the Script: Use detection mode to identify duplicates or enable deletion to remove them.
* Configuration: Easily adjust the script settings to customize detection and deletion parameters.

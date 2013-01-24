#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyside-uic --from-imports dialog.ui > ../python/tk_multi_breakdown/ui/dialog.py
pyside-uic --from-imports item.ui > ../python/tk_multi_breakdown/ui/item.py

echo "building resources..."
pyside-rcc resources.qrc > ../python/tk_multi_breakdown/ui/resources_rc.py

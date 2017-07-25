#!/usr/bin/python
#
#     'SavantSceneDelete'
#     Copyright (C) '2017' J14 Systems
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>

import sqlite3
import os.path
from subprocess import call

try:
    if os.path.isfile('/Users/RPM/Library/Application Support/RacePointMedia/statusfiles/dis/dashboard.sqlite'):
        hosttype = "pro"
        database = "/Users/RPM/Library/Application Support/RacePointMedia/statusfiles/dis/dashboard.sqlite"
    elif os.path.isfile('/data/RPM/GNUstep/Library/ApplicationSupport/RacePointMedia/statusfiles/dis/dashboard.sqlite'):
        hosttype = "smart"
        database = "/data/RPM/GNUstep/Library/ApplicationSupport/RacePointMedia/statusfiles/dis/dashboard.sqlite"
    else:
        hosttype = "none"
        while True:
            databasepath = raw_input("Type the path to your dashboard.sqlite database: ")
            if os.path.isfile(databasepath):
                database = databasepath
                break

    print "Running on a host type of: %s" % hosttype

    if hosttype != "none":
        while True:
            confirm1 = raw_input("Savant needs to be disabled to continue, type 'yes' to confirm: ")
            if confirm1.lower() == 'yes':
                call('/usr/local/bin/rpm/stopSavantSystem')
                break

    while True:
        dashbaord = sqlite3.connect(database)
        query1 = dashbaord.execute("SELECT * FROM Scenes")
        scenenum = 1
        selection = 0
        scenes = {}

        print "Found Scenes:"
        print "----------------------------------------"
        for row in query1:
            print "%s: %s [Active In: %s]" % (scenenum, row[1], row[3])
            scenes[scenenum] = row
            scenenum += 1
        print "----------------------------------------"
        while True:
            try:
                selection = int(raw_input("Type a scene number to delete it: "))
                if selection in scenes:
                    break
                else:
                    raise KeyError
            except ValueError:
                print "Please enter a number from 1 to %s" % (scenenum - 1)
            except KeyError:
                print "Please enter a number from 1 to %s" % (scenenum - 1)

        print "----------------------------------------"
        print "You have chosent to delete \"%s\" which is active in the following zone(s): %s" \
              % (scenes[selection][1], scenes[selection][3])
        print "----------------------------------------"
        confirm = raw_input("Type 'yes' to confirm: ")
        print "----------------------------------------"
        if confirm.lower() == 'yes':
            dashbaord.execute("DELETE from Scenes WHERE identifier = '%s'" % scenes[selection][0])
            dashbaord.execute("DELETE from SceneUserMap WHERE sceneIdentifier = '%s'" % scenes[selection][0])
            dashbaord.execute("DELETE from SceneDefinitions WHERE sceneIdentifier = '%s'" % scenes[selection][0])
            dashbaord.commit()
            print "Scene \"%s\" deleted" % scenes[selection][1]


        print "----------------------------------------"
        confirm2 = raw_input("Would you like to delete any other scenes? yes or no: ")
        print "----------------------------------------"
        if confirm2.lower() != 'yes':
            break


    if hosttype != "none":
        while True:
            confirm1 = raw_input("Savant can now be restarted, type 'yes' to confirm: ")
            if confirm1.lower() == 'yes':
                call('/usr/local/bin/rpm/startSavantSystem')
                break
            elif confirm1.lower() == "no":
                print "Not restarting Savant system. This will have to be done manually"

except KeyboardInterrupt:
    print "Thanks for using J14 Systems Scene Deletion tool!"

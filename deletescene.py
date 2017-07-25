#!/usr/bin/python
#     
#     'SavantSceneDelete'
#     Copyright (C) '2017'  J14 Systems
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

dashbaord = sqlite3.connect('dashboard.sqlite')
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

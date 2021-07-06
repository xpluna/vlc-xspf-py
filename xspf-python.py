##############################
##       Project XSPF       ##
##############################

## >> Automate Python to make VLC Bookmarks
## >> with the timestamps and topics you have!

## Written in Python with Notepad++

## Works on Windows (both x86 and x64 builds)
## Not tested on Mac and Linux

## This is made for videos of length lesser than or 
## equal to 9 hrs 59 min 59s [9:59:59]

## Store the timestamps and topics separated by a space
## in a text file named stamps.txt in the same directory 
## of this file

## The timestamp should be in a H:MM:SS format 
## with no additional initial characters.

## Example of stamps.txt
##
## 1:04:12 Manipulating lists with .pop()
## 1:09:23 Manipulating lists with .sort()
##
## Non-float timestamp <space> Topic
## ^ FORMAT

######################################################################
######################################################################
from pymediainfo import MediaInfo
import os

os.system("pip install pymediainfo")

lines = [] ## To store file contents

with open('D:\\Downloads\\_Miscellaneous\\stamps.txt', 'r') as obj:
    for line in obj.readlines():
        lines.append(line.rstrip())
    
    while '' in lines:
        lines.remove('') ## Eliminate pesky blankspaces

print("\n##############################\n" + 
      "##       Project XSPF       ##\n" +
      "##############################\n\n")

print(f'Finished reading \'stamps.txt\'...\nTimestamp Count = {len(lines)}\n\n')

vidDir = str(input("Video location/directory\n>>> ")).strip()
vid = str(input('\nVideo name [extension exclusive]\n>>> ')).strip()
vidExt = str(input('\nVideo extension [include .]\n>>> '))

xspf_File_Dir = 'file:///' + vidDir.replace('\\', '/') + '/' + vid + vidExt ## Needed as file path in .xspf

def toSec(time, decimal=False):
    '''
    Returns H:Mm:Ss to S format
    '''
    
    duration = '' ## For duration tag in .xspf
    
    ## Cases for 0 in H:Mm:Ss [Y/N]
    ## ┌───┬───┬───┐
    ## │ H │ M │ S │
    ## ├───┼───┼───┤
    ## │ N │ N │ N │ 1
    ## │ N │ N │ Y │ 2
    ## │ N │ Y │ N │ 3
    ## │ N │ Y │ Y │ 4
    ## │ Y │ N │ N │ 5
    ## │ Y │ N │ Y │ 6
    ## │ Y │ Y │ N │ 7
    ## │ Y │ Y │ Y │ 8
    ## └───┴───┴───┘

    ## Case 1
    if time[0] != '0' and time[2] != '0' and time[-2] != '0':
        duration += str(int(time[0])*3600 + int(time[2:4])*60 + int(time[-2:]))

    ## Case 8
    elif time[0] == '0' and time[2] == '0' and time[-2] == '0':
        duration += str(int(time[3])*60 + int(time[-1]))

    ## Cases 4 & 3 resp
    elif time[0] != '0' and time[2] == '0':
        if time[-2] == '0':
            duration += str(int(time[0])*3600 + int(time[3])*60 + int(time[-1]))
        else:
            duration += str(int(time[0])*3600 + int(time[3])*60 + int(time[-2:]))
    
    ## Case 2
    elif time[0] != '0' and time[2] != '0' and time[-2] == '0':
        duration += str(int(time[0])*3600 + int(time[2:4])*60 + int(time[-1]))
    
    ## Cases 6 & 5 resp
    elif time[0] == '0' and time[2] != '0':
        if time[-2] == '0':
            duration += str(int(time[2:4])*60 + int(time[-1]))
        else:
            duration += str(int(time[2:4])*60 + int(time[-2:]))

    ## Case 7
    elif time[0] == '0' and time[2] == '0' and time[-2] != '0':
        duration += str(int(time[3])*60 + int(time[-2:]))
    
    if decimal == False:
        return duration
    
    elif decimal == True:
        duration += '.000'
        return duration

## Millisecond length
fpath = vidDir.replace('\\', '\\\\') + '/' + vid + vidExt
msl = MediaInfo.parse(f"{fpath}").tracks[0].duration

## Writing to a xspf [Part-1/2]
with open(f'{vid}.xspf', 'w') as obj:
    obj.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">\n    <title>Playlist</title>\n    <trackList>\n        <track>\n            <location>{xspf_File_Dir}</location>\n            <duration>{msl}</duration>\n            <extension application="http://www.videolan.org/vlc/playlist/0">\n                <vlc:id>0</vlc:id>\n                <vlc:option>bookmarks=')

## Iterating over the list and turning into a dictionary
 
data = {}
## data = {'topic': timestamp}

for line in lines:
    data[line[8:].replace(',', ';')] = toSec(line[:7], decimal=True)
    ## Don't know why VLC can't parse ',' as bookmark when automated,
    ## But does when done manually :shrug

bookmark = '' ## Bookmarks, a part of file output

for topic, timestamp in data.items():
    bookmark += '{name=' + topic + ',time=' + timestamp + '}, ' ## I guess f-string cannot parse nested {}

## Writing (appending) to a xspf [Part-2/2]
with open(f'{vid}.xspf', 'a') as obj:
    obj.write(bookmark[:-2] + '</vlc:option>\n            </extension>\n        </track>\n    </trackList>\n    <extension application="http://www.videolan.org/vlc/playlist/0">\n        <vlc:item tid="0"/>\n    </extension>\n</playlist>')
    
input('\nDone! Press any key to exit.')

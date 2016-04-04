Linux Ubuntu Users:
- Install php5-cgi "sudo apt-get install php5-cgi".
- For other distributions check the name of package (could be different) and install it.
- Check the correct path (/usr/bin/ by default) in the add-on settings.

OpenELEC: (thanks to zutimmung)
- Install the php-cgi from http://wiki.openelec.tv/index.php?title=RTorrent_Service_Add-on (use the ARM Package for the RPi).
- Move php-cgi executable in a folder that won't be rewritten when updating OpenELEC.
- Make php-cgi executable (e.g. sudo chmod +x php-cgi).
- Check the correct path (/usr/bin/ by default) in the add-on settings.

Windows Users:
- Download php-cgi from http://windows.php.net/download/ choose the last "VC9 x86 Non Thread Safe" zip package.
- Download the x86 version of VisualStudio C++ 2012 from http://www.microsoft.com/en-us/download/details.aspx?id=30679 (need if missing msvcr110.dll)
- Unzip in C:\php5\ or wherever you like.
- Update the correct path in the add-on settings.

Android Users: (thanks to sd26)
- Follow this link http://forum.xda-developers.com/showthread.php?t=1242144 and extract php-cgi for ARM cpu.
- Update the correct path in the add-on settings.

Mac Users:
- Sorry, I don't have a Mac. Search in Google on how to install PHP :-D
- Update the correct path in the add-on settings.

For Skinners:
- To run in Background Mode (adjust settings): <onclick>RunScript(script.ratingupdate)</onclick>
- To run single Movie update: <onclick>RunScript(script.ratingupdate,Single=Movie)</onclick>
- To run single TV Show update: <onclick>RunScript(script.ratingupdate,Single=TVShow)</onclick>

For any question or problem go to http://forum.xbmc.org/showthread.php?tid=107331 and post a debug log using paste.bin or similar.

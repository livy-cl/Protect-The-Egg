#Egg Security with Micropython
A stem project for my school using an esp8266 with micropython flashed.

## Flashing
Under the [esptools](https://github.com/espressif/esptool) directory you can find the [micropython firmware](https://github.com/janjcool/Egg-Security/blob/master/esptools/esp8266-v1.13.bin) (the .bin file), and the [esptool file](https://github.com/janjcool/Egg-Security/blob/master/esptools/esptool) for flashing the firmware on the esp8266 (esptool file is only tested on Linux). See the [read.me](https://github.com/janjcool/Egg-Security/blob/master/esptools/read.me) in the esptools directory for more info.

## The project
My group needs to protect an egg by using a laser tripwire set up. This goes as follows: the laser reflects on 2 mirrors to enter a sensor, when the thief wants to steal the egg he will interrupt the laser so that there is no light on the sensor. My part of the project is programming the sensor and the laser.

## Note
This website and project have been build on [the Linux file system](https://www.howtogeek.com/137096/6-ways-the-linux-file-system-is-different-from-the-windows-file-system/). If you want to use this on Windows, you would need to change all the directory's from a foreword slash / (the Linux standard) to a backward slash \ (the Windows standard). For example "data/config" would become "data\config".

## Compressed and compiled
In the [compressed folder](https://github.com/janjcool/Egg-Security/tree/master/src-compressed), you will find 3 folders. The first folder [pyFiles](https://github.com/janjcool/Egg-Security/tree/master/src-compressed/pyFiles) I put all the [source files](https://github.com/janjcool/Egg-Security/tree/master/src) and made them as small as possible. In the second folder, [mpyFiles](https://github.com/janjcool/Egg-Security/tree/master/src-compressed/mpyFiles), you can find all compiled files, and the not compiled files [boot.py](https://github.com/janjcool/Egg-Security/blob/master/src-compressed/mpyFiles/boot.py) and [main.py](https://github.com/janjcool/Egg-Security/blob/master/src-compressed/mpyFiles/main.py).  I compiled the files using a tool called [mpy-cross](https://github.com/micropython/micropython/tree/master/mpy-cross). This tool and all its dependencies you can find in the third folder: [mpyFileCompiler](https://github.com/janjcool/Egg-Security/tree/master/src-compressed/mpyFileCompiler).

##Regrets
I have 3 main regrets for this project. The first one is using the [esp8266 and not the esp32](https://community.wia.io/d/53-esp8266-vs-esp32-what-s-the-difference), the esp32 has a lot more pins and tools like multi-threading. The second one is that I didn't write very [object-orientated](https://en.wikipedia.org/wiki/Object-oriented_programming) I just saved everything in a dictionary instead of classes. The last regret is not properly planning out this project in advance, which means I needed to throw a lot of work away.

## License
[MIT](https://choosealicense.com/licenses/mit/)

# SeosSniffer
A Java Card applet written for my BSc thesis. The Java applet tries to emulate an iClass Seos card and record the commands sent to it.

## In detail description
The applet is written a subset of the Java programming language and therefore lacks some features like String, int, float and other objects.

## Requirements
- OS: A Linux distro (Kali GNU/Linux Rolling 2020.4 release) was used. Other operating systems can be used, but weren't tried.
- ACR1252 USB NFC reader 
- A Java Card. A Feitian FT-Java/D11CR was used for testing.
- Python 3
- Python pyscard 2.0.0 library 
- Java 8 

## Converting source code to .cap
To compile the Java source code one needs to use `ant` but before compiling one needs to clone Martin Paljak's [ant-javacard][paljak's-git-repo-url] repository and change the below fields according to their own file structure.

![build.xml image](Images/change_build_xml.PNG?raw=true "build.xml fields that need to be changed")

Once change you can run `ant` and see a similar output.
```sh
ant
```
![ant command output](Images/ant.PNG?raw=true "ant command output")

## Uploading .cap file to Java card
To then upload the CAP file generated from the `ant` command one needs to have Martin Paljak's [Global Platform Pro][paljak's-gp-repo] (already downloaded). Global Platform Pro release version [v0.3.5][gp-v0.3.5] was used. Make sure to have a USB card reader connected to the computer/VM and then run:
```sh
java -jar gp.jar --install applet.cap --default 
````
This installs the applet onto the card and sets it as the default program in the card's memory.

## Interacting with the card
To verify if the install was a success or inspect the installed apps on the card you can use:
```sh
java -jar gp.jar --list
```

To delete an installed applet you need to run:
```sh
java -jar gp.jar --deletedeps --delete 0102030405
```
where '0102030405' is our applet's AID.

To retireve the recordings saved to the applets memory you need to use the 'receive_recordings.py'.
```sh
python3 receive_recordings.py
```
Other scripts:


[paljak's-ant-jcard-repo]: <https://github.com/martinpaljak/ant-javacard.git>
[paljak's-gp-repo]: <https://github.com/martinpaljak/GlobalPlatformPro.git>
[gp-v0.3.5]: <https://github.com/martinpaljak/GlobalPlatformPro/releases/tag/v0.3.5>


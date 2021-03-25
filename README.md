# SeosRecorder
This repository contains the code and applications written for a BSc thesis. It includes a Java Card applet for mimicking an iClass Seos card and Python scripts for communicating with it. The repository also contains the Jupyter Notebook used for analysing the more than 90 thousand Seos UIDs collected during testing.

## In detail description
To program a Java card, one must first write an applet in the specific [Java language subset][java-card-language]. One must then convert the source code into a .cap file that has to be loaded onto the Java card.
Once a programmed card is placed onto a high-frequency and ISO/IEC 14443 type A compatible reader (like an ACR-1252), it will record every command sent to it in its memory. The applet currently has 1536 bytes of memory which allows it to be used up to 7 times consecutively to record reader commands before it starts overriding itself.
A list of commands for communicating with the applet once it has been installed on the card are:

| Instruction byte | Meaning               |
|------------------|-----------------------|
| 0xF1             | Return memory array 1 |
| 0xF2             | Return memory array 2 |
| 0xF3             | Return memory array 3 |
| 0xF4             | Return memory array 4 |
| 0xF5             | Return memory array 5 |
| 0xF6             | Return memory array 6 |
| 0xFE             | Clear memory arrays   |

The commands sent to the card need to be in the [APDU format][apdu-format]. Two Python scripts are included in the Python Scripts directory to aid in communicating with the card. Further on them in the Scripts section.

## Requirements
- Operating System: A Linux distro (Kali GNU/Linux Rolling 2020.4 release) virtual machine was used. Other operating systems could potentially be used but were not tested
- ACR1252 USB NFC reader 
- A Java Card. A Feitian FT-Java/D11CR card was used for testing
- Python 3
- Python pyscard 2.0.0 library 
- Java 8 (since the installation for this is tedious, I will include two links \[[1][java-8-guide],[2][java-8-download]] to make it easier)

## Converting source code to .cap
To compile the Java source code, one needs to use `ant`, but before compiling, one needs to clone Martin Paljak’s [ant-javacard][paljak's-ant-jcard-repo] repository and change the below fields according to their file structure.

![build.xml image](Images/change_build_xml.PNG?raw=true "build.xml fields that need to be changed")

Once the values are changed, run `ant` and a similar output should be returned.

![ant command output](Images/ant.PNG?raw=true "ant command output")

## Uploading .cap file to the Java card
To then upload the .cap file generated from the `ant` command, one needs to use Martin Paljak's [Global Platform Pro][paljak's-gp-repo] hat is already included in the repository (Global Platform Pro release version [v0.3.5][gp-v0.3.5] was used). Make sure to have a USB card reader connected to the computer or VM and then run:
```sh
java -jar gp.jar --install applet.cap --default 
````
This command installs the applet onto the card and sets it as the default program in the card’s memory.

## Interacting with the Java card
To verify if the install was a success or inspect the installed apps on the card, use:
```sh
java -jar gp.jar --list
```

To delete an installed applet, one needs to run:
```sh
java -jar gp.jar --deletedeps --delete 0102030405
```
where '0102030405' is the applet's AID.

To retrieve the recordings saved to the applet’s memory, one needs to use the ‘receive_recordings.py’ script.
```sh
python3 receive_recordings.py
```
## Other scripts:
**seos_communication.py** - This script sends the Java card the same commands recorded during a legitimate reader, and Seos card communication. 

**receive_recordings.py** - This script sends the card instructions 0xF1-0xF6 commands, and so retrieves all information recorded. It then processes the collected data and prints out the commands in detail.

[java-card-language]:<https://www.oracle.com/java/technologies/java-card-tech.html>
[java-8-guide]:<https://www.javahelps.com/2015/03/install-oracle-jdk-in-ubuntu.html>
[java-8-download]:<https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html>
[apdu-format]:<https://en.wikipedia.org/wiki/Smart_card_application_protocol_data_unit>
[paljak's-ant-jcard-repo]: <https://github.com/martinpaljak/ant-javacard.git>
[paljak's-gp-repo]: <https://github.com/martinpaljak/GlobalPlatformPro.git>
[gp-v0.3.5]: <https://github.com/martinpaljak/GlobalPlatformPro/releases/tag/v0.3.5>

# Voice based Email For Blind [CLI] :email:	

<p align="center">
 <img src="https://i.ibb.co/zZnR5H3/download.png" border="0" /></p>

<p align="center">
 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/71e0d668762049618c4d33fb0a62b7a7)](https://www.codacy.com/manual/hacky1997/voice-based-email-for-blind?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hacky1997/voice-based-email-for-blind&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/codacy-coverage.svg)](https://badge.fury.io/py/codacy-coverage)
[![Circleci](https://circleci.com/gh/hacky1997/voice-based-email-for-blind.svg?style=svg)](https://circleci.com/gh/hacky1997/voice-based-email-for-blind)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/hacky1997/voice-based-email-for-blind/fork)
[![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)
 
`Created By : Sayak Naskar`
`License : MIT`
`Email: sayaknaskar@gmail.com`

</p>

**Free, Open-Source Emailing System for Blind**

## About
   The project is a `python-based` application for visually impaired persons using speech to text voice response, thus enabling everyone to control their mail accounts using their voice only and to be able to read,send, and perform all the other useful tasks. The system will prompt the user with voice commands to perform certain action and the user will respond to the same. The main benefit of this system is that the use of mouse is completely eliminated, the user will have to respond through voice only.
   
## Features
* Send email via voice.
* Fetch unseen emails.
* Count number of unseen emails.

## Modification
 * If you want to save the mp3 files in other directory then just follow the below instruction otherwise don't modify anything. 
 * Just add your desktop directory in code where I have used `path` words in several lines. If you don't know your desktop directory then just open `terminal` or `command prompt` and paste the below code. Like: `C:\Users\sayak\Desktop` (this is my desktop directory).
 
   ```%userprofile%\Desktop```
   
 * Also paste your `email id` and `password` in line number 104.
 * If `invalid or unsupported audio file` occurs or `Recall that only FLAC, AIFF, and RIFF WAV files are supported` occurs then try this [link](https://stackoverflow.com/questions/25672289/failed-to-open-file-file-wav-as-a-wav-due-to-file-does-not-start-with-riff-id/57349558#57349558). Read the file with `librosa`, then convert it back to a temporary `.wav` file. Then read it back with the `wave` package.
 * Okay so for SMTPAuthenticationError just visit this [site](https://myaccount.google.com/lesssecureapps). Allow the less secure  apps: ON

## Installation

<details><summary>Windows Installation</summary>

#### Installation with Python3
   ```C:\Users\sayak>git clone https://github.com/hacky1997/voice-based-email-for-blind.git```
   
   ```C:\Users\sayak>cd voice-based-email-for-blind```
   
   ```C:\Users\sayak>python3 -m pip install -r requirements.txt```
   
   ```C:\Users\sayak>python3 voice_based_email_for_blind.py```
 
</details>

<details><summary>Linux Installation</summary>

#### Installation with Python3
  ```root@kali:~/git clone https://github.com/hacky1997/voice-based-email-for-blind.git```
  
  ```root@kali:~/cd voice-based-email-for-blind```
  
  ```root@kali:~/pip3 install -r requirements.txt```
  
  ```root@kali:~/python3 voice_based_email_for_blind.py```
  
</details>

## Avbin
 * In some system, it requires avbin so keep it as it is. Don't delete those exe files.
 * So install `avbin`. I have provided two types of avbin. Just install one of them according your architecture.
 * If your system needs this then just uncomment line number 13 & 14 in the code.
 * For more info have a look on this [AVbin](https://github.com/AVbin/AVbin)
 * For download manually [AVbin](http://avbin.github.io/AVbin/Download.html)

## Pyaudio
 * Select your achitecture & Download [Pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) from this link.
 * Open the terminal where you have kept your `.whl` file and add the following command in terminal.

   ``` pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl```  
   
## Usage
 ```python3 voice_based_email_for_blind.py ```
 
## Warning
 This is a **personal** development, please respect its philosophy.
  
### **Note: I will try to modify this code and will upload the modified version. But due to some personal issue I am not able to complete it.
 
## Contribution
   Feel free to open issues or PRs for any problem you may encounter, typos that you see or aspects that are confusing. Contributions are welcome, open an issue or email me if you have something you want to work on.
 
## Thank you
I really appreciate all kinds of feedback. Thanks for using and supporting this project!

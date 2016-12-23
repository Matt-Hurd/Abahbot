# Abahbot

## What is Abahbot?
Abahbot was my very first public-facing script. What started out as an mirc script eventually turned into a Python bot.  
I started Abahbot in 2011 and used it as my introduction to Python. It has gone through many iterations, but I've kept the core the same, so it's sort of a mess.

## How do I use it?
Honestly, it's been quite a while since I've set it up, and the most recent additions were hacked together for maintenance. I had never planned for this code to be public, so it's not the most user friendly.  
  
First, you're going to need to add a file named `secrets.py`. Have the contents be `PASS="oauth:yourverylongoathhere"`, with your personal oath.  

Next, modify `abahbot.py`, changing the `OWNER`, `NICK`, and `BOTMODS` fields. You're also going to need to change several other instances of the term `abahbot` throughout.  
  
I believe I removed the old whisper features that utilized `groups.txt`, so that can be ignored.  
  
Modify `channels.txt` to have only the channels you wish to bot in.  
  
Remove unwanted quotes from `quotes.json`.  
  
It should *hopefully* be working now. Good luck!

## Why is this code so awful and buggy?
As I stated, this code was worked on as a way for me to learn Python. As tempting as it is to fix (or rewrite) it all, I'd most likely want to create a new bot in Go instead.

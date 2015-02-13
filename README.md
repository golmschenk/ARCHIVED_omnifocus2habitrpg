# OmniFocus To HabitRPG
## What does it do?
This script will allow you to quickly move completed tasks from OmniFocus to HabitRPG. It first grabs all tasks from OmniFocus that were *marked as completed today*. It will then find any of these tasks which have the exact same name as your HabitRPG dailies and complete them if they are not already completed. For any other completed tasks, it will display the name of each one and with a single key click you can ignore that task or send it to HabitRPG as a completed task. It also let's you choose which difficulty to submit it to HabitRPG as depending on which key you click.
## What doesn't it do?
This is not a full syncing service. It did what I needed and may help you. It's a short script and should be easy to modify should you want something slightly different.
## Setup
After you have installed the requirements (below), remove "template." from the secret file and add your secret tokens to the file from HabitRPG. Then just run the "of2hrpg" script.
## Requirements
+ Python3
+ py-applescript *(Python package)*
+ PyObjC *(Python package)*
+ OmniFocus **Pro** *(for Applescript support)*

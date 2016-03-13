# gasbot
A feature rich twitch moderation bot made with python 3.*

Old code can be found at my ruwbot repo

## Installation
Download the source code and place it somewhere on your computer. Make sure you have python 3 installed and added to your PATH variable. The bot has to be configured via the config.py file in order to run. To run the bot simply run the run.bat file (if you encounter problems try running the file as administrator) 

## Modules

#### Test Module
Displays the emote Kappa every time it recieves input form the channel.

#### Sound Module
Allows users to play sounds on the broadcasters computer for a cost of points set by the broadcaster in the configuration file

#### Point Commands Module
Enables the users to display their own points with `!points` command, gamble their points with `!roulette` and allows the author and the broadcaster to gift points to users with the `!givepoints x user` command

#### Missions Module
Allows users to join missions created by the broadcaster. The winner of a specific missions is awarded with points. The broadcaster starts a mission with `!startmission missionname`

#### Points Genrator Module
Gives users 1 point every `x` second where `x` is decided by the broadcaster in the configurations file

#### Uptime Module
Displays how long the bot has been running for when recieving the `!uptime` command

#### Autism Module
Displays a semi-random level of 'autism' for a specific user with the `!autism user` command. If no user is specified it will target the sender.

#### Custom Commands Module
Allows the broadcaster to specify simple custom commands with a trigger command and a bot response in the custom/commands.py file

#### Duel Module
Users can challenge eachother to duels using the `!duel user amount` command and accept or decline the duel with `!accept` and `!decline` The winner of each duel is announced instantly and is random.

#### Time Out Module
Allows users to time eachother out for a specified amount of time and a cost of points. Users can be protected such as mods and the broadcaster in the configuration file. These users can't be time out regardless but users who attempt to time them out won't be charged points if they exist in the protected users list. The command to buy a time out is `!buytimeout target_user`

## Missions

Missions can be activated by the broadcaster and the user(s) to fulfill the requirements for the mission will be awarded points upon ending.

#### Emote Mission
The bot will announce a random emote in the chat. The first user to type the same emote in the chat wins.
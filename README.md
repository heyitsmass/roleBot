# roleBot

## ~~Invite this bot your server!~~

## As of December 2022, Discord has implemented features that render this bot obsolete

roleBot is an open-source role management bot for discord community servers! 

roleBot autogathers any role below it's own rank, ignoring user exclusions and displays them as a clickable button for users to assign or remove themselves. Any role ranked above the bot in the server settings cannot is not assignable.

## /exclude 
### Administrator only! Red is already excluded, Green can be excluded.
![img](https://i.gyazo.com/2447030ba54174175bd46b608c0f61b1.png)

## /roles 
### Non-Administrator invocation! Red is removable, Green is assignable, Grey is excluded.
![img](https://i.gyazo.com/c367f9c1abee9415e884104acef2e021.png)

### Administrator invocation! All roles are assignable!
![img](https://i.gyazo.com/f257d66f3ec155d44f1ed092d328cd8b.png)


### Purpose: 

Some community servers may have multiple 'display' roles for users who want to join specific channels, or include themselves in certain groups, but exlude themselves from others. For instance, Servers with multiple game channels may have a role for First Person Shooter (FPS) oriented players, Massive Multiplayer Online (MMO) focus gamers, Board and Card game enthusients, and many more. 

roleBot gives server users the ability to do this, without incurring extensive overhead, or making itself known to other members. All messages are sent ephermerally to notify only the user invoking the command. This creates an overall lightweight design with only two commands, Recording no actual messages and logging no user data other than excluded role id's. Privacy is integral for a bot with role management access.

### Example: 

```python 

# all available server roles 
server_role_names = [
    "FPS Player", 
    "MMO Gamer", 
    "Card Enthusiant", 
    "Board Gamer",
    "Super Secret Role",
    "roleBot",
    "@everyone", 
    "moderator", 
    "administrator" 
 } 
 
 # user defined exclusions
 exclusion_names = [ 
    "Super Secret Role" 
 ]
 
 # roles gathered by the bot 
 available_roles = [ 
    "FPS Player", 
    "MMO Gamer", 
    "Card Enthusiant", 
    "Board Gamer"
 ] 
 ```

## Installation instructions

If you would like to use this bot personally, feel free to download the source 

### Linux (Ubuntu) & MacOS 

    pip3 -m install discord 
    
    git clone https://github.com/heyitsmass/roleBot 
    
    cd roleBot 
    
    mkdir database requirements 
    
    python3 bot.py -t <discord_API_token> 
    

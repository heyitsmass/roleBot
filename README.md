# roleBot
roleBot is an open-source role management bot for discord community servers! 

roleBot autogathers any role below it's own rank, ignoring user exclusions and displays them as a clickable button for users to assign or remove themselves. 

![img](https://i.imgur.com/0d1CukD.png)

### Purpose: 

Some community servers may have multiple 'display' roles for users who want to join specific channels, or include themselves in certain groups, but exlude themselves from others. For instance, Servers with multiple game channels may have a role for First Person Shooter (FPS) oriented players, Massive Multiplayer Online (MMO) focus gamers, Board and Card game enthusients, and many more. 

roleBot gives server users the ability to do this, without incurring extensive overhead, or making itself known to other members. All messages are sent ephermerally to notify only the user invoking the command. This creates an overall lightweight design with only two commands, Recording no actual messages and logging no user data other than excluded role id's. Privacy is integral for a bot with role management access.

### Example: 

```python 

# all available server roles 
server_role_names = [
    "lower 1" 
    "lower 2" 
    "lower 3" 
    "lower 4" 
    "roleBot"
    "@everyone" 
    "moderator" 
    "administrator" 
 } 
 
 # user defined exclusions
 exclusion_names = [ 
    "lower 2" 
 ]
 
 # roles gathered by the bot 
 available_roles = [ 
     "lower 1" 
     "lower 3" 
     "lower 4" 
 ] 
 ```

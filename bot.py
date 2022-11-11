from config import Token, Database
import discord 
from discord.ext import commands 
import os 
import json 

import argparse 

parser = argparse.ArgumentParser(
  prog = "roleBot", 
  description= "Lightweight 'display' role manager for Discord." 
)
parser.add_argument(
  '-t', '--token', action='store', required=False
)
args = parser.parse_args()

if args.token: 
  token = Token(args.token) 
else: 
  token = Token() 
class cBot(commands.Bot): 
  async def on_ready(self): 
    await self.tree.sync()
    await self.change_presence(
      activity = discord.Activity(
        type=discord.ActivityType.listening, 
        name="/roles to set roles!"
        )
      )
    print(f'Logged in as {self.user}')
  
  async def on_guild_join(self, guild:discord.Guild): 
    print(f'Joined {guild.name}')
    if not os.path.isdir('database'): 
      raise RuntimeError(f'Missing database directory.') 
    loc = f'database/{guild.id}.json'
    db = {} 
    db['exclusions'] = []
    json.dump(db, open(loc, 'x')) 
    print(f'created db @ {loc}')

class _Button(discord.ui.Button):
  def __init__(self, role:discord.Role, remove:bool=False, exclude:bool=False, **args): 
    self.role = role 
    self.remove = remove
    self.role_name = role.name
    self.role_id = role.id 
    self.exclude = exclude  

    if self.remove: 
      args['style'] = discord.ButtonStyle.red
    else: 
      args['style'] = discord.ButtonStyle.green

    if 'disabled' in args.keys(): 
      args['style'] = discord.ButtonStyle.grey

    super().__init__(**args) 

  async def callback(self, inter:discord.Interaction):
    if self.exclude: 
      db:dict = Database(inter.guild_id) 
      if self.remove:
        self.remove = False 
        db['exclusions'].remove(self.role_id) 
        content = f'{self.role_name} was removed from the exclusions list'
        self.style = discord.ButtonStyle.green 
      else: 
        self.remove = True 
        db['exclusions'].append(self.role_id) 
        content = f'{self.role_name} was added to the exclusions list'
        self.style = discord.ButtonStyle.red 
      
      await inter.response.edit_message(content=content, view=super().view) 
    else: 
      if not self.remove: 
        self.remove = True 
        self.style = discord.ButtonStyle.red 
        content = f'You were added to {self.role.name}'
        await inter.user.add_roles(self.role) 
      else: 
        self.remove = False 
        self.style = discord.ButtonStyle.green
        content = f'You were removed from {self.role.name}' 
        await inter.user.remove_roles(self.role) 
    
      await inter.response.edit_message(content=content, view=super().view)

intents = discord.Intents.default() 
intents.message_content = True 
intents.reactions = True 
intents.members = True 

bot = cBot(intents=intents, command_prefix='$')

@bot.tree.command(description='Display roles available for assignment or removal.') 
async def roles(inter:discord.Interaction):
  # Displays a list of assignable roles. 
  db = Database(inter.guild_id, mode='r')
  exclusions = db['exclusions']
  self = inter.guild.get_member(bot.user.id)
  user_role_ids = list(role.id for role in inter.user.roles) 

  view = discord.ui.View()
  #button = rButton(inter.user.roles[0], False, label="hello")
  for role in inter.guild.roles: 
    if role == self.top_role: 
      # roles above this are not assignable by the bot.
      # we can consider adding any roles at or above this unassignable and could add a disabled button
      break   
    elif role.name == '@everyone': 
      # everyone is already assigned to this role.
      continue 
    
    if role.id not in exclusions or inter.user.guild_permissions.administrator: 
      #role is assignable 
      #check if the user is assigned to the role 
      if role.id in user_role_ids: 
        #user is already assigned to the role, switch the button type to remove
        view.add_item(_Button(role, True, label=role.name)) 
      else:  
        #user is not assigned to the sole, switch the button type to assign 
        view.add_item(_Button(role, label=role.name)) 
        
    else: 
      #disable the button entirely. 
      view.add_item(_Button(role, label=role.name, disabled=True)) 

  
  await inter.response.send_message(content="Available roles", view=view, ephemeral=True) 
  
@bot.tree.command(description="Exclude roles from list.") 
async def exclude(inter:discord.Interaction, role_name:str):
  if not inter.user.guild_permissions.administrator: 
    await inter.response.send_message(content="*You do not have permission to execute this command. Contact the server owner.*", ephemeral=True)
    return 
  role = next(filter(lambda i: i.name.lower() == role_name.lower(), inter.guild.roles), None )
  
  db:list = Database(inter.guild_id) 
  if role.id not in db['exclusions']: 
    db['exclusions'].append(role.id)
    _str = f'{role.name} added to exclusions.'  
  else: 
    db['exclusions'].remove(role.id) 
    _str = f'{role.name} removed from exclusions.' 

  await inter.response.send_message(content=_str, ephemeral=True) 

bot.run(token) 



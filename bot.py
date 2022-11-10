from config import Token, Database
from typing import Awaitable
import discord 
from discord.ext import commands 

class myClient(commands.Bot): 
  async def on_ready(self):
    await self.tree.sync()
    print(f'Logged in as {self.user}')
    game = discord.Activity(name="/roles to set roles!", type=3)
    await self.change_presence(status = discord.Status.online, activity=game)

  async def on_guild_join(self, guild:discord.Guild): 
    Database(guild.id) 


class roleButton(discord.ui.Button): 
  def __init__(self, role:discord.Role, func:Awaitable[discord.Role], _emoji:str='💀', remove=False): 
    super().__init__(label=role.name, style=discord.ButtonStyle.green)
    self.role = role 
    self.func = func 
    self.remove = remove
  
  async def callback(self, interaction:discord.Interaction): 
    await self.func(self.role) 
    super().view.remove_item(self) 

    if super().view.children: 
      _str = 'assigned to'
      if not self.remove: 
        _str = 'removed to'
      await interaction.response.edit_message(content=f'You were {_str} {self.role.name}', view=super().view) 

    else:
      _str = 'removed' 
      if not self.remove: 
        _str = 'assigned'
       
      await interaction.response.edit_message(content=f'You\'ve been {_str} from all available roles!', view=super().view)

intents = discord.Intents.default() 
intents.message_content = True 
intents.reactions = True 
intents.members = True 

bot = myClient(intents=intents, command_prefix='$') 

@bot.tree.command(description='Display roles available for assignment or removal.') 
async def roles(inter:discord.Interaction):
  # Displays a list of assignable roles. 
  db = Database(inter.guild_id)
  exclusions = db['exclusions']
  user = inter.guild.get_member(bot.user.id)
  user_role_ids = list(role.id for role in inter.user.roles) 

  view = discord.ui.View()
  #button = rButton(inter.user.roles[0], False, label="hello")
  for role in inter.guild.roles: 
    if role == user.top_role: 
      # roles above this are not assignable by the bot.
      # we can consider adding any roles at or above this unassignable and could add a disabled button
      break 
    elif role.name == '@everyone': 
      # everyone is already assigned to this role.
      continue 
  
    if role.id not in exclusions: 
      #role is assignable 
      #check if the user is assigned to the role 
      if role.id in user_role_ids: 
        #user is already assigned to the role, switch the button type to remove
        view.add_item(rButton(role, True, label=role.name)) 
      else:  
        #user is not assigned to the sole, switch the button type to assign 
        view.add_item(rButton(role, label=role.name)) 
        
    else: 
      #disable the button entirely. 
      view.add_item(rButton(role, label=role.name, disabled=True))
  
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

bot.run(Token()) 



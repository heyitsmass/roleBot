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

@bot.tree.command(name='roles', description='Display roles available for assignment.') 
async def _assign(interaction:discord.Interaction):
  db = Database(interaction.guild_id) 

  if db['emoji_links'].keys(): 

    ids = list(r.id for r in interaction.user.roles) 
    view = discord.ui.View()

    for emoji in db['emoji_links']: 
      if db['emoji_links'][emoji] not in ids: 
        role = interaction.guild.get_role(db['emoji_links'][emoji])
        button = roleButton(role, interaction.user.add_roles)
        view.add_item(button) 
  
    if view.children: 
      await interaction.response.send_message(view=view, ephemeral=True) 
    else: 
      await interaction.response.send_message(content="You've been assigned to all available roles!", ephemeral=True)
  else: 
    await interaction.response.send_message(content="There exist no assignable roles.", ephemeral=True) 

@bot.tree.command(name='remove', description='Display roles you can be removed from.') 
async def _remove(interaction:discord.Interaction): 
  db = Database(interaction.guild_id) 

  if db['emoji_links'].keys(): 
    ids = list(r.id for r in interaction.user.roles) 
    view = discord.ui.View() 

    for emoji in db['emoji_links']: 
      if db['emoji_links'][emoji] in ids: 
        role = interaction.guild.get_role(db['emoji_links'][emoji]) 
        button = roleButton(role, interaction.user.remove_roles, remove=True) 
        view.add_item(button) 
      
    if view.children: 
      await interaction.response.send_message(view=view, ephemeral=True) 
    else: 
      await interaction.response.send_message(content="You're not assigned to any roles.", ephemeral=True)

  else: 
    # no emoji links 
    await interaction.response.send_message(content="There exist no removable roles.", ephemeral=True) 

@bot.tree.command(name='assign', description='Link an emoji to a role.') 
async def _assign(interaction:discord.Interaction, emoji:str, role_name:str): 
  db = Database(interaction.guild_id) 
  ids = db['emoji_links'].values() 

  if emoji not in db['emoji_links'].keys(): 
    #emoji can be linked 
    found = False 
    for r in interaction.guild.roles: 
      if r.name.lower() == role_name.lower(): 
        found = True 
        if r.id in ids: 
          await interaction.response.send_message('Role is assigned to another emoji.', ephemeral=True)
        else: 
          db['emoji_links'][emoji] = r.id 
          await interaction.response.send_message(f'{r.name} linked to {emoji}', ephemeral=True)
        break 
    
    if not found: 
        await interaction.response.send_message(f'{role_name} does not exist in this guild.', ephemeral=True)

  else: 
    #emoji linked to another role
    role = interaction.guild.get_role(db['emoji_links'][emoji]) 
    await interaction.response.send_message(f'{emoji} is already linked to {role.name}', ephemeral=True)

@bot.tree.command(name='reassign', description='Relink a role to a new emoji.') 
async def _reassign(interaction:discord.Interaction, role_name:str, emoji_new:str): 
  role = next(filter(lambda i: i.name.lower() == role_name.lower(), interaction.guild.roles), None )

  if role: 
    db = Database(interaction.guild_id) 
    for emoji in db['emoji_links']: 
      if db['emoji_links'][emoji] == role.id: 
        del db['emoji_links'][emoji] 
        break 

    db['emoji_links'][emoji_new] = role.id 
    await interaction.response.send_message(f'{role.name} reassigned to {emoji_new}.', ephemeral=True) 

  else: 
    await interaction.response.send_message(f'{role_name} is not a role.', ephemeral=True) 
  
bot.run(Token()) 



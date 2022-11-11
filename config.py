import os 
import json 
import time 

class MissingSecretTokenError(Exception): 
  def __init__(self, loc:str=''): 
    self.loc = loc 

  def __str__(self): 
    return f'\n\tInput a secret API token into \'{self.loc}\' or initialize with Token(\'<secret>\')'
class Token(str): 
  def __new__(self, token:str=''):
    loc, mode = 'requirements/secret.token', 'r'
    if not os.path.isfile(loc): 
      mode = 'x' 
    else: 
      if token: 
        mode = 'w' 

    file = open(loc, mode) 

    if mode in ['x', 'w']: 
      with file: 
        file.write(token) 

    else: 
      token = file.read() 
      if not token: 
        raise MissingSecretTokenError(loc) 

    return super().__new__(self, token) 


class Database(dict): 
  def __init__(self, guild_id:int, mode:str='w'): 
    self.loc:str = f'database/{guild_id}.json'
    self.db:dict = json.load(open(self.loc, 'r')) 
    self.file = open(self.loc, mode)
    self.mode = mode 

  def __del__(self): 
    if self.mode == 'w': 
      json.dump(self.db, self.file) 
      print("Db closed.") 

  def __getitem__(self, __key): 
    return self.db[__key] 
  
  def __setitem__(self, __key, __value): 
    self.db[__key] = __value 
  
  def __delitem__(self, __key): 
    del self.db[__key] 

  def __repr__(self):
    return str(self.db) 

  def keys(self): 
    return self.db.keys() 
  
  def values(self): 
    return self.db.values() 

  def items(self): 
    return self.db.items()

  def get(self, __key): 
    return self.db.get(__key)  






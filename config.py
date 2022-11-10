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


class Database:
  '''
    Constructs and opens a database for guildID 

    Ensures database integrity.  

    Parameters: 
      guildID:int -> 
      
        The guild for the database being requested 

      mode:str = 'w' -> 

        The mode the database should be opened for, a fork of open() 

        
  ''' 
  def __init__(self, guildID:int, mode:str='w'): 
    self.guildID = guildID 
    self.dbLoc = f'dependencies/database/{guildID}.json'
    if not os.path.isfile(self.dbLoc): 
      self.dbFile = open(self.dbLoc, 'x')
      self.db = {} 
      self.db['emoji_links'] = {}  
    else: 
      self.db = json.load(open(self.dbLoc, 'r'))
      self.mode = mode 
      self.dbFile = open(self.dbLoc, mode) 

  def __del__(self): 
    if self.mode == 'w': 
      json.dump(self.db, self.dbFile) 
    
    self.dbFile.close() 
  
  def __getitem__(self, key): 
    return self.db[key]

  def __setitem__(self, key, value): 
    self.db[key] = value 

  def __delitem__(self, key): 
    del self.db[key] 

  def keys(self): 
    return self.db.keys() 
  
  def values(self): 
    return self.db.values()





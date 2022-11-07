import os 
import json 
import time 

class MissingTokenError(Exception): 
  def __str__(self): 
    return f'Enter secret API token into \'dependencies/token/secret.token\''

class Token(str): 
  '''
    Gathers a token from the dependency file. 

    Creates a token file if unavailable. 

    Location: dependencies/token/secret.token

    Parameters: 
      token:str
        -> Optional, Token to be written to new file.

        -> Ignored if the file already exists or not provided. 
  '''
  def __init__(self, token:str=''): 
    self.__loc = 'dependencies/token/secret.token' 
    self.__token = token 
    if not os.path.isfile(self.__loc): 
      file = open(self.__loc, 'x')
      if self.__token: 
        file.write(self.__token)
        file.close() 
      else: 
        raise MissingTokenError
    else: 
      self.__token = open(self.__loc, 'r').read()
      if not self.__token: 
        raise MissingTokenError
      
  def __str__(self): 
    return self.__token 


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





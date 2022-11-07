import os 

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







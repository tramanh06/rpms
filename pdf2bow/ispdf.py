import re
import subprocess as sp

def ispdf(fileName):
  """ Check if file is a pdf or not 
      Requires the file command
  """ 

  cmd = "file" # -kb ", fileName)
  flags = "-kb"
  arg  = fileName

  # Call `file fileName`
  proc = sp.Popen([cmd, flags, arg], stdout=sp.PIPE)
  proc.wait()
  result = proc.stdout.readline()

  if re.match('[ ]*PDF', result):
    return True

  return False


if __name__ == "__main__":
    ispdf()

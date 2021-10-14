import os

def clear():
    command = 'clear'
    if os.name in ('nt','dos'):
        command='cls'
    os.system(command)


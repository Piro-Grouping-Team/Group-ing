import itertools
import random

def groupCodeGenerate(username, groupId):
    code = ''
    nameLength = len(username)
    randomNames = list(itertools.permutations(username,nameLength))
    randomName = random.choice(randomNames)    
    for alphabet in randomName:
        code += format(ord(alphabet), 'x')
    code += format(groupId, 'x')
    return code

import shortuuid

def groupCodeGenerate():
    code = shortuuid.uuid()
    return code


# import itertools
# import random

# def groupCodeGenerate(username, groupId):
#     code = ''
#     randomNames = list(itertools.permutations(username, 5))
#     randomName = random.choice(randomNames)    
#     for alphabet in randomName:
#         code += format(ord(alphabet), 'x')
#     code += format(groupId, 'x')
#     return code

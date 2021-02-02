import re

madlibsFile = open('madlibs.txt')
madlibsContent = madlibsFile.read()
madlibsFile.close()
upperCaseWords  = re.findall('[A-Z][A-Z]+', madlibsContent)
vowels = ('a','e','i','o','u')

def construct_question(word, determiner):
    return f'Enter {determiner} {word.lower()} \n'

for word in upperCaseWords:
    replace = input(construct_question(word, 'an')) if word.lower().startswith(vowels) else input(construct_question(word, 'a'))
    madlibsContent = madlibsContent.replace(word, replace)

madlibsFile = open('madlibs.txt', 'w')
madlibsFile.write(madlibsContent)

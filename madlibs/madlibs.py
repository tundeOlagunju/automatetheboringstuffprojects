import re

madlibsFile = open('madlibs.txt')
madlibsContent = madlibsFile.read()
madlibsFile.close()
upperCaseWords  = re.findall('[A-Z][A-Z]+', madlibsContent)
vowels = ('a','e','i','o','u')

for word in upperCaseWords:
    replace = input(f'Enter an {word.lower()} \n') if word.lower().startswith(vowels) else input(f'Enter a {word.lower()} \n')
    madlibsContent = madlibsContent.replace(word, replace)

madlibsFile = open('madlibs.txt', 'w')
madlibsFile.write(madlibsContent)

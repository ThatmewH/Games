from passlib.hash import sha256_crypt
file = open("letters.txt", "r")
word = file.read()
word = word.replace("\n", "")

hashedWord = sha256_crypt.encrypt(word)
guessWord = input("Word: ")

print(sha256_crypt.verify(guessWord, hashedWord))

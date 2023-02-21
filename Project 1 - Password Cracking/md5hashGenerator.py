import hashlib

stringPwd = input("Enter a password to be hashed: ")
pwdH = hashlib.md5(stringPwd.encode())
pwdHash = pwdH.hexdigest()

print("MD5 hash of the password is: "+pwdHash)        
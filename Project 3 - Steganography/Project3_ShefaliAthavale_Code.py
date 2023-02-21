
import binascii
import re
import os
import hashlib


## Function to embed secret message in JPEG File
def embed(carrierFile,message):

    # Open carrier file and read it's contents
    with open(carrierFile, 'rb') as f:
        content = f.read()
        f.close()

    # Find the EOF offset for the JPEG file and retrieve contents of the image upto EOF offset
    eof_list_jpeg = [match.start() for match in re.finditer(re.escape(b'\xFF\xD9'),content)]  
    eofImage = eof_list_jpeg[-1]
    hexcontent = binascii.hexlify(content[:eofImage])   

    # Convert text message into bytes and add it to the original image content
    # We add 4 additional bytes of data before appending the secret message 
    # for better retrieval of the secret message from the file  
    msg = message.encode('utf-8')
    msg = binascii.hexlify(msg).decode('utf-8')
    dataMsg = bytes(msg, 'utf-8')   
    hexcontent += b'ffffffff'+dataMsg + b'ffd9'
    data = bytes.fromhex(hexcontent.decode("utf-8"))
    
    # Retrieve original carrier file name 
    extension = ''.join(carrierFile.split(".")[-1])
    filename = carrierFile.split(".")[:-1]
    
    # Write the contents to the new file 
    embedFile = filename[0]+'_modified.'+extension
    with open(embedFile, 'wb') as f1:
        f1.write(data)
        f1.close()

    # Output details about Original and Modified Carrier File to the screen
    print()
    print("Original Carrier File Details:")
    print("File Name: "+carrierFile)
    print("Size: "+str(os.path.getsize(carrierFile)/1000)+" KB")
    md5Hash = hashlib.md5(content).hexdigest()
    print("MD5 Hash: "+md5Hash)
    print()
    print("Modified Carrier File Details:")
    print("File Name: "+embedFile)
    print("Size: "+str(os.path.getsize(embedFile)/1000)+" KB")
    md5Hash1 = hashlib.md5(data).hexdigest()
    print("MD5 Hash: "+md5Hash1)



## Function to extract secret message from a JPEG File
def extract(embeddedFile):

    # Open carrier file and read it's contents
    with open(embeddedFile, 'rb') as f:
        content = f.read()
        f.close()
    
    # Find the EOF offset for the JPEG file and retrieve contents of the image upto EOF offset
    eof_list_jpeg = [match.start() for match in re.finditer(re.escape(b'\xFF\xD9'),content)] 
    # Find the offset of the start of 4 additional bytes of data
    eof_list_space = [match.start()+4 for match in re.finditer(re.escape(b'\xFF\xFF\xFF\xFF'),content)]
    eofImage = eof_list_jpeg[-1]
    eofSpace = eof_list_space[-1]
    # Secret Message is the message between 4 additional bytes of data and EOF offset for JPEG image
    secMsg = content[eofSpace:eofImage].decode('utf-8')  

    return secMsg
   


if __name__ == "__main__":
    print()
    print("1: Embed a message in a file")
    print("2: Extract a message from a file")

    method = input("Enter your choice: ")
    if method == "1":
        filename = input("Enter name of the carrier file: ")
        message = input("Enter message to embed: ")
        embed(filename, message)
        print()
        print("Embedded secret message is: "+message)
        print()

    elif method=="2":
        filename = input("Enter name of the carrier file: ")
        secretMessage = extract(filename)
        print()
        print("Extracted secret message is: "+secretMessage)
        print()






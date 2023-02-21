

## File Signatures of PNG, JPEG/JPG and PDF files

# PNG: 89 50 4E 47 0D 0A 1A 0A - 49 45 4E 44 AE 42 60 82

# JPEG/JPG: FF D8 - FF D9

# PDF: 25 50 44 46 - 
# 0A 25 25 45 4F 46 (.%%EOF)
# 0A 25 25 45 4F 46 0A (.%%EOF.)
# 0D 0A 25 25 45 4F 46 0D 0A (..%%EOF..)
# 0D 25 25 45 4F 46 0D (.%%EOF.)


import sys
import re
import os
import hashlib

md5Hashes = []

os.makedirs('Athavale',exist_ok=True)
## Function to carve file and save individual files
def carveFile(sof,eof,subdata,c,type):
    fileName = 'carved_'+str(c)+'.'+str(type)
    fcarve = open(fileName, 'wb')
    fcarve.write(subdata)
    fcarve.close()
    print("Created file "+fileName)
    print("File Type is: "+type)
    print("Start of File is: "+str(sof))
    print("End of File is: "+str(eof))
    print("File Size is: "+str(os.path.getsize(fileName)/1000)+" KB")
    with open(fileName,'rb') as f:
        data = f.read()
        md5Hash = hashlib.md5(data).hexdigest()
        print("MD5 Hash of the file "+fileName+ " is: "+str(md5Hash))
        md5Hashes.append(md5Hash)
    print()


## Start of File and End of File for JPEG/JPG, PNG, PDF stored in dictionary
sof_dict = {'jpeg':b'\xFF\xD8\xFF\xE0','jpeg1':b'\xFF\xD8\xFF\xE1','png':b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A','pdf':b'\x25\x50\x44\x46'}
eof_dict = {'jpeg':b'\xFF\xD9\x00','jpeg1':b'\xFF\xD9\xFF','jpeg2':b'\xFF\xD9\x20','png':b'\x49\x45\x4E\x44\xAE\x42\x60\x82','pdf':b'\x0A\x25\x25\x45\x4F\x46','pdf1':b'\x0A\x25\x25\x45\x4F\x46\x0A','pdf2':b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A', 'pdf3':b'\x0D\x25\x25\x45\x4F\x46\x0D'}


## File name of the file to be carved
fname = str(sys.argv[1])
fname_obj = open(fname, 'rb')
data = fname_obj.read()
fname_obj.close()


## List of Start of File and End of File offsets for JPEG/JPG Images
sof_list_jpeg=[match.start() for match in re.finditer(re.escape(sof_dict['jpeg']),data)]
# sof_list_jpeg.extend(match.start() for match in re.finditer(re.escape(sof_dict['jpeg1']),data))
# eof_list_jpeg=[match.start() for match in re.finditer(re.escape(eof_dict['jpeg']),data)]
eof_list_jpeg=[match.start()+2 for match in re.finditer(re.escape(eof_dict['jpeg']),data)]
eof_list_jpeg.extend(match.start()+2 for match in re.finditer(re.escape(eof_dict['jpeg1']),data))
eof_list_jpeg.extend(match.start()+2 for match in re.finditer(re.escape(eof_dict['jpeg2']),data))

## List of Start of File and End of File offsets for PNG Images
sof_list_png=[match.start() for match in re.finditer(re.escape(sof_dict['png']),data)]
# eof_list_png=[match.start() for match in re.finditer(re.escape(eof_dict['png']),data)]
eof_list_png=[match.start()+8 for match in re.finditer(re.escape(eof_dict['png']),data)]

## List of Start of File and End of File offsets for PDFs
sof_list_pdf=[match.start() for match in re.finditer(re.escape(sof_dict['pdf']),data)]
# eof_list_pdf=[match.start() for match in re.finditer(re.escape(eof_dict['pdf']),data)]
# eof_list_pdf.extend(match.start() for match in re.finditer(re.escape(eof_dict['pdf1']),data))
# eof_list_pdf.extend(match.start() for match in re.finditer(re.escape(eof_dict['pdf2']),data))
# eof_list_pdf.extend(match.start() for match in re.finditer(re.escape(eof_dict['pdf3']),data))
eof_list_pdf=[match.start()+6 for match in re.finditer(re.escape(eof_dict['pdf']),data)]
eof_list_pdf.extend(match.start()+7 for match in re.finditer(re.escape(eof_dict['pdf1']),data))
eof_list_pdf.extend(match.start()+9 for match in re.finditer(re.escape(eof_dict['pdf2']),data))
eof_list_pdf.extend(match.start()+7 for match in re.finditer(re.escape(eof_dict['pdf3']),data))


c = 0

os.chdir('Athavale')

## Loop to get the JPEG/JPG data from SOF and EOF offsets and send to carveFile function to carve the file 
for i in sof_list_jpeg:
    flag = 0
    for j in eof_list_jpeg:
        if i<j and flag==0:
            flag = 1
        # if i<j:    
            subdata = data[i:j]
            c+=1
            carveFile(i,j,subdata,c,'jpeg')

## Loop to get the PNG data from SOF and EOF offsets and send to carveFile function to carve the file     
for i in sof_list_png:
    flag = 0
    for j in eof_list_png:
        if i<j and flag==0:
            flag = 1
        # if i<j:
            subdata = data[i:j]
            c+=1
            carveFile(i,j,subdata,c,'png')

## Loop to get the PDF data from SOF and EOF offsets and send to carveFile function to carve the file 
for i in sof_list_pdf:
    flag = 0
    for j in eof_list_pdf:
        if i<j and flag==0:
            flag = 1
        # if i<j:
            subdata = data[i:j]
            c+=1
            carveFile(i,j,subdata,c,'pdf')


m = 1
with open('hashes.txt','w') as f:
    for hash in md5Hashes:
        f.write("carved_"+str(m)+" - "+hash)
        f.write("\n")
        m+=1
    f.close()

sys.exit()

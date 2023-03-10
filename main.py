import time
from pdf2image import convert_from_path
import numpy as np
import os
import fnmatch
from PIL import Image

#CONVERT PDFS TO PNG WITH WRITTEN WATERMARK

poppler_path =r"Release-22.04.0-0\poppler-22.04.0\Library\bin" # necessary
saving_folder=r"ThePlaceWhereThePicturesWillBeSaved"

dirpath=r"ThePlaceFromWherePDFSAreTaken"

print (len(fnmatch.filter(os.listdir(dirpath), '*.PDF')))
a=len(fnmatch.filter(os.listdir(dirpath), '*.PDF'))

last_item1=os.listdir("ThePlaceFromWherePDFSAreTaken")[a-1]
last_item1=last_item1[:-4]
last_item=int(last_item1)
print("last", last_item)

c = 1
number= os.listdir("ThePlaceFromWherePDFSAreTaken")[0]
number = number[:-4]
print(number)
num= int(number)
os.chdir("ThePlaceFromWherePDFSAreTaken")

if len(os.listdir(saving_folder)) == 0:
    print("Directory is empty")
else:
    for f in os.listdir(saving_folder):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join(saving_folder, f))
c=1
num= int(number)
while(num<=last_item):
        if(os.path.exists(f"ThePlaceFromWherePDFSAreTaken\{num}.PDF") == True):
                pdf_path=f"ThePlaceFromWherePDFSAreTaken\{num}.PDF" # For each file from the directory #
                pages = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)

                for page in pages:
                        img_name=f"{num}-{c}.png"
                        page.save(os.path.join(saving_folder,img_name),"PNG")
                        c+=1
                num+=1
                c=1
        else:
                num=num+1

#REMOVE THE WATERMARK FROM THE PNG

dirpath=r"ThePlaceWhereThePicturesAreSaved" # the folder path 

print (len(fnmatch.filter(os.listdir(dirpath), '*.png')))
a=len(fnmatch.filter(os.listdir(dirpath), '*.png')) # the number of png files from the folder

number= os.listdir("ThePlaceWhereThePicturesAreSaved")[0] # the name of the first element from the folder as a string
number = number[:-6] # cut to get the number of the file
#print(number)
num= int(number) #conversion to int
os.chdir("ThePlaceWhereThePicturesAreSaved") #select working folder
c=1


saving_folder=f"SavingFolderForEditedPicturedWithTheWatermarkRemoved"

last_item1=os.listdir("ThePlaceWhereThePicturesAreSaved")[a-1]
last_item1=last_item1[:-6]
last_item=int(last_item1)

print(last_item)

if len(os.listdir(saving_folder)) == 0:
    print("Directory is empty")
else:
    for f in os.listdir(saving_folder):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join(saving_folder, f))
c=1
num= int(number)

while(num<=last_item): #for each file
    while(os.path.exists(f"{num}-{c}.png") == True): #while the file exists
        im = Image.open(f"{num}-{c}.png") #open file
        data = np.array(im) #create the array
        # initial value
        r1, g1, b1 = 178, 178, 178 #set the color
        # the final value
        r2, g2, b2 = 255, 255, 255
        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2] #set rgb
        mask = (red == r1) & (green == g1) & (blue == b1) #set mask
        data[:, :, :3][mask] = [r2, g2, b2] #first mask
        n = 179
        while n <= 255: #applying masks from the second step to the last one
                 mask = (red == n) & (green == n) & (blue == n)
                 data[:, :, :3][mask] = [r2, g2, b2]
                 im = Image.fromarray(data) #save the object image
                 n = n + 1 #increment n

        im.save(f'SavingFolderForEditedPicturedWithTheWatermarkRemoved\{num}-{c}_mod.png') #save the image
        c+=1 #increment c
        print(num)
    num+=1 #increment num so it goes to the next file
    c=1 # set c to 1



#CONVERT PNG FILES TO PDF

dirpath=r"SavingFolderForEditedPicturedWithTheWatermarkRemoved"
image_list = []
print(dirpath)
a=len(fnmatch.filter(os.listdir(dirpath), '*.png'))
print(a)
number= os.listdir("SavingFolderForEditedPicturedWithTheWatermarkRemoved")[0]
number = number[:-10]
num= int(number)
print(num)

last_item1=os.listdir("SavingFolderForEditedPicturedWithTheWatermarkRemoved")[a-1]
last_item1=last_item1[:-10]
last_item=int(last_item1)
print(last_item)

os.chdir("SavingFolderForEditedPicturedWithTheWatermarkRemoved")
c=1
i=0

#last_item check

saving_folder=f'TheFolderWithTheFilesWithoutWatermark'

if len(os.listdir(saving_folder)) == 0:
    print("Directory is empty")
else:
        for f in os.listdir(saving_folder):
                if not f.endswith(".pdf"):
                        continue
                os.remove(os.path.join(saving_folder, f))
c=1
num= int(number)

while(num<=last_item):

    if(os.path.exists(f"{num}-{c}_mod.png") == True):
        imageOne=Image.open(f'SavingFolderForEditedPicturedWithTheWatermarkRemoved\{num}-{c}_mod.png')
        imgOne=imageOne.convert('RGB')
        #image_list.insert(i, imgOne)
        c+=1
        i+=1

        while(os.path.exists(f"{num}-{c}_mod.png") == True):
                image = Image.open(f'SavingFolderForEditedPicturedWithTheWatermarkRemoved\{num}-{c}_mod.png')
                print(f"{num}-{c}_mod.png")
                img=image.convert('RGB')
                image_list.insert(i,img)
                c+=1
                i+=1
        imgOne.save(f'TheFolderWithTheFilesWithoutWatermark\{num}.pdf', save_all=True, append_images=image_list)
        image_list = []
        c = 1
        i = 0
        num += 1
    else:
        num+=1


#PRINTING PDF FILES
#Print files with the defauld printer

dirpath=r"TheFolderWithTheFilesWithoutWatermark"

#print (len(fnmatch.filter(os.listdir(dirpath), '*.pdf')))
a=len(fnmatch.filter(os.listdir(dirpath), '*.Pdf'))

number= os.listdir(r"TheFolderWithTheFilesWithoutWatermark")[0]
number = number[:-4]
#print(number)
num= int(number)

last_item1=os.listdir("TheFolderWithTheFilesWithoutWatermark")[a-1]
print(last_item1)
last_item1=last_item1[:-4]
last_item=int(last_item1)
print(last_item)

os.chdir(r"TheFolderWithTheFilesWithoutWatermark")
c=1

while(num<=last_item):

        if(os.path.exists(f"{num}.PDF") == True):
            os.startfile(f"{num}.pdf", "print")
            print(f"{num}.PDF")
            time.sleep(10)
            num+=1
        else:
            num+=1
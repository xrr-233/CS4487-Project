import os
import random
import shutil

#say that we start from putting 'original' and 'manipulated' folders in './dataset'. 
#Let's randomly split the images from the two folders into three sets and put them into seperate folders.

def record_data(folder_path):
   alldata = []
   for path, subdirs, files in os.walk(folder_path):   #the folder where you put images
      for filename in files:
        f = os.path.join(path, filename)
        alldata.append(f)
   
   print(len(alldata))
   
   alldataset = set(range(len(alldata)))
   train = set(random.sample(alldataset, int(float(len(alldata))*0.8)))   #pick out 12000*80% of all data for training
   temp = alldataset - train #use set operation to do segmentation, producing mutually exclusive sets
   val = set(random.sample(temp, int(float(len(list(temp))*0.5))))   #50 percent of remaining data as val, other 50% as test
   test = temp-val
   train = list(train)
   val = list(val)
   test = list(test)
   
   train_file, val_file, test_file=[],[],[]
   for i in train:
      train_file.append(alldata[i])
   for i in val:
      val_file.append(alldata[i])
   for i in test:
      test_file.append(alldata[i])
   
   with open("train.txt", "w") as TRA: #produce txt file, written with the path of selected images
       for x in train_file:
           TRA.write(x + "\n")
   TRA.close()
   with open("val.txt", "w") as VA:
       for x in val_file:
           VA.write(x + "\n")
   VA.close()
   with open("test.txt", "w") as TES:
       for x in test_file:
           TES.write(x + "\n")
   TES.close()

record_data('./dataset')




def mkdir(path): #create folers to put the three sets of images
    # os.path.exists check if folder exists
    folder = os.path.exists(path)

    if not folder:
        # check if folder exist and decide whether to create or report an error
        os.makedirs(path)
        print('folder created：', path)

    else:
        print('folder existed：', path)

train_folder = "./dataset/train"
val_folder = "./dataset/val"
test_folder = "./dataset/test"
mkdir(test_folder)
mkdir(train_folder)
mkdir(val_folder)

mkdir(train_folder+'/0_real')
mkdir(val_folder+'/0_real')
mkdir(test_folder+'/0_real')
mkdir(train_folder+'/1_fake')
mkdir(val_folder+'/1_fake')
mkdir(test_folder+'/1_fake')
#in each folder we will put them into 0_real and 1_fake subfolder


def read_move(dirfile, target_dir): #move the images to the three new folders:
    f = open(dirfile)
    for line in f:
        line = line.replace("\\","/")
        line2 = line.replace("\n","")
        if 'manipulated' in line:
           shutil.move(line2,target_dir+'/1_fake')
        else:
           shutil.move(line2,target_dir+'/0_real')

read_move("train.txt",train_folder)
read_move("val.txt",val_folder)
read_move("test.txt",test_folder)




shutil.rmtree('./dataset/manipulated')#delete the two unuseful empty folders
shutil.rmtree('./dataset/original') 




def record_data_again(folder_path,txt_name):#produce txt files, written the path of newly distributed images.
   alldata = []
   for path, subdirs, files in os.walk(folder_path):   #the folder where you put sets of images
      for filename in files:
        f = os.path.join(path, filename)
        #print(f)
        alldata.append(f)
   
   with open(txt_name+".txt", "w") as Writefile: #produce a txt file, written with the path of images in the set
       for x in alldata:
           x = x.replace("\\","/")
           Writefile.write(x + "\n")
   Writefile.close()

record_data_again('./dataset/train','train')
record_data_again('./dataset/test','test')
record_data_again('./dataset/val','val')

print('finally we get the three folders with real/fake images seperated, and three txt files written with the path of these images.(txt in main path)')
#finally we get the three folders with real/fake images seperated, and three txt files written with the path of these images.(txt in main path)

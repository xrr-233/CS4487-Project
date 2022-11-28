import os
import random
import shutil

#say that we start from putting the unzipped 'original' and 'manipulated' folders in './dataset'. 
#Let's randomly split the images from the two folders into three sets and put them into seperate folders.

#learn from the datasets we know that there are 6 types of deepfakes in the "manipulated" images:
#1.DF 2.eyes 3.F2F 4.FS 5.mouth 6.NT

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
            
def read_move(dirfile, target_dir): #move the images to the new folders:
    f = open(dirfile)
    for line in f:
        line = line.replace("\n","")
        if 'manipulated' in line:
            shutil.move(line,target_dir+'/1_fake')
        else:
            shutil.move(line,target_dir+'/0_real')        
        
        
def record_data(folder_path):#the folder where you put images
    #the order of this list is count_DF, count_eyes, count_F2F, count_FS, count_mouth, count_NT
    count_classes_name = list(['DF','eyes','F2F','FS','mouth','NT'])
    count_classes = list([0,0,0,0,0,0])
    filenames_classes = list([list(),list(),list(),list(),list(),list()])
    classes_sets = list([None,None,None,None,None,None])
    #variables for later set operations. The reason to use set operation is to create
    #mutually exclusive sets of images. Six elements means the six types of manipulation. Sorry it's messy here
        
    
    alldata_real = []
    alldata_fake = []
    for path, subdirs, files in os.walk(folder_path):   
        for filename in files:
            f = os.path.join(path, filename)
            if "manipulated" in f:
                alldata_fake.append(f)
            elif "original" in f:
                alldata_real.append(f)
    print(len(alldata_fake))
    print(len(alldata_real))
   
    
   
    for data in alldata_fake:
        if "DF" in data:
            count_classes[0] += 1
            filenames_classes[0].append(data)
        elif "eyes" in data:
            count_classes[1] += 1
            filenames_classes[1].append(data)
        elif "F2F" in data:
            count_classes[2] += 1
            filenames_classes[2].append(data)
        elif "FS" in data:
            count_classes[3] += 1
            filenames_classes[3].append(data)
        elif "mouth" in data:
            count_classes[4] += 1
            filenames_classes[4].append(data)
        elif "NT" in data:
            count_classes[5] += 1  
            filenames_classes[5].append(data)


    alldataset_real = set(range(len(alldata_real)))
    #turn the dataset into type "set" for further operation.
   
    len_real_train = list([0,0,0,0,0,0])
    len_real_val = list([0,0,0,0,0,0])
    len_real_test = list([0,0,0,0,0,0])
   
   
   
   
   
    for k in range(len(count_classes)):
        if k == 0:
            fromallreal = set(random.sample(alldataset_real, int(float((len(alldata_real)*(count_classes[k]/len(alldata_fake))))))) 
            classes_sets[k]=fromallreal       
        elif k < len(count_classes)-1:
            fromallreal = set(alldataset_real)
            othersetlength = 0
            for kk in range(k):
                fromallreal = fromallreal-classes_sets[kk] 
                othersetlength += count_classes[kk]
            fromallreal = set(random.sample(fromallreal, int(float((len(fromallreal)*(count_classes[k]/(len(alldata_fake)-othersetlength)))))))
            classes_sets[k]=fromallreal
        else:
            fromallreal = set(alldataset_real)
            othersetlength = 0
            for kk in range(k):
                fromallreal = fromallreal-classes_sets[kk] 
                othersetlength += count_classes[kk]
            classes_sets[k]=fromallreal            
        
        train = set(random.sample(fromallreal, int(float(len(list(fromallreal))*0.8))))        
        
        temp = fromallreal - train #use set operation to do segmentation, producing mutually exclusive sets
        val = set(random.sample(temp, int(float(len(list(temp))*0.5))))   #50 percent of remaining data as val, other 50% as test
        test = temp-val
        train = list(train)
        val = list(val)
        test = list(test)
        len_real_train[k] = len(train)
        len_real_val[k] = len(val)
        len_real_test[k] = len(test)
         
        
        #The idea for distributing real images is: we earlier get the proportion of each type of manipulation. We apply this proportion to pick out
        #a number of real images. Then add the real image and (this type of) fake image together to form a overall dataset (of this type).
        #lastly, apply 8:1:1 for train, val, test.
        #example: we have 1333 "DF" type of manipulated images over all 8000 manipulated images. The proportion is 1333/8000 ≈ 1/6.
        #Then we pick out 4000*1/6 ≈ 666 of real image to mix up with "DF" images to form a total set for studying consis 666+1333 = 1999 ≈ 1/6 of 12000.
        #Finally, apply 8:1:1 to train, val, test.         
        
        thisclassfake = set(range(len(filenames_classes[k])))
        trainfake = set(random.sample(thisclassfake, int(float(count_classes[k]*0.8))))  
        tempfake = thisclassfake - trainfake #use set operation to do segmentation, producing mutually exclusive sets
        valfake = set(random.sample(tempfake, int(float(len(list(tempfake))*0.5))))   #50 percent of remaining data as val, other 50% as test
        testfake = tempfake-valfake
        trainfake = list(trainfake)
        valfake = list(valfake)
        testfake = list(testfake)         


        train_file, val_file, test_file=[],[],[]
        for i in train:
            train_file.append(alldata_real[i])
        for i in val:
            val_file.append(alldata_real[i])
        for i in test:
            test_file.append(alldata_real[i])
            
            
        trainfake_file, valfake_file, testfake_file=[],[],[]
        for i in trainfake:
            trainfake_file.append(filenames_classes[k][i])
        for i in valfake:
            valfake_file.append(filenames_classes[k][i])        
        for i in testfake:
            testfake_file.append(filenames_classes[k][i])            
        
        path_train_real = train_folder+'/'+count_classes_name[k]+'/0_real'
        path_val_real = val_folder+'/'+count_classes_name[k]+'/0_real'
        path_test_real = test_folder+'/'+count_classes_name[k]+'/0_real'
        path_train_fake = train_folder+'/'+count_classes_name[k]+'/1_fake'
        path_val_fake = val_folder+'/'+count_classes_name[k]+'/1_fake'
        path_test_fake = test_folder+'/'+count_classes_name[k]+'/1_fake'        
        
        mkdir(path_train_real)
        mkdir(path_val_real)
        mkdir(path_test_real)
        mkdir(path_train_fake)
        mkdir(path_val_fake)
        mkdir(path_test_fake) 
            
        with open(train_folder+'/'+count_classes_name[k]+"/train_"+count_classes_name[k]+".txt", "w") as TRA: 
            #produce txt file, written with the path of selected images
            for x in train_file:
                x = x.replace("\\","/")
                x = x.replace("\n","")                
                TRA.write(x + "\n")
            for y in trainfake_file:
                y = y.replace("\\","/")
                y = y.replace("\n","")                
                TRA.write(y + "\n") 
        TRA.close()
        
        with open(val_folder+'/'+count_classes_name[k]+"/val_"+count_classes_name[k]+".txt", "w") as VA:
            for x in val_file:
                x = x.replace("\\","/")
                x = x.replace("\n","")
                VA.write(x + "\n")
            for y in valfake_file:
                y = y.replace("\\","/")
                y = y.replace("\n","")                 
                VA.write(y + "\n")          
        VA.close()
        
        with open(test_folder+'/'+count_classes_name[k]+"/test_"+count_classes_name[k]+".txt", "w") as TES:
            for x in test_file:
                x = x.replace("\\","/")
                x = x.replace("\n","")                
                TES.write(x + "\n")
            for y in testfake_file:
                y = y.replace("\\","/")
                y = y.replace("\n","")                 
                TES.write(y + "\n")           
        TES.close()   

                
        read_move(train_folder+'/'+count_classes_name[k]+"/train_"+count_classes_name[k]+".txt",train_folder+'/'+count_classes_name[k])
        print('finished moving train folder for _'+count_classes_name[k] + ' class')
        read_move(val_folder+'/'+count_classes_name[k]+"/val_"+count_classes_name[k]+".txt",val_folder+'/'+count_classes_name[k])
        print('finished moving val folder for _'+count_classes_name[k] + ' class')
        read_move(test_folder+'/'+count_classes_name[k]+"/test_"+count_classes_name[k]+".txt",test_folder+'/'+count_classes_name[k])
        print('finished moving test folder for _'+count_classes_name[k] + ' class')
        #move the images to the according folder.
        
        os.remove(train_folder+'/'+count_classes_name[k]+"/train_"+count_classes_name[k]+".txt")
        os.remove(val_folder+'/'+count_classes_name[k]+"/val_"+count_classes_name[k]+".txt")
        os.remove(test_folder+'/'+count_classes_name[k]+"/test_"+count_classes_name[k]+".txt")
   
record_data('./dataset')


shutil.rmtree('./dataset/manipulated')#delete the two empty folders
shutil.rmtree('./dataset/original') 




#finally write 3 txt files, including the path of the images used in each set. 
#by default written in main folder
def write_finaltxt(folder_path): #the main folder of all images
    trainpath = folder_path + '/train'
    valpath = folder_path + '/val'
    testpath = folder_path + '/test'
   
   
    traindata = []
    valdata = []
    testdata = []

   
    for path, subdirs, files in os.walk(trainpath):   #the folder where you put images
        for filename in files:
            f = os.path.join(path, filename) #don't use this line if you only want names, not path. Then change 'f' to 'filename'.
            traindata.append(f)
    with open("train.txt", "w") as TRA: 
         #produce txt file, written with the path of selected images
        for x in traindata:
            x = x.replace("\\","/")
            TRA.write(x + "\n") 
    TRA.close()
      
    for path, subdirs, files in os.walk(testpath):   
        for filename in files:
            f = os.path.join(path, filename)#don't use this line if you only want names, not path. Then change 'f' to 'filename'.
            testdata.append(f)
    with open("test.txt", "w") as TES: 
        for x in testdata:
            x = x.replace("\\","/")               
            TES.write(x + "\n") 
    TES.close()   

    for path, subdirs, files in os.walk(valpath):   
        for filename in files:
            f = os.path.join(path, filename) #don't use this line if you only want names, not path. Then change 'f' to 'filename'.
            valdata.append(f)
    with open("val.txt", "w") as VA: 
        for x in valdata:
            x = x.replace("\\","/")               
            VA.write(x + "\n") 
    VA.close()        
   
write_finaltxt('./dataset')
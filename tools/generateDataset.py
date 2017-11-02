import numpy as np
import os 
import sys
import time
import StringIO, PIL.Image
from unrealcv import client
import json
import cv2

objectColor=['pink','red','orange','brown','yellow','olive','green','blue','purple','white','gray','black']
class Dataset(object):
    def __init__(self,folder,nberOfImages,cameraId):
        self.folder=folder
        self.litImage='litImage'
        self.normalImage='normalImage'
        self.depthImage='depthImage'
        self.maskImage='maskImage'
        self.annotation='annotation'
        self.annotExtension='json'
        self.index=0
        self.extension='jpg'
        self.nberOfImages=nberOfImages
        self.cameraId=cameraId
        self.objectColor={}
        self.listObjects={}
        #make dataset directory
        try:
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)
            else:
                for the_file in os.listdir(self.folder):
                    file_path = os.path.join(self.folder, the_file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
        except Exception,e:
             print('Error: Problem with dataset directory. '+str(e))
        
        try:
            client.connect()
            print('Status: \n'+client.request('vget /unrealcv/status'))
            objects=client.request('vget /objects').split(' ')
            print(objects)
            print(str(len(objects))+' objects found in the scene.')
            #map object to color
            for i in range(len(objects)):
                #convert '(R=127,G=191,B=127,A=255)' to [127, 191, 127, 255]
                e=client.request('vget /object/'+objects[i]+'/color')
                t=e.split('(')[1].split(')')[0].split(',')
                t=[int(t[0].split('=')[1]),int(t[1].split('=')[1]),int(t[2].split('=')[1]),int(t[3].split('=')[1])]
                #t=np.array(t,dtype='uint8')
                self.objectColor[objects[i]]=t
            print(self.objectColor)
        except Exception,e:
            print('Error: Problem with unrealcv .'+str(e))
        
    #convert from raw to RGB image matrice
    def read_png(self,res):
        img = PIL.Image.open(StringIO.StringIO(res))
        return np.asarray(img)
    #get key from dictionnary given value
    def getKey(self,val):
        res=None
        for key in self.objectColor.keys():
            if(self.objectColor[key][0]<=val[0]+3 and self.objectColor[key][0]>=val[0]-3 and
                self.objectColor[key][1]<=val[1]+3 and self.objectColor[key][1]>=val[1]-3 and
                self.objectColor[key][2]<=val[2]+3 and self.objectColor[key][2]>=val[2]-3 and
                self.objectColor[key][3]<=val[3]+3 and self.objectColor[key][3]>=val[3]-3 ):
                return key
        return None
    #get objects     
    def getCurrentObjects(self,img):
        self.listObjects={}
        sh=img.shape
        n=sh[0]
        m=sh[1]
        for i in range(n):
            for j in range(m):
                key=self.getKey(list(img[i][j]))
                if key in self.listObjects.keys():
                    self.listObjects[key].append([i,j])
                else:
                    self.listObjects[key]=[[i,j]]
        
    #object name from id
    def getName(self,objectId):
        return objectId
        
    #annotate images
    def annotate(self):
        #build json object
        jsonArray=[]
        #image and question ids. Question id is not used for now
        imageId=str(self.index)
        questionId=""
        try:
            #get camera Position x,y,z
            camPosition=client.request('vget /camera/'+str(self.cameraId)+'/location').split(' ')
            camPosition=[float(camPosition[0]),float(camPosition[1]),float(camPosition[2])]
            #get camera orientation teta,beta,phi
            camOrientation=client.request('vget /camera/'+str(self.cameraId)+'/rotation').split(' ')
            camOrientation=[float(camOrientation[0]),float(camOrientation[1]),float(camOrientation[2])]
        except Exception,e:
            print('Error occured when requesting camera properties. '+str(e))
        #objId is the object Id
        for objId in self.listObjects.keys():
            #get object tags template
            objTagTemp={"objectShape":"","objectExternalMaterial":"","objectInternalMaterial":"","objectHardness":"",
                        "objectPickability":"","objectGraspability":"","objectStackability":"","objectOpenability":""}
            #get object color
            objColor=""
            #get object Location
            objLocation=""
            #get object segmentation color
            objSegColor=self.objectColor[objId]
            #get object segmentation pixels
            objSegPixels=self.listObjects[objId]
            if len(objSegPixels)<=0:
                raise ValueError()
            #get object cuboid
            objCuboid=[]
            #get object local orientation
            objLocalOrientation=[]
            #get object local Position: with camera as reference
            objLocalPosition=[]
            #get object tags,global Position and orientation
            try:
                objTags=client.request('vget /object/'+objId+'/tags')
                #split tags
                objTags=objTags.split(';')
                for elt in objTags:
                    try:
                        elt=elt.split(':')
                        objTagTemp[elt[0]]=elt[1]
                    except Exception,e:
                         print('Error occured when parsing object tags. '+str(e))
                #get object Position x,y,z
                objPosition=client.request('vget /object/'+objId+'/location').split(' ')
                objPosition=[float(objPosition[0]),float(objPosition[1]),float(objPosition[2])]
                #get object orientation teta,beta,phi
                objOrientation=client.request('vget /object/'+objId+'/rotation').split(' ')
                objOrientation=[float(objOrientation[0]),float(objOrientation[1]),float(objOrientation[2])]
            except Exception,e:
                print('Error occured when requesting object properties. '+str(e))
                
             
            jsonArray.append(
                              '{"objectId":"'+objId+'",'+
                                '"objectName":"'+self.getName(objId)+'",'+
                                '"objectShape":"'+objTagTemp["objectShape"]+'",'+
                                '"objectColor":"'+objColor+'",'+
                                '"objectExternMaterial":"'+str(objTagTemp["objectExternalMaterial"])+'",'+
                                '"objectInternMaterial":"'+str(objTagTemp["objectInternalMaterial"])+'",'+
                                '"objectHardness":"'+str(objTagTemp["objectHardness"])+'",'+
                                '"objectLocation":"'+str(objLocation)+'",'+
                                '"objectPickability":"'+str(objTagTemp["objectPickability"])+'",'+
                                '"objectGraspability":"'+str(objTagTemp["objectGraspability"])+'",'+
                                '"objectStackability":"'+str(objTagTemp["objectStackability"])+'",'+
                                '"objectOpenability":"'+str(objTagTemp["objectOpenability"])+'",'+
                                '"objectGlobalOrientation":'+str(objOrientation)+','+
                                '"objectGlobalPosition":'+str(objPosition)+','+
                                '"objectLocalPosition":'+str(objLocalPosition)+','+
                                '"objectLocalOrientation":'+str(objLocalOrientation)+','+
                                '"objectCuboid":'+str(objCuboid)+','+
                                '"objectSegmentationColor":'+str(objSegColor)+','+
                                '"objectSegmentationPixels":'+str(objSegPixels)+''+
                                '}'
                            )
        
        
        listObj='['
        for i in range(len(jsonArray)):
            listObj=listObj+jsonArray[i]
            if i==len(jsonArray)-1:
                listObj=listObj+']'
            else:
                listObj=listObj+','
        jsonImage='{'+'"imageId":"'+str(imageId)+'",'+'"questionId":"'+str(questionId)+'",'+'"cameraGlobalOrientation":'+str(camOrientation)+','+'"cameraGlobalPosition":'+str(camPosition)+','+'"objects":'+str(listObj)+''+'}'
        try:
            #convert from plain to json
            jsonImage=json.loads(jsonImage)
            #write json annotation to file
            with open(os.path.join(self.folder,self.annotation+str(self.index)+'.'+self.annotExtension),'w') as outfile:
                json.dump(jsonImage,outfile,indent=5)
            print('Annotation saved successfully.')
            del jsonArray[:]
        except Exception,e:
            print('Annotation failed. '+str(e))
    
    def cleanup(self):
        client.disconnect()
        
    #get object pixels
    def getObjectColor(self, jsonFile,objName,imageName):
        try:
            with open(jsonFile,'r') as infile:
                jsonImage=json.load(infile)
            for a in jsonImage['objects']:
                if a['objectName']==objName:
                    e=a
                    break
            if e==None:
                raise ValueError('Unknown object with name: '+objName)
            lign=[]
            col=[]
            obj=e
            img=cv2.imread(imageName)
            histo=np.zeros([256,256,256],dtype='uint')
            for elt in obj['objectSegmentationPixels']:
                histo[img[elt[0]][elt[1]][0]][img[elt[0]][elt[1]][1]][img[elt[0]][elt[1]][2]]+=1
            imax=0
            jmax=0
            kmax=0
            max=0
            for i in range(255):
                for j in range(255):
                    for k in range(255):
                        if  histo[i][j][k]>=max:
                            max= histo[i][j][k]
                            [imax,jmax,kmax]=[i,j,k]
            
            print('Color computed successfully: '+str(objName))
            return [imax,jmax,kmax,max]
        except Exception,e:
            print('Failed to compute object color. '+str(e))
            return []
    
    def saveObject(self, jsonFile,objName,imageName,outImageName):
        try:
            with open(jsonFile,'r') as infile:
                jsonImage=json.load(infile)
            for a in jsonImage['objects']:
                if a['objectName']==objName:
                    e=a
                    break
            if e==None:
                raise ValueError('Unknown object with name: '+objName)
            lign=[]
            col=[]
            obj=e
            for e in obj['objectSegmentationPixels']:
                lign.append(e[0])
                col.append(e[1])
            
            xmin=min(lign)
            ymin=min(col)
            xmax=max(lign)
            ymax=max(col)
            
            img=np.ones([xmax-xmin+1,ymax-ymin+1,3],dtype='uint8')*255
            im=cv2.imread(imageName)
            for e in obj['objectSegmentationPixels']:
                img[e[0]-xmin][e[1]-ymin][0]=im[e[0]][e[1]][0]
                img[e[0]-xmin][e[1]-ymin][1]=im[e[0]][e[1]][1]
                img[e[0]-xmin][e[1]-ymin][2]=im[e[0]][e[1]][2]
            cv2.imwrite(outImageName,img)
            print('Object saved successfully.')
        except Exception,e:
            print('Failed to save object. '+str(e))
     
    #compute  RGB-color of an image
    def computeRGBColor(self, imageName):
        #weighted sum of pixels' RGB color
        length=0
        try:
            sum=np.array([256,256,256],dtype='uint')
            img=cv2.imread(imageName)
            histo=np.zeros([256,256,256],dtype='uint')
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                   histo[img[i][j][0]][img[i][j][1]][img[i][j][2]]+=1
            imax=0
            jmax=0
            kmax=0
            max=0
            for i in range(255):
                for j in range(255):
                    for k in range(255):
                        if  histo[i][j][k]>=max:
                            max= histo[i][j][k]
                            [imax,jmax,kmax]=[i,j,k]
            
            print('Color computed successfully: '+str(imageName))
            return [imax,jmax,kmax,max]
        except Exception,e:
            print('Failed to compute color: '+str(imageName)+' .'+str(e))
            return None
            
            
            
        
    #save nberOfImages images
    def scan(self):
        for i in range(self.nberOfImages):
                try:
                    
                    
                    img=client.request('vget /camera/'+str(self.cameraId)+'/lit png')
                    img=self.read_png(img)
                    img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                    if not(cv2.imwrite(os.path.join(self.folder,self.litImage)+str(i)+'.'+self.extension,img)):
                        print('Failed to save lit image!!!')
                        
                       
                    img=client.request('vget /camera/'+str(self.cameraId)+'/normal png')
                    img=self.read_png(img)
                    img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                    if not(cv2.imwrite(os.path.join(self.folder,self.normalImage)+str(i)+'.'+self.extension,img)):
                        print('Failed to save normal image!!!')
                    
                   
                    img=client.request('vget /camera/'+str(self.cameraId)+'/depth png')
                    img=self.read_png(img)
                    img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                    if not(cv2.imwrite(os.path.join(self.folder,self.depthImage)+str(i)+'.'+self.extension,img)):
                        print('Failed to save depth image!!!')
                        
                   
                    img=client.request('vget /camera/'+str(self.cameraId)+'/object_mask png')
                    img=self.read_png(img)
                    self.getCurrentObjects(img)
                    #build annotation
                    self.index=i
                    self.annotate()
                    #print(self.listObjects)  
                    img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                    if not(cv2.imwrite(os.path.join(self.folder,self.maskImage)+str(i)+'.'+self.extension,img)):
                        print('Failed to save maskimage!!!')

                 
                except Exception,e:
                    print('Image could not be saved not saved: error occured .'+str(e))
            
        print('Scan terminated with success.')

    # Calculates translation Matrix given translation vector.
    def vectorToTranslationMatrix(self,vector) :
        
        T = np.array([[1,         0,                  0,               vector[0]    ],
                        [0,         1,                  0,               vector[1]    ],
                        [0,         0,                  1,               vector[2]    ],
                        [0,         0,                  0,               1    ]
                        ])
        return T
        
    # Calculates Rotation Matrix given euler angles.
    def eulerAnglesToRotationMatrix(self,theta) :
        
        R_x = np.array([[1,         0,                  0                   ],
                        [0,         np.cos(theta[0]), -np.sin(theta[0]) ],
                        [0,         np.sin(theta[0]), np.cos(theta[0])  ]
                        ])
            
            
                        
        R_y = np.array([[np.cos(theta[1]),    0,      np.sin(theta[1])  ],
                        [0,                     1,      0                   ],
                        [-np.sin(theta[1]),   0,      np.cos(theta[1])  ]
                        ])
                    
        R_z = np.array([[np.cos(theta[2]),    -np.sin(theta[2]),    0],
                        [np.sin(theta[2]),    np.cos(theta[2]),     0],
                        [0,                     0,                      1]
                        ])
                        
                        
        R = np.dot(R_z, np.dot( R_y, R_x ))
    
        return R
    
    # Checks if a matrix is a valid translation matrix.
    def isTranslationMatrix(self,R) :
        if R.shape[0]!=R.shape[1]:
            return False
        for i in range(R.shape[0]):
            if R[i][i]!=1:
                return False
            for j in range(R.shape[1]-1):
                if j!=i and R[i][j]!=0:
                    return False
        return True
    
        
    # Checks if a matrix is a valid rotation matrix.
    def isRotationMatrix(self,R) :
        if R.shape[0]!=R.shape[1]:
            return False
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

     
    # Calculates translation matrix to translation vector
    def translationMatrixToVector(self,R) :
        assert(self.isTranslationMatrix(R))
        vector=[]
        for i in range(R.shape[0]):
            vector.append(R[i][R.shape[1]-1])
        return vector
        
    # Calculates rotation matrix to euler angles
    # The result is the same as MATLAB except the order
    # of the euler angles ( x and z are swapped ).
    def rotationMatrixToEulerAngles(self,R) :
    
        assert(self.isRotationMatrix(R))
        
        sy = np.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
        
        singular = sy < 1e-6
    
        if  not singular :
            x = np.atan2(R[2,1] , R[2,2])
            y = np.atan2(-R[2,0], sy)
            z = np.atan2(R[1,0], R[0,0])
        else :
            x = np.atan2(-R[1,2], R[1,1])
            y = np.atan2(-R[2,0], sy)
            z = 0
    
        return np.array([x, y, z])    
    
    #radian to    
import numpy as np

class DatasetClasses(object):
    """This class is platform independent and holds 
       information about classes found in the dataset
    """
    #Field of view
    FIELD_OF_VIEW=70.0
    
    #Number of target feature(classes)
    #Object category, color, shape, material, openability, poses, relationships
    NUM_FEATURES=7
    
    #Target features
    FEATURES_INDEX={'CATEGORY':0,'COLOR':1,'SHAPE':2,'MATERIAL':3,'OPENABILITY':4,'RELATION':5,'RELATION_CATEGORY':6}

    #categories
    OBJECT_NAME_DICO=['Tea','Juice','Plate','Mug','Bowl','Tray','Tomato','Ketchup','Salt','Muesli','Spoon','Spatula','Milk','Coffee','Knife','Cornflakes','Eggholder','Pancake','Cereal','Rice']#Any other is part of background
    
    #colors
    OBJECT_COLOR_DICO=['Red', 'Orange', 'Brown', 'Yellow', 'Green', 'Blue', 'White', 'Gray', 'Black', 'Violet','Pink']
    
    #shape
    OBJECT_SHAPE_DICO=['Cubic','Conical', 'Cylindrical', 'Filiform', 'Flat']
    
    #material
    OBJECT_MATERIAL_DICO=['Plastic', 'Wood', 'Glass', 'Steel', 'Cartoon', 'Ceramic']
    
    #openability
    OBJECT_OPENABILITY_DICO={'True':'Openable','False':'Non-Openable'}
    
    #object relationships
    OBJECT_RELATION_DICO={'Left':'LeftRight','Right':'LeftRight','Front':'FrontBehind','Behind':'FrontBehind','Over':'OverUnder','Under':'OverUnder','Valign':'OverUnder','In':'OnIn','On':'OnIn'}
    
    #relationship categories
    RELATION_CATEGORY_DICO={0+1:'LeftRight',1+1:'FrontBehind',2+1:'OverUnder',3+1:'OnIn'}

    # Number of classes per features(object's category/name, color, shape, material, openability) (including background)
    NUM_CLASSES =[1+len(OBJECT_NAME_DICO),
                  1+len(OBJECT_COLOR_DICO),
                  1+len(OBJECT_SHAPE_DICO),
                  1+len(OBJECT_MATERIAL_DICO),
                  1+len(OBJECT_OPENABILITY_DICO),
                  1+len(OBJECT_RELATION_DICO),
                  1+len(RELATION_CATEGORY_DICO)]  # background + 3 shapes

    #Max Object Coordinate in cm
    MAX_OBJECT_COORDINATE=420
    
    #Max CAMERA_CENTER_TO_PIXEL_DISTANCE in m
    MAX_CAMERA_CENTER_TO_PIXEL_DISTANCE=np.sqrt(3.*(MAX_OBJECT_COORDINATE**2))/100.
    
    #Image Shape
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 640
    IMAGE_MAX_CHANNEL=6
    
    # Image mean (RGB)
    MEAN_PIXEL = np.array([123.7, 116.8, 103.9,173., 122., 127.])
    
    #Properties of image files 
    
    DATASET_FOLDER='D:/dataset1'
    SCREENSHOT_FOLDER='C:\\Users\\Franklin\\Desktop\\masterthesis\\P12-VisionScanning-UR16\\VisionScanning\\Saved\\Screenshots\\Windows'
    LIT_IMAGE_NAME_ROOT='litImage'
    NORMAL_IMAGE_NAME_ROOT='normalImage'
    DEPTH_IMAGE_NAME_ROOT='depthImage'
    MASK_IMAGE_NAME_ROOT='maskImage'
    ANNOTATION_IMAGE_NAME_ROOT='annotation'
    ANNOTATION_FILE_EXTENSION='json'
    IMAGE_FILE_EXTENSION='jpg'
    DEPTH_FILE_EXTENSION='exr'
    NUMBER_IMAGES=0
    INDEX=0
    CAMERA_ID=0
    #with or without connection to UE4: values={'offline','online'}
    MODE='online'
    #resume from actual scene or restart for a new scene:values={'continue','restart'}
    STATE='restart' 
    
    #Canonical relationships between object in the scene
    ACTOR_IDS={0:'A_Albi_Juice_1',1:'A_Mug_32',2:'A_Bowl_35',3:'A_Spoon_14'}
    # Only use relations={ 'left','front','under','on','in','has','valign'} for optimization.
    # The other relationships will be deductively generated. if A is left B,then B is right A.
    RELATIONSHIP_MAP=[[0,'left',1],[2,'front',0],[3,'front',0],[2,'front',1],[3,'front',1],[3,'in',2]]
    
    
    
    def __init__(self):
        pass
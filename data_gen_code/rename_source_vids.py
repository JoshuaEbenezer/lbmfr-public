import os
import filecmp
from shutil import copyfile
import glob

output_dir = '../full_length_source_videos_fullnames'
files = glob.glob(os.path.join('../full_length_source_videos','*'))
for fullfilename in files:
    flag = 1
    dirname = os.path.splitext(os.path.basename(fullfilename))[0]
    extension =os.path.splitext(os.path.basename(fullfilename))[1] 
    if( 'EPL2019_D' in dirname ):
        newdirname = 'EPLDay'
    elif( 'EPL2019_N' in dirname ):
        newdirname = 'EPLNight'
    elif( 'UsOpen' in dirname ):
        
        newdirname = 'USOpen'
    elif( 'TNF_N' in dirname ):
        
        newdirname = 'TNFNFL'
    elif( 'TNF_F' in dirname ):
        
        newdirname = 'TNFF'
    elif('Clip1' in dirname):
        
        newdirname = 'Cricket1'
    elif('Clip2' in dirname):
        
        newdirname = 'Cricket2'
    else:
        newdirname='ERROR'
        flag = 0
    if(flag):
        print(fullfilename)
        newname = '_'.join([newdirname,'SRC','SRC','SRC','SRC'])+extension
        print(newname) 
        outname = os.path.join(output_dir,newname)
        print(outname)
        if not os.path.exists(outname) or not filecmp.cmp(fullfilename,outname):
            print('copying')
            copyfile(fullfilename,outname)



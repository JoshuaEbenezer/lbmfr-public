import os
import filecmp
from shutil import copyfile
import glob

output_dir = '../full_length_distorted_mp4_fullnames'
for root,dirs,files in os.walk("../full_length_distorted_mp4/",topdown=False):
    for name in files:
        fullfilename = os.path.join(root,name)
        print(fullfilename)
        dirname = os.path.basename(os.path.dirname(fullfilename))
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
        print(name)
        if(('Hevc' in name)):
            bitrate = name.split('_')[-2]
            res =  name.split('_')[-3]
            if('Sfr' in name or 'SFR' in name):
                fps = 'SFR'
            else:
                fps = 'HFR'
            newname = '_'.join([newdirname,'HEVC',fps,res,bitrate])+'.mp4'
#            print(newname) 
        elif('HEVC' in name):
            bitrate = name.split('_')[-1]
            res =  name.split('_')[-2]
            fps =  name.split('_')[-3]
            newname = '_'.join([newdirname,'HEVC',fps,res,bitrate])
        elif('AVC' in name):
            if(newdirname=='Cricket2' and name.split('_')[-4]=='HFR'):
                bitrate = name.split('_')[-1]
                res =  name.split('_')[-2]
                fps =  name.split('_')[-4]
            else:
                bitrate = name.split('_')[-1]
                res =  name.split('_')[-2]
                fps =  name.split('_')[-3]
            newname = '_'.join([newdirname,'AVC',fps,res,bitrate])
#            print(newname)
        else:
            print(fullfilename,' is NOT seen')
        outname = os.path.join(output_dir,newname)
        print(outname)
        if not os.path.exists(outname) or not filecmp.cmp(fullfilename,outname):
            print('copying')
            copyfile(fullfilename,outname)
#
#

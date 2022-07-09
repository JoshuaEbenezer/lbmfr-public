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
        else:
            continue
        print(name)
        if('AVC' in name):
            bitrate = name.split('_')[-1]
            res =  name.split('_')[-2]
            fps =  name.split('_')[-3]
            if(fps=='SFR'):
                newname = '_'.join([newdirname,'AVC',fps,res,bitrate])
                outname = os.path.join(output_dir,newname)
                print(outname)
                if not os.path.exists(outname) or not filecmp.cmp(fullfilename,outname):
                    print('copying')
                    copyfile(fullfilename,outname)
#            print(newname)
            else:
                print('not avc hfr')
#

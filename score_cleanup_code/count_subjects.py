import os
import glob

filenames = glob.glob(os.path.join('./mos_sepsess_zscores','*'))
group1 = 0
group2 = 0
group3 = 0
for f in filenames:
    base = os.path.splitext(os.path.basename(f))[0]
    num = int(base.split('_')[1])
    print(num)
    if(num<=30 or (num >=91 and num<=120)):
        group1=group1+1
    elif(num<=60 or (num >=121 and num<=150)):
        group2=group2+1
    elif(num<=90 or (num >=151 and num<=180)):
        group3=group3+1

print(group1,group2,group3)


import os
from entropy.entropy_cal import video_process
from entropy.entropy_temporal_pool import entropy_temporal_pool
import numpy as np

def greed_feat(args):
    dist_path = args.dist_path
    ref_path = args.ref_path
    if (args.dist_fps!=args.ref_fps):
        print('different fps, using PR')
        pseudo_reference_name = os.path.join('./pseudo_reference_lbvfr',os.path.splitext(os.path.basename(args.ref_path))[0]+'_pseudo_reference.y4m')
    else:
        print('same fps, PR is original video')
        pseudo_reference_name = args.ref_path
    
    filt = args.temp_filt
    num_levels = 3
    
    height = args.height
    width = args.width
    gray = True
    ref_fps = args.ref_fps
    bit_depth = args.bit_depth
    if bit_depth == 8:
        multiplier = 1.5
        scales = [4,5]      #for 1080p resolution
    else:
        multiplier = 3      #10 bit video
        scales = [5,6]      #for 4K resolution
    
    #calculate number of frames in reference and distorted    
    ref_stream = open(ref_path,'r')
    ref_stream.seek(0, os.SEEK_END)
    ref_filesize = ref_stream.tell()
    print(ref_filesize,height,width,multiplier)
    ref_T = int(ref_filesize/(height*width*multiplier))
    print(ref_T,' is the reference time')
    
    dist_stream = open(dist_path,'r')
    print(dist_path)
    dist_stream.seek(0, os.SEEK_END)
    dist_filesize = dist_stream.tell()
    print(dist_filesize)
    dist_T = int(dist_filesize/(height*width*multiplier))
    print(dist_T, ' is the distorted time')
    
    fps = args.dist_fps       #frame rate of distorted sequence
    
    arg_list = [ref_path, width, height, bit_depth, \
                   ref_fps, ref_T, filt, num_levels, scales]
    print(arg_list)
    arg_list = [pseudo_reference_name, width, height, bit_depth, \
                   fps,dist_T, filt, num_levels, scales]
    print(arg_list)
    #calculate spatial entropy
    ref_entropy = video_process(ref_path, width, height, bit_depth, gray, \
                                   ref_T, filt, num_levels, scales)
    dist_entropy = video_process(dist_path, width, height, bit_depth, gray, \
                                   dist_T, filt, num_levels, scales)
    pr_entropy = video_process(pseudo_reference_name, width, height, bit_depth, gray, \
                                   dist_T, filt, num_levels, scales)
    
    
    #number of valid frames
    end_lim = dist_entropy['spatial_scale' + str(scales[0])].shape[-1]
    
    greed_feat = np.zeros(16,dtype=np.float32)
    for idx,scale_factor in enumerate(scales):
        print(fps,ref_fps)
        if fps != ref_fps:
            print('Performing temporal pooling')
            #Temporal Pooling of reference entropies to match the number of frames
            ref_entropy['spatial_scale' + str(scale_factor)] = \
            entropy_temporal_pool(ref_entropy['spatial_scale' + str(scale_factor)][None,:,:,:],\
                                       fps,ref_fps,end_lim)
            ref_entropy['temporal_scale' + str(scale_factor)] = \
            entropy_temporal_pool(ref_entropy['temporal_scale' + str(scale_factor)],\
                                              fps,ref_fps,end_lim)
        
        a = ref_entropy['spatial_scale' + str(scale_factor)]
        b= dist_entropy['spatial_scale' + str(scale_factor)]
        print(a.shape,b.shape)
    #    spatial entropy difference
        ent_diff_sp = np.abs(ref_entropy['spatial_scale' + str(scale_factor)] - \
                             dist_entropy['spatial_scale' + str(scale_factor)])
        if len(ent_diff_sp.shape) < 4:
            ent_diff_sp = ent_diff_sp[None,:,:,:]
        spatial_ent = np.mean(np.mean(ent_diff_sp[0,:,:,:],axis=0),axis=0)
        greed_feat[idx] = np.mean(spatial_ent)
        
    #     temporal entropy difference
        for freq in range(dist_entropy['temporal_scale' + str(scale_factor)].shape[0]):
            a = dist_entropy['temporal_scale' + str(scale_factor)][freq,:,:,:]
            b = pr_entropy['temporal_scale' + str(scale_factor)][freq,:,:,:]
            c = ref_entropy['temporal_scale' + str(scale_factor)][freq,:,:,:]
            
            ent_diff_temporal = np.abs(((1+np.abs(a - b))*(1+c)/(1+b)) - 1)
            temp_ent_frame = np.mean(np.mean(ent_diff_temporal,axis=0),axis=0)
            
            greed_feat[2*(freq+1)+idx] = np.mean(temp_ent_frame)
    
    return greed_feat

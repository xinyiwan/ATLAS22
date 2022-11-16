import os
import glob
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np



images_list = glob.glob("/home/k8s-group5/Training/*/*/*/*/*T1w.nii.gz")

working_path = '/home/k8s-group5'
images_path = os.path.join(working_path,"Images")
masks_path = os.path.join(working_path,"Masks")
if not os.path.exists(images_path):
    os.mkdir(images_path)
if not os.path.exists(masks_path):
    os.mkdir(masks_path)

for i in images_list[0:1]:

    label = i.split("/anat/")[1].split("_ses")[0]

    i_mask = i.replace("_T1w.nii.gz","_label-L_desc-T1lesion_mask.nii.gz")
    mask = nib.load(i_mask).get_fdata()
    mask_data = np.zeros((mask.shape[1],mask.shape[1],mask.shape[2]))
    mask_data[18:215,:,:] = mask

    img = nib.load(i).get_fdata()
    img_data = np.zeros((img.shape[1],img.shape[1],img.shape[2]))
    img_data[18:215,:,:] = img

    # Get meaningful volume from data
    for idx in range(50,mask_data.shape[-1]-50):
        if 1 in mask_data[:,:,idx]:
            plt.imshow(mask_data[:,:,idx],cmap = 'gray')
            plt.axis('off')
            mask_file = label + "_{}_".format(idx) + "mask.jpg"
            plt.savefig(os.path.join(masks_path,mask_file), dpi = 70)


            plt.imshow(img_data[:,:,idx],cmap = 'gray')
            plt.axis('off')
            img_file = label + "_{}_".format(idx) + "img.jpg"
            plt.savefig(os.path.join(images_path,img_file), dpi = 70)
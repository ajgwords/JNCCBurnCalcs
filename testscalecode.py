"""
This module contains code for testing the scaling up on JASMIN of calculating burn locations in Scotland, using data held on CEDA
    
Contributors: 
    Alastair Graham, Geoger Ltd, @ajggeoger
    Duncan Blake, Nature Scotland

"""

# Imports
#import json
#import pandas as pd
#import logging
#import numpy as np
import os
import datetime
import rasterio
#from rasterio.mask import mask
#from rasterio.features import geometry_mask
#from shapely.geometry import mapping
#from rasterstats import zonal_stats


def pre(imagename):
    '''
    Opens and reads the pre fire image. 
    Takes in a path to a .tif file.
    Returns individual bands and the image profile.
    '''
    with rasterio.open(imagename) as dataset:
        print('PRE BURN IMAGE')
        print('Name: ', dataset.name)
        print('Count: ', dataset.count)
        print('Width: ', dataset.width)
        print('Height: ', dataset.height)
        print('CRS: ', dataset.crs)

        profile = dataset.profile.copy()

        red = dataset.read(3)
        nir = dataset.read(7)
        swir1 = dataset.read(9)
        swir2 = dataset.read(10)
        return red, nir, swir1, swir2, profile


def post(imagename):
    ''' 
    Opens and reads the post fire image. 
    Takes in a path to a .tif file.
    Returns individual bands and the image profile.
    '''
    with rasterio.open(imagename) as dataset:
        print('POST BURN IMAGE')
        print('Name: ', dataset.name)
        print('Count: ', dataset.count)
        print('Width: ', dataset.width)
        print('Height: ', dataset.height)
        print('CRS: ', dataset.crs)

        profile = dataset.profile.copy()

        red = dataset.read(3)
        nir = dataset.read(7)
        swir1 = dataset.read(9)
        swir2 = dataset.read(10)
        return red, nir, swir1, swir2, profile


def nbr(swir1, nir):
    '''
    Calculates Normalised Burn Ratio (NBR).
    The NBR equation is the opposite way round to normal but this is as recommended by Filiponi: to make the behavior of the indices consistent i.e. the values of all the indices increase if fire has occurred. 
    '''
    nbr = ((swir1 - nir)/(swir1 + nir)).astype(rasterio.float32)
    return nbr
    

def nbr2(swir2, swir1):
    '''
    Calculates NBR2
    '''
    nbr2 = ((swir2 - swir1)/(swir2 + swir1)).astype(rasterio.float32)
    return nbr2

def savi(nir, red, L = 0.5):
    '''
    Calculates Soil Adjusted Vegetation Index (SAVI) 
    The default version of paramer L is set to 0.5. Specify a value in the function call to over-ride this.
    '''
    savi = (-1 * (1.5 * ((nir - red) / (nir + red + L)))).astype(rasterio.float32)
    return savi


def savedata():
    
""" with rasterio.open(os.path.join(image_dir,'{}_indices.tif'.format(iteration)), 'w', **s2prof) as dst:
  for block_index, window in dst.block_windows(1):
    #read in each band of pre fire image for current window
    s2pre_block_blue = s2pre.read(1, window=window, masked=True).astype(float)
    s2pre_block_green = s2pre.read(2, window=window, masked=True).astype(float)
    s2pre_block_red = s2pre.read(3, window=window, masked=True).astype(float)
    s2pre_block_re5 = s2pre.read(4, window=window, masked=True).astype(float)
    s2pre_block_re6 = s2pre.read(5, window=window, masked=True).astype(float)
    s2pre_block_re7 = s2pre.read(6, window=window, masked=True).astype(float)
    s2pre_block_NIR = s2pre.read(7, window=window, masked=True).astype(float)
    s2pre_block_NIR8A = s2pre.read(8, window=window, masked=True).astype(float)
    s2pre_block_SWIR1 = s2pre.read(9, window=window, masked=True).astype(float)
    s2pre_block_SWIR2 = s2pre.read(10, window=window, masked=True).astype(float)

    #read in each band of post fire image for current window
    s2post_block_blue = s2post.read(1, window=window, masked=True).astype(float)
    s2post_block_green = s2post.read(2, window=window, masked=True).astype(float)
    s2post_block_red = s2post.read(3, window=window, masked=True).astype(float)
    s2post_block_re5 = s2post.read(4, window=window, masked=True).astype(float)
    s2post_block_re6 = s2post.read(5, window=window, masked=True).astype(float)
    s2post_block_re7 = s2post.read(6, window=window, masked=True).astype(float)
    s2post_block_NIR = s2post.read(7, window=window, masked=True).astype(float)
    s2post_block_NIR8A = s2post.read(8, window=window, masked=True).astype(float)
    s2post_block_SWIR1 = s2post.read(9, window=window, masked=True).astype(float)
    s2post_block_SWIR2 = s2post.read(10, window=window, masked=True).astype(float)
    
   
    np.seterr(divide='ignore', invalid = 'ignore' ) #ignore errors from calculating indices/ ratios#over= 'ignore', under = 'ignore' 

    
    

    #write results for current window
    dst.write_band(1, pre_nbr, window = window)
    dst.write_band(2, post_nbr, window = window)
     """
    pass




if __name__ == "__main__":
    
    # TODO: make sure logging is in place

    # Set working directory
    wd = '/home/al/sdaDocuments/ProjectFiles/Muirburn_TEMP'
    # Set output directory
    od = wd
    
    # Set image 
    # TODO: (improve on this using dict)
    image = 'S2A_20190627_lat57lon375_T30VVJ_ORB080_utm30n_osgb_vmsk_sharp_rad_srefdem_stdsref.tif'
    image_data = os.path.join(wd, image)

    # Start timer
    starttime1 = datetime.datetime.now()
    print('--STARTING PROCESSING--')

    print('--GETTING DATA--')
    # pre-fire image
    prered, prenir, preswir1, preswir2, preprofile = pre(image_data)
    # post-fire image
    #postred, postnir, postswir1, postswir2, postprofile = post(image_data)
    
    print('--CALCULATING NBR--')
    prenbr = nbr(preswir1, prenir)
    print("Pre-NBR Shape: ", prenbr.shape)
    #postnbr = nbr(postswir1, postnir)
    #print("Post-NBR Shape: ", postnbr.shape)

    print('--CALCULATING NBR2--')
    prenbr2 = savi(preswir2, preswir1)
    print("Pre-NBR2 Shape: ", prenbr2.shape)
    #postnbr2 = nbr(postswir2, postswir1)
    #print("Post-NBR2 Shape: ", postnbr.shape)

    print('--CALCULATING SAVI--')
    presavi = savi(prenir, prered)
    print("Pre-SAVI Shape: ", bob.shape)
    #postsavi = savi(postnir, postred)
    #print("Pre-SAVI Shape: ", postsavi.shape)


    print('--WRITING OUTPUT--')
    

    # Stop timer
    endtime1=datetime.datetime.now()
    deltatime1=endtime1-starttime1
    print(("Time to process:  {0}  hr:min:sec".format(deltatime1)))



# -- Notes --


#output greater than 4GB therefore needs to be BigTIFF
#s2prof.update(count=C, nodata=None, dtype=np.float32, BIGTIFF="IF_SAFER")
#print((s2prof))


#Combined: 
#dSAVI still shows reasonable separability with the other classes (especially snow to no snow) though with a little overlap with no cloud to cloud (which did not exist in the Cairngorms image pair). 
#With the two test areas combined the results are a bit confused but NBR or NBR2 probably show the best separability. 
#The following ruleset seemed to give quite good results for both Skye and the Cairngorms and utilised both sets of training data to set the thresholds: 
#dSAVI >= median value (0.2853) AND post fire NBR > =median value (0.2395) 
#And a secondary rule to remove issues of false positives at edges of clouds 
#dNBR2 >= 0.8 (NB those pixels meeting this criterium were removed). 
#As a test these thresholds were used on a third area – Lammer Law in the southern highlands – as some previous work had already mapped burn patches occurring between 20 September 2019 and 19 April 2020. 
# Of the 115 burn areas mapped 89 were identified automatically.  That’s 77% There were 23 additional polygons that did not intersect a mapped burn area. 
#However of these 13 are almost certainly burns (south east corner above). 
#Of the remaining ten: 
#4 could feasibly be burns (unfortunately no synchronous aerial photography to tell) 
#3 represented one area along a watercourse (reason unknown) 
#3 were area of water. 
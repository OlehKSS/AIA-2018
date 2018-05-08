import numpy, cv2
from immas import basic_functions

def dice_similarity(segmented_images,groundtruth_images):
    '''
        Performs dice similarity score calculation.
        
        Args:
        segmented_image (uint): segmentation results we want to evaluate (1 image, treated as binary)
        groundtruth_image (uint): reference/manual/groundtruth segmentation image
        
        Returns:
        dice_index (float): DICE similarity score
        '''

    # Settings for one image
    segData = segmented_images + groundtruth_images
    TP_value = numpy.amax(segmented_images) + numpy.amax(groundtruth_images)
    TP = (segData == TP_value).sum()  # found a true positive: segmentation result and groundtruth match(both are positive)
    segData_FP = 2. * segmented_images + groundtruth_images
    segData_FN = segmented_images + 2. * groundtruth_images
    FP = (segData_FP == 2 * numpy.amax(segmented_images)).sum() # found a false positive: segmentation result and groundtruth mismatch
    FN = (segData_FN == 2 * numpy.amax(groundtruth_images)).sum() # found a false negative: segmentation result and groundtruth mismatch
    return 2*TP/(2*TP+FP+FN)  # according to the definition of DICE similarity score

def find_match(img, visual_result = "no"):
    _, segmented_contours, _ = cv2.findContours(img.image_data, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _, groundtruth_contours, _ = cv2.findContours(img.cropped_ground_truth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_mass_grd = len(groundtruth_contours)
    
    num_TP = 0
    num_FP = 0
    for i in range(0, len(segmented_contours)):
        segmented_mask = numpy.zeros(img.image_data.shape, dtype='uint8')
        cv2.drawContours(segmented_mask, [segmented_contours[i]], -1, 255, thickness=cv2.FILLED)
        DICE = numpy.zeros(len(groundtruth_contours))
        for j in range(0, len(groundtruth_contours)):
            groundtruth_mask = numpy.zeros(img.image_data.shape, dtype='uint8')
            cv2.drawContours(groundtruth_mask, [groundtruth_contours[j]], -1, 255, thickness=cv2.FILLED)
            DICE[j] = dice_similarity(segmented_mask,groundtruth_mask)
        if numpy.amax(DICE) >= 0.2:
            num_TP = num_TP + 1
        else:
            num_FP = num_FP + 1
    if visual_result == "yes":
        basic_functions.accuracy(img.image_data,img.cropped_ground_truth,"yes")

    return num_TP, num_FP, num_mass_grd

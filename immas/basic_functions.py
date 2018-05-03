import cv2,sys,numpy
import matplotlib.pyplot as plt

def show_image_cv(img, window_name):
    '''
        Shows images using cv2 imshow in smaller windows. Close by pressing any key
        
        Args:
        img: image file.
        window_name (string): name of window to be displayed
        
        Returns:
        0
        '''
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.startWindowThread()
    cv2.resizeWindow(window_name, 332, 408)
    cv2.imshow(window_name, img)
    cv2.waitKey(0)


def show_image_plt(img, image_name):
    '''
        Shows images using matplotlib plt.
        
        Args:
        img: image file.
        image_name (string): title of image to be displayed
        
        Returns:
        0
        '''
    plt.imshow(img, cmap="gray")
    plt.axis('off')
    plt.title(image_name)
    plt.show()

def accuracy(segmented_images, groundtruth_images, visual_results):

    """
    Write a function which finds the accuracy of a given output image given the image and the ground truth
    Based on Alessandro Bria's C++ file compute-segmentation-accuracy.cpp

    Accuracy (ACC) is defined as:
        ACC = (True positives + True negatives)/(number of samples)
        i.e., as the ratio between the number of correctly classified samples (in our case, pixels)
        and the total number of samples (pixels)

    # # # # # Images must be of unsigned type # # # # #

    Input:  segemented_images (uint) - segmentation results we want to evaluate (1 or more images, treated as binary)
            groundtruth_images (uint) - reference/manual/groundtruth segmentation images
            visual_results (string) - false color images displaying the comparison between automated segmentation results and groundtruth
                             True positives = blue, True negatives = gray, False positives = yellow, False negatives = red,
                             in format "yes" or "no"

    Output: accuracy (float) - average accuracy over all given images
    """

    # True positives (TP), True negatives (TN), and total number N of pixels are all we need
    TP = 0
    TN = 0
    N = 0

    #Settings for one image
    if (len(numpy.shape(segmented_images)) == 2):
        if visual_results == "no":
            segData = segmented_images + groundtruth_images
            TP_value = numpy.amax(segmented_images) + numpy.amax(groundtruth_images)
            TP = TP + (segData == TP_value).sum()  # found a true positive: segmentation result and groundtruth match(both are positive)
            TN = TN + (
                            segData == 0).sum()  # found a true negative: segmentation result and groundtruth match(both are positive)
            N = N + (segData.shape[0] * segData.shape[1])
        elif visual_results == "yes":
            # prepare visual result(3 - channel RGB image initialized to black = (0, 0, 0) )
            img = numpy.zeros((segmented_images.shape[0], segmented_images.shape[1], 3), dtype=numpy.uint8)

            # Calculate accuracy as above
            segData = segmented_images + groundtruth_images
            TP_value = numpy.amax(segmented_images)+numpy.amax(groundtruth_images)
            TP = (segData == TP_value).sum()  # found a true positive: segmentation result and groundtruth match(both are positive)
            TN = (segData == 0).sum()  # found a true negative: segmentation result and groundtruth match(both are positive)
            N = (segData.shape[0] * segData.shape[1])

            # Find indicies of TN, TP, FN, FP
            ind_TP = numpy.where(segData == TP_value)
            ind_TP = numpy.ravel_multi_index(ind_TP, (segmented_images.shape[0], segmented_images.shape[1]))
            ind_TN = numpy.where(segData == 0)
            ind_TN = numpy.ravel_multi_index(ind_TN, (segmented_images.shape[0], segmented_images.shape[1]))

            segData_FP = 2. * segmented_images + groundtruth_images
            segData_FN = segmented_images + 2. * groundtruth_images
            ind_FP = numpy.where(segData_FP == 2*numpy.amax(segmented_images))
            ind_FP = numpy.ravel_multi_index(ind_FP, (segmented_images.shape[0], segmented_images.shape[1]))

            ind_FN = numpy.where(segData_FN == 2*numpy.amax(groundtruth_images))
            ind_FN = numpy.ravel_multi_index(ind_FN, (segmented_images.shape[0], segmented_images.shape[1]))

            # TP: Mark with blue
            numpy.put(img[..., 2], ind_TP, 255)

            # TN: Mark with grey
            numpy.put(img[..., 0], ind_TN, 128)
            numpy.put(img[..., 1], ind_TN, 128)
            numpy.put(img[..., 2], ind_TN, 128)

            # FP: Mark with yellow
            numpy.put(img[..., 0], ind_FP, 255)
            numpy.put(img[..., 1], ind_FP, 255)

            # FN: Mark with red
            numpy.put(img[..., 0], ind_FN, 255)

            show_image_plt(numpy.uint8(img), "Accuracy results")
            #plt.savefig('visual results.png')

    #All other cases
    else:

        num_segmented_images = len(segmented_images)
        num_groundtruth_images = len(groundtruth_images)

        # Checks to ensure input are of the correct format
        if 0 == num_segmented_images:
            raise ValueError("Error in accuracy(): the set of segmented images is empty")
            sys.exit()
        elif num_groundtruth_images != num_segmented_images:
            raise ValueError(
                "Error in accuracy(): the number of groundtruth images {} is different than the number of segmented images {}".format(
                    num_groundtruth_images, num_segmented_images))
            sys.exit()

        if visual_results == "no":

            #Some more checks to ensure images are correct size/shape
            for i in range(0, num_segmented_images):
                if segmented_images[i].shape != groundtruth_images[i].shape:
                    raise ValueError("Error in accuracy(): size of segemented image {} does not match that of the groundtruth image".format(i))
                    sys.exit()

            for i in range(0, num_segmented_images):
                segData = segmented_images[i] + groundtruth_images[i]
                TP = TP + (segData == numpy.amax(segData)).sum() # found a true positive: segmentation result and groundtruth match(both are positive)
                TN = TN + (segData == 0).sum() # found a true negative: segmentation result and groundtruth match(both are positive)
                N = N + (segData.shape[0] * segData.shape[1])

        elif visual_results == "yes":
            for i in range(0, num_segmented_images):
                if segmented_images[i].shape != groundtruth_images[i].shape:
                    raise ValueError("Error in accuracy(): size of segemented image {} does not match that of the groundtruth image".format(i))
                    sys.exit()

            for i in range(0, num_segmented_images):
                # prepare visual result(3 - channel RGB image initialized to black = (0, 0, 0) )
                img = numpy.zeros((segmented_images[i].shape[0], segmented_images[i].shape[1], 3), dtype=numpy.uint8)

                # Calculate accuracy as above
                segData = segmented_images[i] + groundtruth_images[i]
                TP = (segData == numpy.amax(
                    segData)).sum()  # found a true positive: segmentation result and groundtruth match(both are positive)
                TN = (segData == 0).sum()  # found a true negative: segmentation result and groundtruth match(both are positive)
                N = (segData.shape[0] * segData.shape[1])

                # Find indicies of TN, TP, FN, FP
                ind_TP = numpy.where(segData == numpy.amax(segData))
                ind_TP = numpy.ravel_multi_index(ind_TP, (segmented_images[i].shape[0], segmented_images[i].shape[1]))
                ind_TN = numpy.where(segData == 0)
                ind_TN = numpy.ravel_multi_index(ind_TN, (segmented_images[i].shape[0], segmented_images[i].shape[1]))

                segData_FP = 2 * segmented_images[i] + groundtruth_images[i]
                segData_FN = segmented_images[i] + 2 * groundtruth_images[i]
                ind_FP = numpy.where(segData_FP == 2 * numpy.amax(segmented_images[i]))
                ind_FP = numpy.ravel_multi_index(ind_FP, (segmented_images[i].shape[0], segmented_images[i].shape[1]))
                ind_FN = numpy.where(segData_FN == 2 * numpy.amax(groundtruth_images[i]))
                ind_FN = numpy.ravel_multi_index(ind_FN, (segmented_images[i].shape[0], segmented_images[i].shape[1]))

                # TP: Mark with blue
                numpy.put(img[..., 2], ind_TP, 255)

                # TN: Mark with grey
                numpy.put(img[..., 0], ind_TN, 128)
                numpy.put(img[..., 1], ind_TN, 128)
                numpy.put(img[..., 2], ind_TN, 128)

                # FP: Mark with yellow
                numpy.put(img[..., 1], ind_FP, 255)
                numpy.put(img[..., 0], ind_FP, 255)

                # FN: Mark with red
                numpy.put(img[..., 0], ind_FN, 255)

                show_image_plt(numpy.uint8(img), "Accuracy results")

    return (TP + TN) / N  # according to the definition of Accuracy


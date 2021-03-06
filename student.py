import numpy as np
import matplotlib
from skimage.io import imread
#from skimage.color import rgb2grey
from skimage.feature import hog
from skimage.transform import resize
from scipy.spatial.distance import cdist

from sklearn import preprocessing
from sklearn.svm import LinearSVC
from skimage.feature import hog
from PIL import Image
#from cyvlfeat.kmeans import kmeans
from time import time

#import sklearn.cluster
from sklearn.cluster import KMeans

def get_tiny_images(image_paths):
    """
    This feature is inspired by the simple tiny images used as features in
    80 million tiny images: a large dataset for non-parametric object and
    scene recognition. A. Torralba, R. Fergus, W. T. Freeman. IEEE
    Transactions on Pattern Analysis and Machine Intelligence, vol.30(11),
    pp. 1958-1970, 2008. http://groups.csail.mit.edu/vision/TinyImages/

    Inputs:
        image_paths: a 1-D Python list of strings. Each string is a complete
                     path to an image on the filesystem.
    Outputs:
        An n x d numpy array where n is the number of images and d is the
        length of the tiny image representation vector. e.g. if the images
        are resized to 16x16, then d is 16 * 16 = 256.

    To build a tiny image feature, resize the original image to a very small
    square resolution (e.g. 16x16). You can either resize the images to square
    while ignoring their aspect ratio, or you can crop the images into squares
    first and then resize evenly. Normalizing these tiny images will increase
    performance modestly.

    As you may recall from class, naively downsizing an image can cause
    aliasing artifacts that may throw off your comparisons. See the docs for
    skimage.transform.resize for details:
    http://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.resize

    Suggested functions: skimage.transform.resize, skimage.color.rgb2grey,
                         skimage.io.imread, np.reshape
    """

    # TODO: Implement this function!
    N = len(image_paths)
    print(f'length is {N}')
    output = np.zeros((N,256))
    for i in range(len(image_paths)):
        img = imread(image_paths[i])
        #print(f'type of image is : {type(img)}')
        resized_img = resize(img, (16,16),
                       anti_aliasing=True)
        img_norm = (resized_img - np.mean(resized_img)) / np.std(resized_img)

        # converting to 1d array and storing in output array
        output[i,:] = resize(img_norm,(1,256))

        #NORMALIZATOIN TO BE ADDED HERE


    return output


def build_vocabulary(image_paths, vocab_size):
    """
    This function should sample HOG descriptors from the training images,
    cluster them with kmeans, and then return the cluster centers.

    Inputs:
        image_paths: a Python list of image path strings
         vocab_size: an integer indicating the number of words desired for the
                     bag of words vocab set

    Outputs:
        a vocab_size x (z*z*9) (see below) array which contains the cluster
        centers that result from the K Means clustering.

    You'll need to generate HOG features using the skimage.feature.hog() function.
    The documentation is available here:
    http://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.hog

    However, the documentation is a bit confusing, so we will highlight some
    important arguments to consider:
        cells_per_block: The hog function breaks the image into evenly-sized
            blocks, which are further broken down into cells, each made of
            pixels_per_cell pixels (see below). Setting this parameter tells the
            function how many cells to include in each block. This is a tuple of
            width and height. Your SIFT implementation, which had a total of
            16 cells, was equivalent to setting this argument to (4,4).
        pixels_per_cell: This controls the width and height of each cell
            (in pixels). Like cells_per_block, it is a tuple. In your SIFT
            implementation, each cell was 4 pixels by 4 pixels, so (4,4).
        feature_vector: This argument is a boolean which tells the function
            what shape it should use for the return array. When set to True,
            it returns one long array. We recommend setting it to True and
            reshaping the result rather than working with the default value,
            as it is very confusing.

    It is up to you to choose your cells per block and pixels per cell. Choose
    values that generate reasonably-sized feature vectors and produce good
    classification results. For each cell, HOG produces a histogram (feature
    vector) of length 9. We want one feature vector per block. To do this we
    can append the histograms for each cell together. Let's say you set
    cells_per_block = (z,z). This means that the length of your feature vector
    for the block will be z*z*9.

    With feature_vector=True, hog() will return one long np array containing every
    cell histogram concatenated end to end. We want to break this up into a
    list of (z*z*9) block feature vectors. We can do this using a really nifty numpy
    function. When using np.reshape, you can set the length of one dimension to
    -1, which tells numpy to make this dimension as big as it needs to be to
    accomodate to reshape all of the data based on the other dimensions. So if
    we want to break our long np array (long_boi) into rows of z*z*9 feature
    vectors we can use small_bois = long_boi.reshape(-1, z*z*9).

    The number of feature vectors that come from this reshape is dependent on
    the size of the image you give to hog(). It will fit as many blocks as it
    can on the image. You can choose to resize (or crop) each image to a consistent size
    (therefore creating the same number of feature vectors per image), or you
    can find feature vectors in the original sized image.

    ONE MORE THING
    If we returned all the features we found as our vocabulary, we would have an
    absolutely massive vocabulary. That would make matching inefficient AND
    inaccurate! So we use K Means clustering to find a much smaller (vocab_size)
    number of representative points. We recommend using sklearn.cluster.KMeans
    to do this. Note that this can take a VERY LONG TIME to complete (upwards
    of ten minutes for large numbers of features and large max_iter), so set
    the max_iter argument to something low (we used 100) and be patient. You
    may also find success setting the "tol" argument (see documentation for
    details)
    """

    """
    #fd, hog_image=hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), block_norm='L2-Hys', visualize=False, transform_sqrt=False, feature_vector=True, multichannel=None, *, channel_axis=None)
    # TODO: Implement this functio  n!
    bag_of_features = []
    
    print("Extract HOG features")
    
    #The Python Debugger
    #pdb.set_trace()
    


    for path in image_paths:
        img = np.asarray(Image.open(path),dtype='float32')
#         frames, descriptors = dsift(img, step=[5,5], fast=True)
       # descriptors = hog(img, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), block_norm='L2-Hys', visualize=False, transform_sqrt=False, feature_vector=True, multichannel=None, *, channel_axis=None)
        descriptors=hog(img, orientations=9, pixels_per_cell=(5,5),cells_per_block=(3, 3), visualize=False)
       # descriptors=hog(img, pixels_per_cell=(5,5),cells_per_block=(3, 3), visualize=False)
        #print("descriptors shape ---->",np.shape(descriptors))
        #descriptors=descriptors.reshape((-1,9*9))
        #print("descriptors shape ---->",np.shape(descriptors))

        bag_of_features.append(descriptors)
    print("bag_of_features shape ---->",np.shape(bag_of_features))
    #print("bag_of_features----->",bag_of_features[1,:2])
    #mean_data = np.array(mean_data)

    
    #print("bag_of_features[0,:] len----->",len(bag_of_features[0,:]))
    bag_of_features = np.concatenate(bag_of_features, axis=0).astype('int')
    bag_of_features=bag_of_features.reshape((-1,9*9))
    #print("bag_of_features shape ---->",bag_of_features.reshape(bag_of_features.shape[0],2).shape)
    
    #bag_of_features=bag_of_features.reshape(1500,-1)
    #pdb.set_trace()
    
    print("Compute vocab")
    start_time = time()
    #vocab = kmeans(bag_of_features, vocab_size, initialization="PLUSPLUS")
    vocab = KMeans(n_clusters=vocab_size, random_state=0).fit(bag_of_features)    

    end_time = time()
    print("It takes ", (start_time - end_time), " to compute vocab.")
    
    return np.array([vocab.cluster_centers_])
"""
    All_features_vectors = []
    for img in image_paths:
        image = imread(img)
        image = resize(image, (128, 64))
        features_vector = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False,
                              feature_vector=True, multichannel=None)
        features_vector = features_vector.reshape(-1, 2*2*9)
        All_features_vectors.append(features_vector)

    All_features_vectors = np.vstack(All_features_vectors)
    print(All_features_vectors.shape)
    kmeans_clf = KMeans(n_clusters=vocab_size, max_iter=100).fit(All_features_vectors)
    vocab = kmeans_clf.cluster_centers_

    return vocab


def get_bags_of_words(image_paths):


    vocab = np.load('vocab.npy')
    print('Loaded vocab from file.')

    vocab_len = vocab.shape[0]
    histograms = np.zeros((len(image_paths), vocab_len))
    vocab=vocab.resize((200,81))
    print("vocab shape ---->",np.shape(vocab))

    for i, img in enumerate(image_paths):
        image = imread(img)
        image = resize(image, (120, 60))
        features_vector = hog(image, orientations=9, pixels_per_cell=(5,5), cells_per_block=(3,3), visualize=False,
                                feature_vector=True, multichannel=None)
        features_vector = features_vector.reshape(-1, 9* 9)
        histo = np.zeros(vocab_len)
        distances = cdist(features_vector, vocab)
        closest_vocab = np.argsort(distances, axis=1)[:, 0]
        index, count = np.unique(closest_vocab, return_counts=True)
        histo[index] += count
        histo = histo / np.linalg.norm(histo)
        histograms[i] = histo

    return histograms

    """
    This function should take in a list of image paths and calculate a bag of
    words histogram for each image, then return those histograms in an array.

    Inputs:
        image_paths: A Python list of strings, where each string is a complete
                     path to one image on the disk.

    Outputs:
        An nxd numpy matrix, where n is the number of images in image_paths and
        d is size of the histogram built for each image.

    Use the same hog function to extract feature vectors as before (see
    build_vocabulary). It is important that you use the same hog settings for
    both build_vocabulary and get_bags_of_words! Otherwise, you will end up
    with different feature representations between your vocab and your test
    images, and you won't be able to match anything at all!

    After getting the feature vectors for an image, you will build up a
    histogram that represents what words are contained within the image.
    For each feature, find the closest vocab word, then add 1 to the histogram
    at the index of that word. For example, if the closest vector in the vocab
    is the 103rd word, then you should add 1 to the 103rd histogram bin. Your
    histogram should have as many bins as there are vocabulary words.

    Suggested functions: scipy.spatial.distance.cdist, np.argsort,
                         np.linalg.norm, skimage.feature.hog
    """

"""
    bag_of_features = []
    vocab = np.load('vocab.npy')
    vocab=vocab.resize((200,81))
    print('Loaded vocab from file.')
    print("vocab shape ---->",np.shape(vocab))
    histograms = np.zeros((len(image_paths),int(np.shape(vocab))))

    for index,image in enumerate(image_paths):
        img = imread(image)
        img_resized = resize(img,(120,60))
        
 #       feat_vector = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3),
     #    block_norm='L2-Hys', visualize=False, transform_sqrt=False,
      #   feature_vector=True, multichannel=None, *, channel_axis=None)
        feat_vector =hog(img, orientations=9, pixels_per_cell=(5,5),cells_per_block=(3, 3), visualize=False)

        #print("feat_vector shape ---->",np.shape(feat_vector))
        feat_vector=feat_vector.reshape((-1,9*9))

        dist = cdist(feat_vector,vocab)
        hist = np.zeros(int(np.shape(vocab)))

        nearest_vocab = np.argsort(dist,axis =1)[:,0]

        pos,count = np.unique(nearest_vocab,return_counts = True)

        hist[pos] += count
        hist = hist / np.linalg.norm(hist)
        histograms[index] = hist
    
        #bag_of_features.append(feat_vector)
        #feat_vec_resized=feat_vector.reshape((-1,9*9))
        #feat_vec_resized = resize(-1,2*2*9)

    #bag_of_features = np.concatenate(bag_of_features, axis=0).astype('int')
    #bag_of_features=bag_of_features.reshape((-1,9*9))
    #vocab = KMeans(n_clusters=vocab_size, random_state=0).fit(bag_of_features)    
#-----------------------------------------------------------------------------------------------------------------------------------

    return histograms """







def svm_classify(train_image_feats, train_labels, test_image_feats):
    """
    This function will predict a category for every test image by training
    15 many-versus-one linear SVM classifiers on the training data, then
    using those learned classifiers on the testing data.

    Inputs:
        train_image_feats: An nxd numpy array, where n is the number of training
                           examples, and d is the image descriptor vector size.
        train_labels: An nx1 Python list containing the corresponding ground
                      truth labels for the training data.
        test_image_feats: An mxd numpy array, where m is the number of test
                          images and d is the image descriptor vector size.

    Outputs:
        An mx1 numpy array of strings, where each string is the predicted label
        for the corresponding image in test_image_feats

    We suggest you look at the sklearn.svm module, including the LinearSVC
    class. With the right arguments, you can get a 15-class SVM as described
    above in just one call! Be sure to read the documentation carefully.
    """
    # TODO: Implement this function!

    SVC = LinearSVC(C=700.0, class_weight=None, dual=True, fit_intercept=True,intercept_scaling=1, loss='squared_hinge', max_iter= 2000, multi_class='ovr', penalty='l2', random_state=0, tol= 1e-4,verbose=0)
    SVC.fit(train_image_feats, train_labels)
    
    pred_test_label = SVC.predict(test_image_feats)
    
    return np.array([pred_test_label])


def nearest_neighbor_classify(train_image_feats, train_labels, test_image_feats):
    """
    This function will predict the category for every test image by finding
    the training image with most similar features. You will complete the given
    partial implementation of k-nearest-neighbors such that for any arbitrary
    k, your algorithm finds the closest k neighbors and then votes among them
    to find the most common category and returns that as its prediction.

    Inputs:
        train_image_feats: An nxd numpy array, where n is the number of training
                           examples, and d is the image descriptor vector size.
        train_labels: An nx1 Python list containing the corresponding ground
                      truth labels for the training data.
        test_image_feats: An mxd numpy array, where m is the number of test
                          images and d is the image descriptor vector size.

    Outputs:
        An mx1 numpy list of strings, where each string is the predicted label
        for the corresponding image in test_image_feats

    The simplest implementation of k-nearest-neighbors gives an even vote to
    all k neighbors found - that is, each neighbor in category A counts as one
    vote for category A, and the result returned is equivalent to finding the
    mode of the categories of the k nearest neighbors. A more advanced version
    uses weighted votes where closer matches matter more strongly than far ones.
    This is not required, but may increase performance.

    Be aware that increasing k does not always improve performance - even
    values of k may require tie-breaking which could cause the classifier to
    arbitrarily pick the wrong class in the case of an even split in votes.
    Additionally, past a certain threshold the classifier is considering so
    many neighbors that it may expand beyond the local area of logical matches
    and get so many garbage votes from a different category that it mislabels
    the data. Play around with a few values and see what changes.

    Useful functions:
        scipy.spatial.distance.cdist, np.argsort, scipy.stats.mode
    """


    """ ====================================================================
        k = 1
        m = test_image_feats.shape[0]
        output = np.empty(m, dtype = "S")

        categories = np.unique(train_labels)

        # Gets the distance between each test image feature and each train image feature
        # e.g., cdist
        distances = cdist(test_image_feats, train_image_feats, 'euclidean')

        for each in distances:
            votes = []
            index = np.argsort(each)
            votes.append(train_labels[index[each]])
            max_votes = 0
            for cat in categories:
                if votes.count(cat) > max_votes:
                    result = cat
            output.append(result)

    """
#----------------------------------
    test_predicts = []
    for num in range(test_image_feats.shape[0]):
        each_row = []
        each = np.tile(test_image_feats[num],(train_image_feats.shape[0],1))
        square_each = np.square(each - train_image_feats)
        for sq in range(square_each.shape[0]):
            each_row.append(np.sqrt(sum(square_each[sq])))
        minimum = min(each_row)
        minimum_ind = each_row.index(min(each_row))
        test_predicts.append(train_labels[minimum_ind])

    # TODO:
    # 1) Find the k closest features to each test image feature in euclidean space

    # 2) Determine the labels of those k features
    # 3) Pick the most common label from the k
    # 4) Store that label in a list

    #return output
    return test_predicts

# from keras import backend as K
# from keras.layers import  Layer
import numpy as np
import os.path
import cv2


# class TripletLossLayer(Layer):
#     def __init__(self, alpha, **kwargs):
#         self.alpha = alpha
#         super(TripletLossLayer, self).__init__(**kwargs)
#
#     def triplet_loss(self, inputs):
#         a, p, n = inputs
#         p_dist = K.sum(K.square(a - p), axis=-1)
#         n_dist = K.sum(K.square(a - n), axis=-1)
#         return K.sum(K.maximum(p_dist - n_dist + self.alpha, 0), axis=0)
#
#     def call(self, inputs):
#         loss = self.triplet_loss(inputs)
#         self.add_loss(loss)
#         return loss


class IdentityMetadata():
    def __init__(self, base, type, name, file):
        # dataset base directory
        self.base = base
        # identity people type
        self.type = type
        # identity name
        self.name = name
        # image file name
        self.file = file

    def __repr__(self):
        return self.image_path()

    def image_path(self):
        return os.path.join(self.base, self.type, self.name, self.file)


def load_metadata(path):
    metadata = []
    for i in sorted(os.listdir(path)):
        type = []
        for j in sorted(os.listdir(os.path.join(path, i))):
            person = []
            for k in sorted(os.listdir(os.path.join(path + i, j))):
                # Check file extension. Allow only jpg/jpeg' files.
                ext = os.path.splitext(k)[1]
                if ext == '.jpg' or ext == '.jpeg':
                    person.append(IdentityMetadata(path, i, j, k))
            type.append(person)
        metadata.append(type)
    return np.array(metadata, dtype=object)


def load_image(path):
    img = cv2.imread(path)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    return img[..., ::-1]


def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))

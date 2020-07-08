from model import create_model
from keras import backend as K
from keras.models import Model
from keras.layers import Input, Layer
from data import triplet_generator
import numpy as np
import os.path
import cv2
from align import AlignDlib

alignment = AlignDlib('data/data_dlib/landmarks.dat')

class TripletLossLayer(Layer):
    def __init__(self, alpha, **kwargs):
        self.alpha = alpha
        super(TripletLossLayer, self).__init__(**kwargs)

    def triplet_loss(self, inputs):
        a, p, n = inputs
        p_dist = K.sum(K.square(a - p), axis=-1)
        n_dist = K.sum(K.square(a - n), axis=-1)
        return K.sum(K.maximum(p_dist - n_dist + self.alpha, 0), axis=0)

    def call(self, inputs):
        loss = self.triplet_loss(inputs)
        self.add_loss(loss)
        return loss


class IdentityMetadata():
    def __init__(self, base, name, file):
        # dataset base directory
        self.base = base
        # identity name
        self.name = name
        # image file name
        self.file = file

    def __repr__(self):
        return self.image_path()

    def image_path(self):
        return os.path.join(self.base, self.name, self.file)


def load_metadata(path):
    metadata = []
    for i in sorted(os.listdir(path)):
        person = []
        for f in sorted(os.listdir(os.path.join(path, i))):
            # Check file extension. Allow only jpg/jpeg' files.
            ext = os.path.splitext(f)[1]
            if ext == '.jpg' or ext == '.jpeg':
                person.append(IdentityMetadata(path, i, f))
        metadata.append(person)
    return np.array(metadata,dtype=object)


def load_image(path):
    img = cv2.imread(path, 1)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    return img[..., ::-1]


def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img),
                           landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)


def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))

# if __name__ == '__main__':
#     # nn4_small2 = create_model()
#     #
#     # # Input for anchor, positive and negative images
#     # in_a = Input(shape=(96, 96, 3))
#     # in_p = Input(shape=(96, 96, 3))
#     # in_n = Input(shape=(96, 96, 3))
#     #
#     # # Output for anchor, positive and negative embedding vectors
#     # # The nn4_small model instance is shared (Siamese network)
#     # emb_a = nn4_small2(in_a)
#     # emb_p = nn4_small2(in_p)
#     # emb_n = nn4_small2(in_n)
#     #
#     # # Layer that computes the triplet loss from anchor, positive and negative embedding vectors
#     # triplet_loss_layer = TripletLossLayer(alpha=0.2, name='triplet_loss_layer')([emb_a, emb_p, emb_n])
#     #
#     # # Model that can be trained with anchor, positive negative images
#     # nn4_small2_train = Model([in_a, in_p, in_n], triplet_loss_layer)
#     #
#     # # triplet_generator() creates a generator that continuously returns
#     # # ([a_batch, p_batch, n_batch], None) tuples where a_batch, p_batch
#     # # and n_batch are batches of anchor, positive and negative RGB images
#     # # each having a shape of (batch_size, 96, 96, 3).
#     # generator = triplet_generator()
#     #
#     # nn4_small2_train.compile(loss=None, optimizer='adam')
#     # nn4_small2_train.fit_generator(generator, epochs=1, steps_per_epoch=100)
#
#     # Please note that the current implementation of the generator only generates
#     # random image data. The main goal of this code snippet is to demonstrate
#     # the general setup for model training. In the following, we will anyway
#     # use a pre-trained model so we don't need a generator here that operates
#     # on real training data. I'll maybe provide a fully functional generator
#     # later.
#     nn4_small2_pretrained = create_model()
#     nn4_small2_pretrained.load_weights('weights/nn4.small2.v1.h5')
#
#     metadata = load_metadata('images')
#
#     # Initialize the OpenFace face alignment utility
#
#
#     # # Load an image of Jacques Chirac
#     # jc_orig = load_image(metadata[78].image_path())
#     #
#     # # Detect face and return bounding box
#     # bb = alignment.getLargestFaceBoundingBox(jc_orig)
#     #
#     # # Transform image using specified face landmark indices and crop image to 96x96
#     # jc_aligned = alignment.align(96, jc_orig, bb, landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)
#
#     embedded = np.zeros((metadata.shape[0], 128))
#
#     for i, m in enumerate(metadata):
#         img = load_image(m.image_path())
#         # img = align_image(img)
#         img = cv2.resize(img, (96, 96))
#         # scale RGB values to interval [0,1]
#         try:
#             img = (img / 255.).astype(np.float32)
#             # obtain embedding vector for image
#             embedded[i] = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
#         except:
#             print(m.image_path)
#
#     # show_pair(77, 78)
#     # show_pair(77, 100)
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened():
#         flag, frame = cap.read()
#         kk = cv2.waitKey(1)
#         # 按下 q 键退出
#         if kk == ord('q'):
#             break
#         else:
#             try:
#                 # img = align_image(frame)
#                 frame = cv2.resize(frame, (96, 96))
#                 img = (frame / 255.).astype(np.float32)
#                 img = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
#                 d = []
#                 for i in range(0, len(embedded)):
#                     d.append(distance(embedded[i], img))
#
#                 name = ['Person_2', 'tbs', 'Person_1']
#
#                 print(name[d.index(min(d))])
#                 # if d < 1:
#                 #     print("same face")
#                 # else:
#                 #     print("different face")
#             except Exception as e:
#                 print(e)
#             cv2.imshow("normal", frame)
#     cap.release()
#     cv2.destroyAllWindows()

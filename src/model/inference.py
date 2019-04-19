from fastai.vision import *
from warnings import filterwarnings
# from io import BytesIO
from PIL import Image
import torch
from torch.autograd import Variable
from torchvision import transforms
from annoy import AnnoyIndex


filterwarnings('ignore')
scaler = transforms.Resize((512, 512))
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
to_tensor = transforms.ToTensor()

# number of classes in partial kaggle train set was 228
sz = 512
emb_size = 512
data = ImageDataBunch.single_from_classes('../', range(228), size=sz
                                          ).normalize(imagenet_stats)

learn = cnn_learner(data, models.resnet34)
learn.load('stage-1');
learn.model.eval()
layer = learn.model._modules.get('1')._modules.get('7')


def get_vector(fpath):

    # img = Image.open(BytesIO(binary_data))
    img = Image.open(fpath)

    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    my_embedding = torch.zeros((1, 512))

    def copy_data(m, i, o):
        my_embedding.copy_(o.data)

    h = layer.register_forward_hook(copy_data)
    learn.model(t_img)
    h.remove()

    return my_embedding


t = AnnoyIndex(emb_size)
t.load('../prod.ann')


def get_nn(fpath):
    # returns list of integer indexes
    emb = get_vector(fpath)
    return t.get_nns_by_vector(emb[0], 5)

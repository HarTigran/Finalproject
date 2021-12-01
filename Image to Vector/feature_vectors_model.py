import torch
import numpy as np
import torch.nn as nn
import pytorch_lightning as pl
from torchvision.models import resnet18
from torchvision import transforms
from torchvision.io import read_image
import torchvision.transforms.functional as trsf
import boto3
import io
import pickle
from PIL import Image
from io import BytesIO
import numpy as np
import awswrangler as wr
import os


class Model(pl.LightningModule):
    def __init__(self):
        super(Model, self).__init__()
        self.hidden_layers = 524
        self.resnet = resnet18()
        self.in_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Sequential(
            nn.Linear(self.in_features, self.hidden_layers),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(self.hidden_layers, 196)
        )

    def forward(self, x):
        return self.resnet(x)


model = Model.load_from_checkpoint("trained_model_2021-11-12 19_41_59.859689.ckpt")


class FeatureExtraction(nn.Module):
    def __init__(self, output_layer):
        super().__init__()
        self.output_layer = output_layer
        self.pretrained = model
        self.children_list = []
        for n, c in self.pretrained._modules['resnet'].named_children():
            self.children_list.append(c)
            if n == self.output_layer:
                break

        self.net = nn.Sequential(*self.children_list)
        self.pretrained = None

    def forward(self, x):
        x = self.net(x)
        return x


f_model = FeatureExtraction("avgpool")
f_model.eval()

if __name__ == '__main__':
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.Lambda(lambda x: x / 255.)
    ])
    

    s3 = boto3.resource('s3')#,aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
    bucket = s3.Bucket('images-from-web')
    # object = bucket.Object('img-lst.jpeg')
    # response = object.get()
    # file_stream = response['Body']
    # img = Image.open(file_stream).convert('RGB')
    # img = trsf.to_tensor(img)
    # img = transform(img)
    # p1 = f_model(img.unsqueeze(0))
    # assert p1.shape == torch.Size([1, 512, 1, 1])
    
    all_images = wr.s3.list_objects('s3://images-from-web/*.jpg')
    images_list = []
    images_name = []
    for image in all_images:
        object = bucket.Object(image.split('/')[-1])
        response = object.get()
        file_stream = response['Body']
        img = Image.open(file_stream).convert('RGB')
        img = trsf.to_tensor(img)
        img = transform(img)
        if img.shape == torch.Size([3, 256, 256]):
            p = f_model(img.unsqueeze(0)).squeeze(-1).squeeze(-1).detach().numpy()
            images_list.append(p)
            images_name.append(image)
    images_list = np.concatenate(images_list, axis=0)
    images_name = np.array(images_name)

    s3_client = boto3.client('s3')

    # upload without using disk
    my_array_data = io.BytesIO()
    pickle.dump(images_list, my_array_data)
    my_array_data.seek(0)
    s3_client.upload_fileobj(my_array_data, 'images-from-web', 'test_vectors.pkl')

    my_array_data = io.BytesIO()
    pickle.dump(images_name, my_array_data)
    my_array_data.seek(0)
    s3_client.upload_fileobj(my_array_data, 'images-from-web', 'test_names.pkl')
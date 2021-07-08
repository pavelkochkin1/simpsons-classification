import pickle
import numpy as np

from torchvision import models
from torch import nn

from model.utils import *

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

class MobNetSimpsons():
    def __init__(self):
        print("Loading model...")
        self.model = models.mobilenet_v3_large(pretrained=True)
        num_features = 960
        n_classes = 42
        self.model.classifier = nn.Sequential(
            nn.Linear(num_features, 1280, bias=True),
            nn.Hardswish(),
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(1280, n_classes, bias=True) 
        )
        print("Seting parameters...")
        self.model.load_state_dict(torch.load('model/mobNetLarge.pth', map_location=DEVICE))
        print("Seting on evaluation mode...")
        self.model.eval()

        self.label_encoder = pickle.loads(open('model/label_encoder.pkl', 'rb').read())
        print("Model is ready!")

    def predict(self, image_path):
        img = prepare_img(image_path)

        proba = predict_one_sample(self.model, img, device=DEVICE)
        predicted_proba = np.max(proba)*100
        y_pred = np.argmax(proba)

        label = self.label_encoder.inverse_transform([y_pred])[0].split('_')
        label = label_to_string(label)

        return [label, predicted_proba]



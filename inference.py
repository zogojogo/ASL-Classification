from PIL import Image
import torch, json, sys, argparse
from torchvision import transforms
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Image path input")
args = parser.parse_args()
#Image Acquisition
img_path = args.path
image = Image.open(img_path).convert('RGB')

#Initiate Labels
with open("labels.json") as f:
    labels = json.load(f)

#Image Pre-process
data_transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
image_transformed = data_transform(image).unsqueeze(0)    

#Load Model
model = torch.load('saved_model.pt', map_location=torch.device('cpu'))
model.eval()

#Inference Model
out = model(image_transformed)

#Visualize Model
plt.imshow(image), plt.xticks([]), plt.yticks([])
plt.xlabel("Predicted class is: {}".format(labels[out.argmax()]))
plt.show()

print("Predicted class is: {}".format(labels[out.argmax()]))
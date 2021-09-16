from numpy.lib.shape_base import expand_dims
from torchvision import transforms
from PIL import Image
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os

import vortex.runtime as vrt

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Image path input")
parser.add_argument("-m", "--model_path", help="Choose what model u want to use (.onnx only)")
args = parser.parse_args()

def predict(img_path, export_path):
    runtime_device = 'cpu'
    img = Image.open(img_path).convert('RGB')
    #Transfor Image
    data_transform = transforms.Compose([
        transforms.Resize((224, 224)), 
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    new_img = data_transform(img)
    new_img = np.array(new_img)
    new_img = expand_dims(new_img, 0)
    #Prepare Model
    model = vrt.create_runtime_model(model_path=export_path, runtime=runtime_device)
    results = model(new_img)
    predicted_class = model.class_names[int(results[0]['class_label'].squeeze())]
    confidence = results[0]['class_confidence'].squeeze()
    return predicted_class, confidence, img

def show_result(predicted_class, confidence, img):
    plt.imshow(img), plt.xticks([]), plt.yticks([])
    plt.xlabel("Predicted class is: {} with {:2f} confidence".format(predicted_class, confidence))
    plt.show()
    print('Class Detected : {}'.format(predicted_class))
    print('Confidence : {:2f}'.format(confidence))

#Run inference
predicted_class, confidence, img = predict(args.path, args.model_path)
show_result(predicted_class, confidence, img)

#Show & Predict All Images in Test Data

# outputs = []
# for img in os.listdir('./Test Data'):
#     outputs.append(img)
# outputs.sort()

# for i in range(len(outputs)):
#     predicted_class, confidence, img = predict(os.path.join('Test Data/',outputs[i]), 'model_asl2.onnx')
#     plt.subplot(6,5,i+1)
#     plt.suptitle('Try with Test Data', fontsize=18)
#     plt.imshow(img)
#     plt.xlabel("Class : {} with {:2f} confidence".format(predicted_class, confidence))
#     plt.grid(None) 
#     plt.xticks([])
#     plt.yticks([])
# plt.rcParams["figure.figsize"] = (20,15)
# plt.show()
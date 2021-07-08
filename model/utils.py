import torch
from PIL import Image
from torchvision import transforms

SIZE = 256

def prepare_img(image_path):
    """Prepare image for model"""
    img = Image.open(image_path)
    img.load()

    transform = transforms.Compose([
        transforms.Resize((SIZE,SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    img = transform(img)
    img = img.view(1, 3, 256, 256)
    
    return img

def predict_one_sample(model, inputs, device):
    """Predict probabilities"""
    with torch.no_grad():
        inputs = inputs.to(device)
        model.eval()
        logit = model(inputs).cpu()
        probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
    return probs

def label_to_string(label):
    """Turn label to string"""
    s=''
    for a in label:
        s+=a+' '
    return s


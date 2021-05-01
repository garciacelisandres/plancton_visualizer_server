# Check that we have everything here
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as nnf
import torchvision
import torchvision.transforms as T
from PIL import Image
from natsort import natsorted
from torch.utils.data import Dataset, DataLoader

from database.database_api import get_db, init_db

if not os.path.isdir("../quantificationlib"):
    print("You should have the quantification library in this directory")
    sys.exit()


# Receiving the sample to quantify
class ProductionDataset(Dataset):
    def __init__(self, main_dir, transform):
        self.main_dir = main_dir
        self.transform = transform
        all_imgs = os.listdir(main_dir)
        self.total_imgs = natsorted(all_imgs)

    def __len__(self):
        return len(self.total_imgs)

    def __getitem__(self, idx):
        img_loc = os.path.join(self.main_dir, self.total_imgs[idx])
        image = Image.open(img_loc).convert("RGB")
        tensor_image = self.transform(image)
        return tensor_image


def build_sample(filename: str) -> (str, datetime):
    name = filename.split("/")[-1].replace(".zip", "")
    day_hour_list = name.split("_")[0]
    try:
        date_from_name = datetime.strptime(day_hour_list, "D%Y%m%dT%H%M%S")
    except ValueError:
        date_from_name = datetime.now()
    return name, date_from_name


# Adding all neccesary functions
def load_network(device):
    num_classes = 51
    model = torchvision.models.resnet18(pretrained=True)
    print("Adjusting the CNN for %s classes" % num_classes)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    # Define loss function
    loss_fn = nn.CrossEntropyLoss()
    model.load_state_dict(torch.load("../model.pt"))
    model = model.to(device)  # Send model to gpu
    return model, loss_fn


def make_preds(model, loader, device):
    """
    Check the accuracy of the model.
    """
    with torch.no_grad():
        # Set the model to eval mode
        model.eval()
        y_pred = []
        y_probs = []
        for x in loader:
            x = x.to(device)
            # Run the model forward, and compare the argmax score with the ground-truth
            # category.
            output = model(x)
            predicted = output.argmax(1)
            prob = nnf.softmax(output, dim=1)
            y_probs.extend(prob.cpu().detach().numpy())
            y_pred.extend(predicted.cpu().numpy())
    return y_pred, y_probs


def predict(filename):
    # Load the data
    trainpreds = np.genfromtxt('../results/trainpred.csv', delimiter=',')
    traintrue = np.genfromtxt('../results/traintrue.csv', delimiter=',')
    trainprobs = np.genfromtxt('../results/trainprobs.csv', delimiter=',')
    classes = np.genfromtxt('../results/classes.csv', dtype='str')

    # Fit quantification models
    sys.path.insert(0, os.path.abspath("../quantificationlib"))
    from quantificationlib import classify_and_count, distribution_matching

    quantifier_cc = classify_and_count.CC(verbose=1)
    quantifier_ac = classify_and_count.AC(verbose=1)
    quantifier_hdy = distribution_matching.DFy(verbose=1)
    quantifier_cc.fit(None, traintrue, predictions_train=trainpreds)
    quantifier_ac.fit(None, traintrue, predictions_train=trainprobs)
    quantifier_hdy.fit(None, traintrue, predictions_train=trainprobs)

    prod_transform = T.Compose([
        T.Resize(size=256),
        T.CenterCrop(size=224),
        T.ToTensor(),
        # T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    # This directory should be the directory with the new images... using validation for simplicity here
    prod_dset = ProductionDataset("../production", transform=prod_transform)
    prod_loader = DataLoader(prod_dset, batch_size=256, num_workers=4)
    print("Loaded %d images " % len(prod_dset))

    if not len(prod_dset) > 1:
        print("Skipping the prediction operation: too few images downloaded.")
        return

    # Classify the sample and then quantify it
    pd.set_option('display.float_format', lambda x: '%.5f' % x)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Using %s" % device)

    model, _ = load_network(device)
    y_pred, y_probs = make_preds(model, prod_loader, device)
    y_pred = np.vstack(y_pred)
    y_probs = np.vstack(y_probs)

    results_cc = quantifier_cc.predict(None, predictions_test=y_pred)
    results_ac = quantifier_ac.predict(None, predictions_test=y_pred)
    results_hdy = quantifier_hdy.predict(None, predictions_test=y_probs)

    sample_dict = pd.DataFrame({"CC": results_cc, "AC": results_ac, "HDy": results_hdy}, index=classes)\
        .to_dict("index")
    (name, date_retrieved) = build_sample(filename)

    get_db().insert_sample(name, date_retrieved, sample_dict)

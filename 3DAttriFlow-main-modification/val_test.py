import argparse
import open3d
import torch
import munch
import yaml
from dataset_svr.trainer_dataset import build_dataset_val
import torch
from utils.train_utils import *
import logging
import importlib
import random
import munch
import yaml
import os
from utils.model_utils import *
from tqdm import tqdm
import cv2
import torchvision.transforms as transforms
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

def club(points,path):
    points = torch.squeeze(points,0)

    points = points.cpu().detach().numpy()
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(points)
    
    open3d.io.write_point_cloud(path, pcd)

def photo(image_path):
        image = Image.open(image_path)
        cv2.imwrite("./image.jpg",np.asarray(image))




def val():
    
    # dataloader_test = build_dataset_val(args)

    if not args.manual_seed:
        seed = random.randint(1, 10000)
    else:
        seed = int(args.manual_seed)
    logging.info('Random Seed: %d' % seed)
    random.seed(seed)
    torch.manual_seed(seed)

    model_module = importlib.import_module('.%s' % args.model_name, 'models')
    # print('.%s' % args.model_name, 'models')
    net = torch.nn.DataParallel(model_module.Model(args))
    # print("*************")
    # print(model_module.Model(args))
    
    net.cuda()
    if hasattr(model_module, 'weights_init'):
        net.module.apply(model_module.weights_init)
    
    ckpt = torch.load(args.load_model)
    net.module.load_state_dict(ckpt['net_state_dict'])
    logging.info("%s's previous weights loaded." % args.model_name)

    net.module.eval()

    logging.info('Testing...')

    test_loss_l1 = AverageValueMeter()
    test_loss_l2 = AverageValueMeter()
    image_path = "date/ShapeNetV1Renderings/01111122/1a010000/rendering/10.png"
    photo(image_path)
    image = Image.open(image_path)
    cv2.imwrite("./image.jpg",np.asarray(image))
    transform = transforms.Compose([
            transforms.Resize(size=224, interpolation=2),
            transforms.ToTensor(),])
    image = transform(image)
    image = image[:3, :, :]
    image = image.unsqueeze(0)
    image = image.cuda()
    pred_points = net(image)
    club(pred_points,"./predict_test.ply")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train config file')
    parser.add_argument('-c', '--config', help='path to config file', required=True)
    parser.add_argument('-gpu', '--gpu_id', help='gpu_id', required=True)
    arg = parser.parse_args()
    config_path = arg.config
    args = munch.munchify(yaml.safe_load(open(config_path)))

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(arg.gpu_id)
    print('Using gpu:' + str(arg.gpu_id))

    val()

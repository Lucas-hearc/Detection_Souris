import matplotlib.pyplot as plt
from config import Config
import utils
import model as modellib
import visualize
from model import log
from PIL import Image, ImageDraw
import warnings
import tensorflow as tf
from datetime import datetime

class CustomConfig(Config):

    def __init__(self, num_classes):
        classes_number = num_classes
        super().__init__()

    NAME = "object"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 4
    NUM_CLASSES = 1
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    STEPS_PER_EPOCH = 500
    VALIDATION_STEPS = 5
    ETF_C = 2
    DETECTION_MIN_CONFIDENCE = 0.9

class InferenceConfig(CustomConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def load_inference_model(num_classes, model_path):
    inference_config = InferenceConfig(num_classes)
    model = modellib.MaskRCNN(config=inference_config, model_dir=model_path)
    model.load_weights(model_path, by_name=True)
    return model, inference_config
from pydarknet import Detector, Image

def get_model(data_dir, cfg_dir, weights_dir):
    return Detector(bytes(cfg_dir, encoding="utf-8"), 
                    bytes(weights_dir, encoding="utf-8"), 
                    0, 
                    bytes(data_dir,encoding="utf-8"))

def detect(model, image):
    parsed_img = Image(image)
    return model.detect(parsed_img)
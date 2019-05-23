import darknet

def get_model(data_dir, cfg_dir, weights_dir):
    net = darknet.load_net(cfg_dir.encode('utf-8'), weights_dir.encode('utf-8'), 0)
    meta = darknet.load_meta(data_dir.encode('utf-8'))
    return net, meta

def detect(model, img_dir):
    return darknet.detect(model[0], model[1], img_dir.encode('utf-8'))
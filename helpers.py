import utils
import time
import models
import os
import numpy as np
import json
import train


def show_plot(train_config_file, opt=1):
    training_config = train.TrainingConfig.load_from_file(train_config_file)

    # Model initialization
    model = training_config.get_by_model_key(False)
    checkpoint = models.ModelCheckpoint(model)
    checkpoint.load(training_config.get_model_path('checkpoint'))
    if not checkpoint.loaded:
        print('Not evaluated')
        return

    if opt == 1:
        utils.plot_learning_curve(checkpoint.training_losses, checkpoint.cv_losses, close=True)
    elif opt == 2:
        utils.plot_learning_curve(checkpoint.cv_accuracies, checkpoint.model_specific['polled_accuracies'], close=True)
    else:
        return
    time.sleep(60)


def hp_grid_vgg16():
    size = 10
    lrs = 10 ** np.random.uniform(-5, 0, size).astype(np.float32)
    moms = np.random.choice([0.9, 0.9, 0.98], size)
    bns = np.random.choice(['true', 'false'], size)
    batch_sizes = np.random.choice([32, 64, 64, 128], size)

    hp_tune_dir = 'models/vgg16_hp_tuning_full'

    for i, item in enumerate(zip(lrs, moms, bns, batch_sizes)):
        print(i, item)
        lr, mom, bn, batch_size = item
        data = {
            "name": "vgg16_reduced_dims_hp_{}".format(i + 1),
            "num_epochs": 15,
            "batch_size": batch_size,
            "resume": True,
            "models_dir": os.path.join(hp_tune_dir, 'hp_{}'.format(i + 1)),
            "dataset_path": "datasets/processed/mfcc_vgg16_fma_small_full/mfcc_vgg16_fma_small_full",
            "model": "VGG16_reduced",
            "model_params": {
                "num_classes": 8,
                "pretrained": True,
                "lr": lr,
                "momentum": mom,
                "batchnorm": bn
            }
        }
        os.makedirs(os.path.join(hp_tune_dir, 'hp_{}'.format(i + 1)), exist_ok=True)
        with open(os.path.join(hp_tune_dir, 'hp_{}/config.json'.format(i + 1)), 'w') as cfile:
            json.dump(data, cfile)
    configs = [os.path.join(hp_tune_dir, 'hp_{}/config.json'.format(i + 1)) for i in range(size)]
    with open(os.path.join(hp_tune_dir, 'hp_{}/hp_config.txt'), 'w') as cfile:
        cfile.write('\n'.join(configs))


def hp_grid_conv_ae():
    needed = 10
    size = 100
    lrs = 10 ** np.random.uniform(-4.5, -0.5, size).astype(np.float32)
    moms = np.random.choice([0.9, 0.95, 0.99], size)
    batch_sizes = np.random.choice([32, 64, 64, 128], size)
    num_init_filters = np.random.choice([16, 32, 32, 64], size)
    num_pools = np.random.choice([2, 3, 4, 5], size)
    num_fcs = np.random.choice([2, 3, 4], size)
    fc_scale_downs = np.random.choice([2, 4, 8, 16], size)
    kernel_sizes = np.random.choice([3, 5], size)

    max_params = 5000000

    hp_tune_dir = 'models/conv_ae_hp_tuning_skip_shared'

    done = 0
    for i, item in enumerate(
            zip(lrs, moms, batch_sizes, num_init_filters, num_pools, num_fcs, fc_scale_downs, kernel_sizes)):
        print(i, item)
        lr, mom, batch_size, num_init_filter, num_pool, num_fc, fc_scale_down, kernel_size = item
        data = {
            "name": "conv_ae_skip_shared_{}".format(done + 1),
            "num_epochs": 10,
            "batch_size": int(batch_size),
            "resume": True,
            "models_dir": os.path.join(hp_tune_dir, 'hp_{}'.format(done + 1)),
            "dataset_path": "datasets/processed/mfcc_ae_fma_small_full/mfcc_ae_fma_small_full",
            "model": "conv_ae",
            "model_params": {
                "lr": float(lr),
                "momentum": float(mom),
                "input_dims": [64, 96],
                "enc_len": 10,
                "num_init_filters": int(num_init_filter),
                "num_pools": int(num_pool),
                "num_fc": int(num_fc),
                "fc_scale_down": int(fc_scale_down),
                "kernel_size": int(kernel_size),
                "padding": int(kernel_size / 2),
                "shared_weights": True,
                "skip_connections": True,
                "enc_activation": "sigmoid"
            }
        }
        try:
            config = train.TrainingConfig()
            config.__dict__ = data
            model = config.get_by_model_key(False)
        except Exception as ex:
            print('Error:', ex)
            continue

        num_params = utils.get_trainable_params(model.model)
        if num_params > max_params:
            print('Too many params', num_params)

        os.makedirs(os.path.join(hp_tune_dir, 'hp_{}'.format(done + 1)), exist_ok=True)
        with open(os.path.join(hp_tune_dir, 'hp_{}/config.json'.format(done + 1)), 'w') as cfile:
            json.dump(data, cfile, indent=2)
        done += 1
        if done >= needed:
            break
    if done < needed:
        raise Exception('Could not complete')
    configs = [os.path.join(hp_tune_dir, 'hp_{}/config.json'.format(i + 1)) for i in range(needed)]
    with open(os.path.join(hp_tune_dir, 'hp_config.txt'), 'w') as cfile:
        cfile.write('\n'.join(configs))
import yaml
import os


def load_config(path):
    with open(path,'r',encoding='utf-8') as fl:
        cfg=yaml.load(fl.read())
        return cfg
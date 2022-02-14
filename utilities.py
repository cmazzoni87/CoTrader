import os
import logging

log = logging.getLogger('root')

def make_dir(parent_dir, base_dir):
    #Make directory if it doesn't exist
    dir_name = os.path.join(parent_dir, base_dir)
    if not os.path.isdir(dir_name):
        log.info("Creating directory {}".format(dir_name))
        os.makedirs(dir_name, exist_ok=True)
    return dir_name

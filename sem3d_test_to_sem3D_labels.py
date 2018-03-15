import numpy as np
import os
import scipy.misc
from tqdm import *
import json

from pointcloud_tools.lib.python.PcTools import Semantic3D

# load the configuration file and define variables
print("Loading configuration file")
import argparse
parser = argparse.ArgumentParser(description='Semantic3D')
parser.add_argument('--config', type=str, default="config.json", metavar='N',
help='config file')
args = parser.parse_args()
json_data=open(args.config).read()
config = json.loads(json_data)

input_dir = config["test_input_dir"]
voxel_size = config["voxel_size"]
output_dir = config["output_directory"]

filenames = [
        "bildstein_station1_xyz_intensity_rgb",
        "bildstein_station3_xyz_intensity_rgb",
        "bildstein_station5_xyz_intensity_rgb"
    ]

# create outpu directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in filenames:
    print(filename)

    semantizer = Semantic3D()
    semantizer.set_voxel_size(voxel_size)

    mesh_filename = os.path.join(output_dir, filename+".ply")
    sem3d_cloud_txt = os.path.join(input_dir,filename+".txt")
    output_results = os.path.join(output_dir, filename+".txt")
    score_filename = os.path.join(output_dir, filename+"_scores.npz")

    semantizer.mesh_to_label_file_no_labels(mesh_filename,sem3d_cloud_txt,output_results)

    # jaesik added to use our framework
    new_folder = os.path.join(output_dir, filename)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    # print("sudo mkdir " + new_folder)
    # print("sudo mv " + mesh_filename + " " + os.path.join(new_folder, "scan0.ply"))
    # print("sudo mv " + output_results + " " + os.path.join(new_folder, "out.labels"))
    # print("sudo mv " + score_filename + " " + os.path.join(new_folder, "score.npz"))
    os.rename(mesh_filename, os.path.join(new_folder, "scan0.ply"))
    os.rename(output_results, os.path.join(new_folder, "out.labels"))
	os.rename(score_filename, os.path.join(new_folder, "score.npz"))

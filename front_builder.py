import os
import subprocess

from settings import base_dir, dist_folder


def check_dist_folder(force_update: bool = False):
    # Replace with the actual path to your "dist" folder
    if not os.path.exists(dist_folder):
        print("Error: 'dist' folder does not exist.")
        return
    dist_contents = os.listdir(dist_folder)
    if "index.html" not in dist_contents or force_update:
        os.chdir(os.path.join(base_dir, "pickvibe"))
        subprocess.run(["npm", "run", "build"], check=True)
        subprocess.run(["rm", "-vr", dist_folder], check=True)
        subprocess.run(["cp", "-vrf", "dist", ".."], check=True)
        os.chdir(base_dir)
        print("Subprocess executed.")
    else:
        print("'index.html' file found in 'dist' folder.")

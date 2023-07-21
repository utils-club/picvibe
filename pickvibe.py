"""Publish contents
"""
import os
import argparse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from subprocess import Popen
import subprocess


repo_pref = "rp"
pool = []
base_dir = os.path.dirname(__file__)
dist_folder = os.path.join(base_dir, 'dist')


def get_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder_path", help="Folder path to be mounted as static repo")
    parser.add_argument("--update", help="Update front", type=bool, default=False)
    args = parser.parse_args()
    return args


def check_dist_folder(force_update:bool = False):
      # Replace with the actual path to your "dist" folder
    if not os.path.exists(dist_folder):
        print("Error: 'dist' folder does not exist.")
        return
    dist_contents = os.listdir(dist_folder)
    if "index.html" not in dist_contents or force_update:
        os.chdir(os.path.join(base_dir, 'pickvibe'))
        subprocess.run(["npm", 'run', 'build'], check=True)
        subprocess.run(["rm", '-vr', dist_folder], check=True)
        subprocess.run(["cp", '-vrf', 'dist', '..'], check=True)
        os.chdir(base_dir)
        print("Subprocess executed.")
    else:
        print("'index.html' file found in 'dist' folder.")


app = FastAPI()



origins = [
    "http://localhost:9090",
    "http://localhost:8080",
    'http://localhost:5173',
    "http://0.0.0.0:9090",
    "http://0.0.0.0:8080",
    "http://0.0.0.0:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


args = get_args()
target_folder = os.path.abspath(args.folder_path)


@app.on_event("startup")
def startup_event():
    check_dist_folder(force_update=args.update)
    static_app_process = Popen(
        [
            "python3",
            "-m",
            "http.server",
            "8080",
            "-b",
            "0.0.0.0",
            "-d",
            os.path.join(base_dir, "dist"),
        ]
    )
    pool.append(static_app_process)


@app.on_event("shutdown")
def shutdown_event():
    for p in pool:
        p.kill()


# Mount static repo
app.mount(f"/{repo_pref}", StaticFiles(directory=target_folder), name="static")


@app.get("/flds")
async def get_folders():
    # Logic to retrieve list of folders inside the given folder path
    # You can use os.listdir(args.folder_path) or any other method
    folders = [
        a
        for a in os.listdir(target_folder)
        if os.path.isdir(os.path.join(target_folder, a))
    ]
    return {"folders": folders}


@app.get("/rs/{folder}")
async def get_files(folder: str):
    # Logic to retrieve list of files inside the given folder path
    # You can use os.listdir(args.folder_path) or any other method
    contents = [
        a
        for a in os.listdir(os.path.join(target_folder, folder))
        if os.path.isfile(os.path.join(target_folder, folder, a))
    ]
    return {"files": contents}


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application on 0.0.0.0:9090
    uvicorn.run(app, host="0.0.0.0", port=9090)

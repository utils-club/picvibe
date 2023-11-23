import os


import random

from subprocess import Popen
from datetime import datetime


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from settings import origins, base_dir, repo_pref
from front_builder import check_dist_folder
from models import Note
from service import MediaStreamService

pool = []


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

core = MediaStreamService()


@app.on_event("startup")
def startup_event():
    """Build frontend if dont exists or need to be updated
    and run a static server to serve frontend
    """
    check_dist_folder(force_update=core.args.update)
    static_app_process = Popen(
        [
            "python3",
            "-m",
            "http.server",
            "4070",
            "-b",
            "0.0.0.0",
            "-d",
            os.path.join(base_dir, "dist"),
        ]
    )
    pool.append(static_app_process)


@app.on_event("shutdown")
def shutdown_event():
    """Kill frontend static server"""
    for p in pool:
        p.kill()


# Mount static repo
app.mount(f"/{repo_pref}", StaticFiles(directory=core.args.folder_path), name="static")


@app.get("/flds")
async def get_folders():
    """Logic to retrieve list of folders inside the given folder path
    You can use os.listdir(args.folder_path) or any other method
    """
    return core.get_folders()


@app.get("/rs/{folder}")
async def get_files(folder: str):
    """Logic to retrieve list of files inside the given folder path
    You can use os.listdir(args.folder_path) or any other method
    """
    return core.get_files_in_folder(folder)


@app.post("/note/")
async def create_note(note: Note):
    await core.tag_resource(note)


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application on 0.0.0.0:9090
    uvicorn.run(app, host="0.0.0.0", port=4071)

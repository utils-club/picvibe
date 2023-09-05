import os


import random

from subprocess import Popen
from datetime import datetime


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from settings import origins, base_dir, repo_pref
from interface import get_args
from front_builder import check_dist_folder
from models import Note


pool = []


app = FastAPI()


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
    """Build frontend if dont exists or need to be updated
    and run a static server to serve frontend
    """
    check_dist_folder(force_update=args.update)
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
app.mount(f"/{repo_pref}", StaticFiles(directory=target_folder), name="static")


@app.get("/flds")
async def get_folders():
    """Logic to retrieve list of folders inside the given folder path
    You can use os.listdir(args.folder_path) or any other method
    """
    folders = [
        a
        for a in os.listdir(target_folder)
        if os.path.isdir(os.path.join(target_folder, a))
    ]
    return {"folders": folders}


@app.get("/rs/{folder}")
async def get_files(folder: str):
    """Logic to retrieve list of files inside the given folder path
    You can use os.listdir(args.folder_path) or any other method
    """
    contents = [
        a
        for a in os.listdir(os.path.join(target_folder, folder))
        if os.path.isfile(os.path.join(target_folder, folder, a))
    ]
    current_time = datetime.now()
    random.seed(current_time.year + current_time.day + current_time.month)
    random.shuffle(contents)
    return {"files": contents}


@app.post("/note/")
async def create_note(note: Note):
    try:
        with open("tags.txt", "a") as file:
            file.write(f"{note.model_dump_json()}\n")
        return {"succeded": True}
    except Exception as e:
        return {"succeded": False}


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application on 0.0.0.0:9090
    uvicorn.run(app, host="0.0.0.0", port=4071)

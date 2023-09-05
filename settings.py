import os

repo_pref = "rp"
base_dir = os.path.dirname(__file__)
dist_folder = os.path.join(base_dir, "dist")

origins = [
    "http://localhost:9090",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://0.0.0.0:9090",
    "http://0.0.0.0:8080",
    "http://0.0.0.0:5173",
    "http://192.168.20.57:9090",
    "http://192.168.20.57:4070",
    "http://192.168.20.57:4071",
    "http://192.168.20.57:8080",
    "http://192.168.20.57:5173",
]

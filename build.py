import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from typing import Union


def download(url: str) -> bytes:
    response = urllib.request.urlopen(url)
    return response.read()  # a `bytes` object


def write(path: str, payload: Union[str, bytes], mode: str = "wb"):
    with open(path, mode=mode) as f:
        f.write(payload)


def build(kwargs):
    hackrf_src_url = "https://github.com/mossmann/hackrf/releases/download/v2021.03.1/hackrf-2021.03.1.tar.xz"
    _, tar_name = hackrf_src_url.rsplit("/", 1)
    unpacked_name, _, _ = tar_name.rsplit(".", 2)
    write(tar_name, download(hackrf_src_url))
    print(tar_name, unpacked_name)

    with tempfile.TemporaryDirectory(prefix="pyhackrf") as tmp_dir_name:
        src_dir = f"{tmp_dir_name}/{unpacked_name}"
        host_dir = f"{src_dir}/host"
        build_dir = f"{host_dir}/build"
        print("tmp_dir_name", tmp_dir_name)
        subprocess.run(["tar", "-vxf", tar_name, "-C", tmp_dir_name], stderr=sys.stderr, stdout=sys.stdout)
        shutil.rmtree(build_dir, ignore_errors=True)
        os.makedirs(build_dir, exist_ok=True)
        subprocess.run(["cmake", ".."], stderr=sys.stderr, stdout=sys.stdout, cwd=build_dir)
        subprocess.run(["make"], stderr=sys.stderr, stdout=sys.stdout, cwd=build_dir)
        subprocess.run(["sudo", "make", "install"], stderr=sys.stderr, stdout=sys.stdout, cwd=build_dir)
        subprocess.run(["sudo", "ldconfig"], stderr=sys.stderr, stdout=sys.stdout, cwd=build_dir)

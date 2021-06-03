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


def install_cmake():
    """
    wget https://cmake.org/files/v3.20/cmake-3.20.3.tar.gz
    tar -xzvf cmake-3.20.3.tar.gz
    cd cmake-3.20.3/
    ./bootstrap
    make -j4
    sudo make install
    cmake --version
    :return:
    """
    cmake_src_url = "https://cmake.org/files/v3.20/cmake-3.20.3.tar.gz"
    _, tar_name = cmake_src_url.rsplit("/", 1)
    unpacked_name, _, _ = tar_name.rsplit(".", 2)
    with tempfile.TemporaryDirectory(prefix="pyhackrf-cmake") as tmp_dir_name:
        write(tar_name, download(cmake_src_url))
        src_dir = f"{tmp_dir_name}/{unpacked_name}"
        subprocess.run(["tar", "-vxzf", tar_name, "-C", tmp_dir_name], stderr=sys.stderr, stdout=sys.stdout)
        subprocess.run(["./bootstrap"], stderr=sys.stderr, stdout=sys.stdout, cwd=src_dir)
        subprocess.run(["make", "-j4"], stderr=sys.stderr, stdout=sys.stdout, cwd=src_dir)
        subprocess.run(["sudo", "make", "install"], stderr=sys.stderr, stdout=sys.stdout, cwd=src_dir)
        subprocess.run(["cmake", "--version"], stderr=sys.stderr, stdout=sys.stdout)


def build(kwargs):
    if not shutil.which("cmake"):
        install_cmake()
    install_hackrf()


def install_hackrf():
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

import logging
import os, os.path
from string import Template
from urllib.error import HTTPError
from urllib.request import urlretrieve
from zipfile import ZipFile

from downloadsupport import DownloadSupportMixin, Checksums, ChecksumResult

log = logging.getLogger("llmbench")

class LlamaCppBinary(DownloadSupportMixin):

    LLAMA_CPP_URL_TEMPLATE = Template("https://github.com/ggerganov/llama.cpp/releases/download/b$LLAMA_CPP_VERSION/llama-b$LLAMA_CPP_VERSION-bin-$OS-$ENGINE-$ARCH.zip")

    def __init__(self, engine: str, os: str, arch: str, llama_cpp_version: str, working_dir: str):
        self.engine = engine
        self.os = os
        self.arch = arch
        self.llama_cpp_version = llama_cpp_version
        self.llama_cpp_variant = None
        self.working_dir = working_dir
        self.zip_dir = f"{working_dir}/downloads"
        self.general_bin_dir = f"{working_dir}/bin"
        self.bin_dir = None
        self.zip_filename = None


    def download(self) -> bool:
        url = self.LLAMA_CPP_URL_TEMPLATE.substitute({
            "ENGINE": self.engine,
            "OS": self.os,
            "ARCH": self.arch,
            "LLAMA_CPP_VERSION": self.llama_cpp_version,
        })
        if not os.path.isdir(self.zip_dir):
            os.mkdir(self.zip_dir)
        filename = url.split("/")[-1]
        full_filename = self.zip_dir + "/" + filename
        if not os.path.exists(full_filename):
            log.info(f"Downloading {filename}")
            try:
                urlretrieve(url, filename=full_filename, reporthook=self.download_progress)
            except HTTPError as e:
                log.error(f"Error downloading {url}: {e}")
                return False
        else:
            log.info(f"{filename} already exists.")
        if cresult := Checksums.check_file(full_filename) != ChecksumResult.RESULT_OK:
            log.warning(f"Checksum error for {filename}: {cresult}")
        self.zip_filename = full_filename
        self.llama_cpp_variant = filename[:-4]
        return True


    def extract(self) -> bool:
        if not os.path.isdir(self.general_bin_dir):
            os.mkdir(self.general_bin_dir)
        self.bin_dir = f"{self.general_bin_dir}/{self.llama_cpp_variant}"
        if os.path.isdir(self.bin_dir):
            log.info(f"{self.bin_dir} already exists.")
            return True
        try:
            zip = ZipFile(self.zip_filename)
            zip.extractall(self.bin_dir)
        except Exception as e:
            log.error(f"Error unpacking {self.zip_filename}: {e}")
            return False
        return True

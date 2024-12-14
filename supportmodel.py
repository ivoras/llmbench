import logging
import sys, os, os.path
from urllib.error import HTTPError
from urllib.request import urlretrieve

from config import ModelDescription
from downloadsupport import DownloadSupportMixin, Checksums, ChecksumResult

log = logging.getLogger("llmbench")

class GGUFModel(DownloadSupportMixin):

    def __init__(self, md: ModelDescription, working_dir: str):
        self.md = md
        self.model_dir = f"{working_dir}/models"
        if not os.path.isdir(self.model_dir):
            os.mkdir(self.model_dir)
        self.model_filename = md.url.split("/")[-1]
        self.model_full_filename = f"{self.model_dir}/{self.model_filename}"


    def download(self) -> bool:
        if not os.path.exists(self.model_full_filename):
            log.info(f"Downloading {self.model_filename}")
            try:
                urlretrieve(self.md.url, filename=self.model_full_filename, reporthook=self.download_progress)
            except HTTPError as e:
                log.error(f"Error downloading {self.md.url}: {e}")
                return False
        else:
            log.info(f"{self.model_filename} already exists.")
        if cresult := Checksums.check_file(self.model_full_filename) != ChecksumResult.RESULT_OK:
            log.warning(f"Checksum error for {self.model_filename}: {cresult}")
        return True

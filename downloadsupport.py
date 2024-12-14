import hashlib
import os, os.path, sys
from enum import IntEnum
import logging


log = logging.getLogger("llmbench")


class DownloadSupportMixin:

    def download_progress(self, nblock: int, bsize: int, total: int):
        current_bytes = nblock * bsize
        print(f"{(current_bytes / total)*100:.1f}%", end="\r")


class ChecksumResult(IntEnum):
    RESULT_NOT_CHECKED = 0
    RESULT_OK = 1
    RESULT_ERROR = 2


class Checksums:

    CHECKSUMS_FILE = 'checksums.txt'

    checksums_data = {}

    @classmethod
    def init(cls) -> bool:
        if not os.path.exists(cls.CHECKSUMS_FILE):
            log.error(f"File not found: {cls.CHECKSUMS_FILE}")
            return False
        with open(cls.CHECKSUMS_FILE, 'rt') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                parts = line.split(" ")
                if len(parts) != 2:
                    log.error(f"Invalid line in {cls.CHECKSUMS_FILE}: {line}")
                    continue
                cls.checksums_data[parts[0].lower()] = parts[1].lower()

    @classmethod
    def check_file(cls, full_filename: str) -> ChecksumResult:
        try:
            sum = cls.checksums_data[full_filename.split("/")[-1].lower()]
        except KeyError:
            return ChecksumResult.RESULT_NOT_CHECKED
        block_size = 1024*1024
        hash = hashlib.sha256()
        with open(full_filename, 'rb') as f:
            while block := f.read(block_size):
                hash.update(block)
        if hash.hexdigest() == sum:
            return ChecksumResult.RESULT_OK
        else:
            return ChecksumResult.RESULT_ERROR

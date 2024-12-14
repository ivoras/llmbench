
class DownloadSupportMixin:

    def download_progress(self, nblock: int, bsize: int, total: int):
        current_bytes = nblock * bsize
        print(f"{(current_bytes / total)*100:.1f}%", end="\r")


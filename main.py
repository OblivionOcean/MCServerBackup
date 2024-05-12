import time
import os
import watchdog
from watchdog.observers import Observer
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
import sys
import threading
import tarfile
import zipfile
import shutil

class HD(watchdog.events.FileSystemEventHandler):
    def __init__(self, aim_path, file_type, timing):
        super().__init__()
        self.timer = None
        self.timing = timing
        self.aim_path = aim_path
        self.snapshot = DirectorySnapshot(self.aim_path)
        self.second = 120
        self.method = tarfile.open if file_type == "tar" else (zipfile.ZipFile if file_type == "zip" else None)
        self.ext = "tar.gz" if file_type == "tar" else ("zip" if file_type == "zip" else None) 

    def checkSnapshot(self):
        snapshot = DirectorySnapshot(self.aim_path)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None
        if not os.path.exists("./backup"):
            os.mkdir("./backup")
        if self.method:
            reducted_file = self.method('./backup/%s.%s' % (time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime()), self.ext), mode='w')
            for x in list(diff.files_modified)+list(diff.files_created)+list(diff.files_moved):
                if self.ext == "tar.gz":
                    reducted_file.add(x)
                    print("File %s is added." % x)
                else:
                    reducted_file.write(x)
                    print(str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime()))+" File %s is added." % x)
            reducted_file.close()
        else:
            path2 = './backup/%s' % time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
            os.mkdir(path2)
            for x in list(diff.files_modified)+list(diff.files_created)+list(diff.files_moved):
                shutil.copy(x, path2)
                print("File %s is added." % x)

    def on_any_event(self, event):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.timing, self.checkSnapshot)
        self.timer.start()

def observe(path="", timer=120, file_type=None):
    observer = Observer()
    observer.start()
    event_handler = HD(path, file_type, timer)
    event_handler.second = timer
    observer.schedule(event_handler, path, recursive=True)
    try:
        while True:
            time.sleep(timer)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    observe(path=sys.argv[1], timer=int(sys.argv[2]), file_type=sys.argv[3])
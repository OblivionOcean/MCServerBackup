# MCServerBackup
## Utility
It can be used to collect changed files in a directory during a period by scanning the changed files and copying them into a zip file in "./backup".

Currently, it is used in Minecraft Servers for sensing the changing chunk files in Minecraft worlds.
## Usage
```shell
python main.py [directory] [period]
```
- [directory] should be a relative or absolute path for the directory you want to backup for.
- [period] should be an integer.

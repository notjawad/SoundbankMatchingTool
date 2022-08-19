# Soundbank Matching Tool

![pre](https://i.postimg.cc/FRr6JWzK/download.png)

# Usage
1. Click `File` > `Import`
2. Select the folder containing the soundbanks
3. Select the folder containg the wem files
4. Click `Extract`
5. Wait...

Matched files will be placed in a folder in the same directory as the exe

# Notice

Due to how the [pyinstaller](https://github.com/pyinstaller/pyinstaller) bootloader works, Windows Defender might detect the release as a virus. Read more: https://github.com/pyinstaller/pyinstaller/issues/6062

Alternatively you can compile yourself

```
pip install pyinstaller
pyinstaller -F -w -n "SoundbankMatchingTool" main.py
```

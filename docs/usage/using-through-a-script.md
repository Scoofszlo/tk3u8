This section explains how to use the program through scripts, allowing you to give more flexibity and advaned way of downloading a live stream.

!!! info
    This guide is only applicable for Windows users only.

## Prerequisite

Before everything else, you must install the program via [isolated installation](../installation/isolated-installation-via-uv.md).

To be able to write and edit your scripts, install an IDE of your choice like <b>[Visual Studio](https://code.visualstudio.com/)</b> or <b>[PyCharm](https://www.jetbrains.com/pycharm/)</b>. Text editor like <b>[Notepad++](https://notepad-plus-plus.org/)</b> will work too if you want.

## Creating a script

In the project directory, create a folder named `scripts` and create a file named `download-foo.py`. After that, write a short script where it will download a live stream from a user named `foo` as an example:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username)
```

That's basically how you can write a script.

To simply explain, what this does is that it imports the `Tk3u8` class (line #1) so that we can use it to do a lot of cool stuff like downloading (line #6). But before we can do a lot of things like downloading, we have to create an object of that class (line #5).

## Executing a script

To execute the script, open the terminal from the project directory. After that, execute the script from the `scripts` folder:

```console
uv run scripts/download-foo.py
```

## Executing multiple scripts

If you notice, it's still a bit cumbersome to do `uv run scripts/download-foo.py` every time just to execute a script. If you have multiple scripts for downloading different live streams from different users, it would take a lot of time because you have to execute that command several times.

In order to execute all of these scripts in one go, in your project directory, create a  batch (`.bat`) file that will execute of all these scripts.

For example, to run these three scripts for downloading a live stream from three different users, write this in a batch file:

```bat
@echo off
REM This code will run multiple Python scripts, each in its own terminal.

echo Starting Python scripts...

start cmd /k "uv run scripts/dwnld-john.py"
start cmd /k "uv run scripts/dwnld-jane.py"
start cmd /k "uv run scripts/dwnld-chris.py"

echo All scripts launched. Check the new terminal windows.
pause
```

After that, you can double-click the batch file to run it.

If you have a lot of scripts, instead of writing the `start cmd /k "uv run ..." ` every time, you can do this instead in your batch file:

```bat
@echo off
REM This code will get all the Python scripts from the scripts folder
REM and run each script in its own terminal.

set "SCRIPT_DIR=scripts"

echo Starting Python scripts...

for %%f in ("%SCRIPT_DIR%\*.py") do (
    start cmd /k "uv run "%%f""
)
```

Then, you can now execute the batch file.

## Utilizing `Tk3u8` API for writing your scripts

This section explains how to use the `Tk3u8` class to perform essential features like downloading, as well as configuring it based on your needs.

### Downloading a live stream

To download a live stream from a user, create a variable and type the username inside it that is enclosed with quotation marks:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username)
```
### Choosing stream quality

To choose a quality to download, add a parameter called `quality` inside the `download()`. Values allowed are `original`, `uhd_60`, `uhd`, `hd_60`, `hd`, `ld`, or `sd`:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username, quality="uhd_60")
```

As you have noticed from previous example, the program will work fine even if you don't specify the quality. That's because the program handles this automatically, in which it defaults to `original` value if nothing was specified from the `quality` parameter.

### Wait until live before downloading

To wait for the user to go live and you want the program to start downloading as soon as the user goes live, add a `wait_until_live` parameter with a value of `True` (case-sensitive):

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username, wait_until_live=True)
```

### Setting timeout for checking live status

To set the timeout, add a `timeout` parameter with a value of at least 1:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username, wait_until_live=True, timeout=45)
```

When you don't specify a `timeout` value, it defaults to `30`.

Remember that this should be used together with the `wait_until_live` parameter, which must be set to `True`.

When `timeout` is specified but `wait_until_live` is missing, it will do nothing.

### Force redownloading

If the program happens to stop downloading randomly, you can use this in the parameter of `download()` to automatically reattempt downloading the live stream as long as the user is still live, so that you don't have to manually rerun the script just to start downloading again.

To use this, set the parameter `force_redownload` to True:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username, force_redownload=True)
```

### Custom download location

If you don't want to use the default download location of live streams, you can customize it by specifying the location of folder through `downloads_dir` parameter upon class instantiation of `Tk3u8`:

```py
from tk3u8 import Tk3u8

username = "foo"
download_dir = r"C:\path\to\download_dir"

tk3u8 = Tk3u8(downloads_dir=download_dir)
tk3u8.download(username)
```

!!! info
    Renember to put `r` before the path to ensure that the backslashes are handled properly.

### Custom config file location

If you want to specify the custom path to config file to use, simply supply the `config_file_path` parameter with the location of the config file upon class instantiation of `Tk3u8`:

```py
from tk3u8 import Tk3u8

username = "foo"
config_file_path = r"C:\path\to\config-file.conf"

tk3u8 = Tk3u8(config_file_path=config_file_path)
tk3u8.download(username)
```

!!! info
    Renember to put `r` before the path to ensure that the backslashes are handled properly.

### Using proxy

To set the proxy, call the `set_proxy()` of tk3u8 instance and put the value inside of it enclosed in double quotation marks:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.set_proxy("127.0.0.1:8080")  # Replace this with an actual working proxy
tk3u8.download(username)
```

!!!info
    Remember to put `set_proxy()` first before the `download()` because it won't work if you have swapped their positions.

### Downloading H.265 encoded live stream

Users can opt to download H.265 (HEVC) encoded streams instead of the default ones (H.264/AVC) for potential file size savings or if one wants slightly better stream quality.

To use this, set the parameter `use_h265` to True:

```py
from tk3u8 import Tk3u8

username = "foo"

tk3u8 = Tk3u8()
tk3u8.download(username, use_h265=True)
```

This option may not always work, typically for the `original` quality, as sometimes H.265 encoded version link that is scraped by the program returns a H.264 version for some reason.

Additionally, for some reason, there is an instance that both video codecs in some streams offer similar file sizes. However, when compared, quality is generally a bit better for H.265 version.

For these reasons, using this option does not guarantee smaller file sizes or the same quality as H.264 ones because it is the source that controls the quality of both video codecs, so I would advise you to compare both to see if there is a file size saving or if there is a quality difference. In that way, you can decide whether to use this option or not.

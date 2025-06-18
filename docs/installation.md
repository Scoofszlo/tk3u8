This section will walk you through the process of setting up the required environment and installing all necessary dependencies to get tk3u8 running on your system.

## Installation methods

### Isolated installation (via pip)

This method installs the program via `pip` and uses uv to run the program.

!!! tip
    This method is the most recommended for most users.

#### Requirements
- Windows or Linux
- Python `>=3.10.0`
- ffmpeg
- uv

#### Steps
1. Install Python 3.10.0 or above. Ensure `Add Python x.x to PATH` is checked.
2. Install [ffmpeg](https://ffmpeg.org/download.html). Ensure ffmpeg is added to [PATH](https://phoenixnap.com/kb/ffmpeg-windows#Step_3_Add_FFmpeg_to_PATH).
3. Install [Git](https://git-scm.com/downloads/win).
4. Install uv, through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

    ```console
    pip install uv
    ```

5. Choose a location to store the program's data or source code, and create a folder there (e.g., create a folder named `tk3u8` inside your Documents directory).

6. Initialize the created folder. This will create some stuff needed to isolate the installation of dependencies to this folder.

    ```console
    uv init --app
    ```

7. Install tk3u8 by adding it as a dependency.

    ```console
    uv add tk3u8
    ```

    This will install the tk3u8 package, as well as the dependencies needed by this program.


8. Run the program.
    ```sh
    uv run tk3u8 -h
    ```
    When installed properly, the output should look like this:
    ```text
    Usage: tk3u8 [-h] [-q {original,uhd_60,uhd,hd_60,hd,ld,sd}] [--proxy PROXY]
                 [--wait-until-live] [--timeout TIMEOUT] [--log-level {DEBUG,ERROR}] 
                 [-v] username

    tk3u8 - A TikTok live downloader

    Positional Arguments:
      username              The username to be used for recording live stream

    Options:
      -h, --help            show this help message and exit
      -q {original,uhd_60,uhd,hd_60,hd,ld,sd}
                            Specify the quality of the video to download. Default: original
      --proxy PROXY         The proxy server to use for downloading. Sample format: 127.0.0.1:8080
      --wait-until-live     Let the program wait until the user goes live to start downloading stream
      --timeout TIMEOUT     Set the timeout in seconds before rechecking if the user is live.
      --log-level {DEBUG,ERROR}
                            Set the logging level (default: no logging if not used)
      -v, --version         Show the program's version
    ```

### Isolated installation (via Git)

This step clones the source code from repository using Git and uses `uv` to run the program.

!!! info
    This method is recommended if you want to get latest updates of the program so that you don't have to wait for published releases.

#### Requirements
- Windows or Linux
- Python `>=3.10.0`
- ffmpeg
- uv
- Git

#### Steps
1. Install Python 3.10.0 or above. Ensure `Add Python x.x to PATH` is checked.
2. Install [ffmpeg](https://ffmpeg.org/download.html). Ensure ffmpeg is added to [PATH](https://phoenixnap.com/kb/ffmpeg-windows#Step_3_Add_FFmpeg_to_PATH).
3. Install [Git](https://git-scm.com/downloads/win).
4. Install uv, through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

    ```console
    pip install uv
    ```

5. Clone this repository using Git.

    ```console
    git clone https://github.com/Scoofszlo/tk3u8.git
    ```

6. Change the current directory to the project's folder.
    ```clone
    cd tk3u8
    ```

7. Run the program.
    ```sh
    uv run tk3u8 -h
    ```
    When installed properly, the output should look like this:
    ```text
    Usage: tk3u8 [-h] [-q {original,uhd_60,uhd,hd_60,hd,ld,sd}] [--proxy PROXY]
                 [--wait-until-live] [--timeout TIMEOUT] [--log-level {DEBUG,ERROR}] 
                 [-v] username

    tk3u8 - A TikTok live downloader

    Positional Arguments:
      username              The username to be used for recording live stream

    Options:
      -h, --help            show this help message and exit
      -q {original,uhd_60,uhd,hd_60,hd,ld,sd}
                            Specify the quality of the video to download. Default: original
      --proxy PROXY         The proxy server to use for downloading. Sample format: 127.0.0.1:8080
      --wait-until-live     Let the program wait until the user goes live to start downloading stream
      --timeout TIMEOUT     Set the timeout in seconds before rechecking if the user is live.
      --log-level {DEBUG,ERROR}
                            Set the logging level (default: no logging if not used)
      -v, --version         Show the program's version
    ```

If you don't want to get the latest updates, you can checkout the latest published assuming v0.3.1 is the latest release and you want to use that:

```console
git checkout tags/v0.3.1
```

### System-wide installation via `pip`

!!! warning
    This method installs the program system-wide using the command `pip install tk3u8`. Use this only if you are knowledgeable enough and you are comfortable installing the dependencies of this program system-wide. Doing so may conflict with those already installed on your system so please proceed with caution.

#### Requirements
- Windows or Linux
- Python `>=3.10.0`
- ffmpeg

#### Steps
1. Install Python 3.10.0 or above. Ensure `Add Python x.x to PATH` is checked.
2. Install [ffmpeg](https://ffmpeg.org/download.html). Ensure ffmpeg is added to [PATH](https://phoenixnap.com/kb/ffmpeg-windows#Step_3_Add_FFmpeg_to_PATH).
3. Install `tk3u8` using `pip install`.
    ```sh
    pip install tk3u8
    ```
4. Run the program.
    ```sh
    tk3u8 -h
    ```
    When installed properly, the output should look like this:
    ```text
    Usage: tk3u8 [-h] [-q {original,uhd_60,uhd,hd_60,hd,ld,sd}] [--proxy PROXY]
                 [--wait-until-live] [--timeout TIMEOUT] [--log-level {DEBUG,ERROR}] 
                 [-v] username

    tk3u8 - A TikTok live downloader

    Positional Arguments:
      username              The username to be used for recording live stream

    Options:
      -h, --help            show this help message and exit
      -q {original,uhd_60,uhd,hd_60,hd,ld,sd}
                            Specify the quality of the video to download. Default: original
      --proxy PROXY         The proxy server to use for downloading. Sample format: 127.0.0.1:8080
      --wait-until-live     Let the program wait until the user goes live to start downloading stream
      --timeout TIMEOUT     Set the timeout in seconds before rechecking if the user is live.
      --log-level {DEBUG,ERROR}
                            Set the logging level (default: no logging if not used)
      -v, --version         Show the program's version
    ```

## Updating tk3u8

If you installed the program via pip (isolated installation), run this command:
```console
uv lock -P tk3u8
```

If you installed the program via Git (isolated installation), run this command:
```console
git pull origin
```
If system-wide installation was done via pip:
```
pip install tk3u8 --upgrade
```

## Verifying installation

In case that there are some problems during the installation, ensure that all requirements are properly installed. You can verify each one by running the following commands in your terminal or command prompt:

- **Python**
    ```console
    python --version
    
    # Sample output
    Python 3.12.2
    ```

- **ffmpeg**
    ```console
    ffmpeg -version

    # Sample output
    ffmpeg version 2024-11-11-git-96d45c3b21-full_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
    ...
    ```
    

- **uv**
    ```console
    uv --version

    # Sample output
    uv 0.6.17 (8414e9f3d 2025-04-25)
    ```

- **Git**
    ```sh
    git --version
    
    # Sample output
    git version x.x.x
    ```

If any command fails or shows an error, revisit the installation steps for that requirement.

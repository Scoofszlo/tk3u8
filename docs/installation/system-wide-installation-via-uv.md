This method uses uv to install and run the program.

This is the most recommended as the installation is the easiest, and running the program can be done in your terminal anywhere.

### Requirements

- Windows or Linux
- Python `v3.10` or greater
- FFmpeg
- uv
- Git (optional)

### Steps

1. Install Python 3.10.0 or above. For Windows users, ensure `Add Python x.x to PATH` is checked.
2. Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). For Windows users, follow this [guide](https://phoenixnap.com/kb/ffmpeg-windows#Step_1_Download_FFmpeg_for_Windows) for proper installation.
3. Open your command-line.
4. Install uv through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

    ```console
    pip install uv
    ```

5. Install the latest published stable release of tk3u8 into your system.

    ```console
    uv tool install tk3u8
    ```

    Alternatively, if you want to get the latest published pre-release version, run this command instead.

    ```console
    uv tool install tk3u8 --pre-release allow
    ```

    Or if you want to get the most recent update without having to wait for official pre-release, choose this one instead.

    ```console
    uv tool install git+https://github.com/Scoofszlo/tk3u8
    ```

    !!! warning
        Installing pre-release versions is discouraged as I don't guaranteed them to be stable enough. Although there are testing done for these versions, it is still better if you install the latest stable instead.

6. Run the program.

    ```console
    tk3u8 -v
    ```

    When stable release is installed properly, the output should look like this:

    ```text
    tk3u8 v0.4.0
    ```

## Updating tk3u8

To update tk3u8, run the following command.

```console
uv tool upgrade tk3u8
```

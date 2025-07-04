This method uses pip to install the program.

!!! warning
    This method installs the program system-wide. The problem with this method is that if you have already been using Python for some other stuff in the past, there is a chance that the dependencies of this project might also exist on your computer. This could lead to conflicts, resulting in installation failures and broken functionality for this program, as well as for other programs that rely on those dependencies.

    If you are knowledgeable and able to handle potential problems, please proceed with caution.

##  Requirements

- Windows or Linux
- Python `v3.10` or greater
- FFmpeg

## Steps

1. Install Python 3.10.0 or above. For Windows users, ensure `Add Python x.x to PATH` is checked.
2. Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). For Windows users, follow this [guide](https://phoenixnap.com/kb/ffmpeg-windows#Step_1_Download_FFmpeg_for_Windows) for proper installation.
3. Install the latest published stable release of tk3u8 using `pip install`.
    ```sh
    pip install tk3u8
    ```

    Alternatively, if you want to get the latest published pre-release version, run this command instead.

    ```console
    pip install --pre tk3u8
    ```

    Or if you want to get the most recent update without having to wait for official pre-release, choose this one instead.

    ```console
    pip install git+https://github.com/Scoofszlo/tk3u8
    ```

    !!! warning
        Installing pre-release versions is discouraged as I don't guaranteed them to be stable enough. Although there are testing done for these versions, it is still better if you install the latest stable instead.

4. Run the program.
    ```sh
    tk3u8 -v
    ```
    When stable release is installed properly, the output should look like this:

    ```text
    tk3u8 v0.4.0
    ```

## Updating tk3u8

To update tk3u8, run the following command.

```
pip install tk3u8 --upgrade
```

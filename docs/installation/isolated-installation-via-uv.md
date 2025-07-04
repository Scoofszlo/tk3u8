This method uses uv to install and run the program.

This installation method is preferred if you want to install the program on a specific folder of your choice (e.g., Documents folder) so that all of the installation and opening of the program only happens there.

If you also [write scripts](../usage/using-through-a-script.md) to download live streams, this is also the recommended installation.

## Requirements

- Windows or Linux
- Python `v3.10` or greater
- FFmpeg
- uv
- Git (optional)

## Steps

1. Install Python 3.10.0 or above. For Windows users, ensure `Add Python x.x to PATH` is checked.
2. Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). For Windows users, follow this [guide](https://phoenixnap.com/kb/ffmpeg-windows#Step_1_Download_FFmpeg_for_Windows) for proper installation.
3. Open your command-line.
4. Install uv through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

    ```console
    pip install uv
    ```

5. Choose a location to store the program's data or source code, and create a folder there (e.g., create a folder named `tk3u8` inside your Documents directory).

6. Initialize the created folder with the following command.

    ```console
    uv init --app
    ```

    This will create some stuff needed to isolate the installation of dependencies to this folder.

7. Install the latest published stable release of tk3u8 by adding it as a dependency.

    ```console
    uv add tk3u8
    ```

    Alternatively, if you want to get the latest published pre-release version, run this command instead.

    ```console
    uv add --prerelease allow tk3u8
    ```

    Or if you want to get the most recent update without having to wait for official pre-release, choose this one instead.

    ```console
    uv add git+https://github.com/Scoofszlo/tk3u8
    ```

    !!! warning
        Installing pre-release versions is discouraged as I don't guaranteed them to be stable enough. Although there are testing done for these versions, it is still better if you install the latest stable instead.

8. Run the program.

    ```console
    uv run tk3u8 -v
    ```
    When stable release is installed properly, the output should look like this:

    ```text
    tk3u8 v0.4.0
    ```

## Updating tk3u8

To update tk3u8, run the following command.

```console
uv lock -P tk3u8
```


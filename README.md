# Slack NIxporter

A simple python script that takes an Slack export in a .zip form and downloads all files sent to the channel.

Features implemented:

- [x] Download of all images in a text message (I'm not sure if this works on threads)
- [ ] Download all user avatars
- [ ] Download all public channel Canvas
- [ ] Download all current emojis
- [ ] Make a frontend to show this data (ideally a searchable one)

Feel free to contribute if you want some of these features! 

# How to use

To use, you must have python3 and pip installed, then install the requirements used by the project (you should use a [venv](https://docs.python.org/3/library/venv.html) for this)

```bash
python -m pip install -r requirements.txt
```

Then you can run the `files-downloader.py` script with the following syntax: 

```bash
python files-downloader.py <filename>
```

You can also specify an output file:

```bash
python files-downloader.py <filename> -o <output_filename>
```
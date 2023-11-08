import argparse
import zipfile
import glob
import json
import re
import os
import asyncio
import aiohttp
import shutil

session = None
parser = argparse.ArgumentParser(
    prog="python files-download.py",
    description="Takes a slack export and downloads all avaiable files")

parser.add_argument('filename', type=str, help="Takes the export slack .zip file")
parser.add_argument('-o', '--output', dest="output", required=False, type=str, default="full-export.zip")

files = {}

async def download_file(channel_name,file):
    if(os.path.exists(f"export/{channel_name}/{file[0]}")):
        print(f"{file[0]} already exists... skipping download.")
        return
    async with session.get(file[1]) as req:
        if req.status != 200:
            print(f"File {file[0]} failed to download with status {req.status}.")
            return
        bytes = await req.read()
        file = open(f"export/{channel_name}/{file[0]}", "wb")
        file.write(bytes)

async def download_files():
    global session
    session = aiohttp.ClientSession()
    for k in files.keys():
        print(f"Downloading files from {k} channel...")
        coroutines = [download_file(k, file) for file in files[k]]
        await asyncio.gather(*coroutines)
    await session.close()

if __name__ == '__main__':
    args = parser.parse_args()
    if not zipfile.is_zipfile(args.filename):
        print(f"{args.filename} is not a valid zip file or doesn't exist.")
        exit(1)
    with zipfile.ZipFile(args.filename) as zip:
        zip.extractall('export')
    conversations = glob.glob('export/*/[0-9]*-[0-9]*-[0-9]*.json')
    for conversation in conversations:
        with open(conversation) as cfile:
            channel_name = re.match('export\/(.*)\/.+\.json', conversation).group(1)
            if channel_name not in files:
                files[channel_name] = []
            conversation_json = json.load(cfile)
            messages_with_files = filter(lambda message: message.get('files') is not None and len(message['files']) > 0, conversation_json)
            file_links = map(
                lambda message: 
                    [(message['ts'],file.get('url_private_download'), file.get('name'), file.get('id')) for file in message['files'] 
                     if file.get('url_private_download') is not None ],
                messages_with_files)            
            for file_list in file_links:
                for file in file_list:
                    files[channel_name].append((f"{channel_name}-{file[0]}-{file[3]}-{file[2]}", file[1]))
    asyncio.run(download_files())
    with zipfile.ZipFile(args.output, "w") as zip:
        export_files = glob.glob('export/**', recursive=True)
        for file in export_files:
            zip.write(file)
    shutil.rmtree('export')

    
    
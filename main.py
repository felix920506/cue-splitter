import asyncio
import asyncinotify
import datetime
import os
import os.path
import splitcue

in_env = os.getenv('CUESPLITTER_INPUT_DIR')
out_env = os.getenv('CUESPLITTER_OUTPUT_DIR')

INPUT_DIR = './input' if in_env is None else in_env
OUTPUT_DIR = './output' if out_env is None else out_env
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.jpe']
AUDIO_EXTENSIONS = ['.flac', '.bin', '.wav']
DELETE = True

'''
Get extension from filename
'''
def extension(filename: str):
    name, ext = os.path.splittext(filename)
    return ext

'''
Process a single audio file given audio file name
'''
async def process(audio: str):
    name, ext = os.path.splitext(audio)
    cue = name + '.cue'
    head, tail = os.path.split(name)
    outpath = os.path.join(OUTPUT_DIR, tail)
    
    if os.path.exists(outpath):
        return

    await asyncio.sleep(1)

    # split the input into individiaul tracks
    if ext.lower() == '.bin':
        await splitcue.splitBinFile(audio, cue, outname=tail, outpath=outpath)
    else:
        await splitcue.splitAudioFile(audio, cue, outname=tail, outpath=outpath)
    
    # transcode tracks to flac
    await splitcue.transcodeAudioFilesToFlac(outpath, delete=True)

    # apply metadata tags
    await splitcue.tagAudioFiles(outpath, cue)

    # apply cover image if exists
    # find the cover with correct extension
    covernames = [name+i for i in IMAGE_EXTENSIONS]
    for cover in covernames:
        if os.path.exists(cover):
            await splitcue.addImgToFlacs(outpath, cover)
            if DELETE:
                try:
                    os.remove(cover)
                except:
                    pass
            break
    
    try:
        os.remove(audio)
    except:
        pass

    try:
        os.remove(cue)
    except:
        pass
    
    
'''
Find audio file given cue name
'''
def findaudio(cue: str):
    name, ext = os.path.splitext(cue)
    audionames = [name+i for i in AUDIO_EXTENSIONS]
    for i in audionames:
        if os.path.isfile(i):
            return os.path.abspath(i)
    return None

'''
Find cue name given audio name
'''
def findcue(audio: str):
    name, ext = os.path.splitext(audio)
    cue = name + '.cue'
    if os.path.exists(cue):
        return os.path.abspath(cue)
    else:
        return None

'''
Main functions
'''
async def main():
    eventcache: dict[str: list[str]] = {}
    with asyncinotify.Inotify() as inotify:
        inotify.add_watch(INPUT_DIR, asyncinotify.Mask.CLOSE_WRITE | asyncinotify.Mask.MOVED_TO)
        async for event in inotify:
            # filter out events on input dir itself
            if event.name is not None:
                # eventpath = os.path.join(INPUT_DIR, event.name)
                abspath = os.path.join(INPUT_DIR, event.name)
                name, ext = os.path.splitext(abspath)
                if ext != '.cue' and ext not in AUDIO_EXTENSIONS:
                    continue

                if name in eventcache:
                    eventcache[name].append(abspath)
                else:
                    eventcache[name] = [abspath]
                
                if len(eventcache[name]) == 2:
                    await process(abspath)
                    eventcache.pop(name)



if __name__ == "__main__":
    assert not os.path.isfile(INPUT_DIR)
    assert not os.path.isfile(OUTPUT_DIR)
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    asyncio.run(main())

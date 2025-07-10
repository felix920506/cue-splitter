import asyncio
import os
import os.path

'''
Splits the provided audio file using the provided cue file into wav files. Original files will not be touched.
Supports all formats supported by shntools
'''
async def splitAudioFile(filepath: str, cuepath: str, outname: str = 'track', outpath: str = None):
    cmd = ['shnsplit', '-f', cuepath]
    if outname is not None:
        cmd.extend(['-t', f'{outname}-%n'])
    if outpath is not None:
        try:
            os.makedirs(outpath)
        except:
            pass

        cmd.extend(['-d', outpath])
    
    cmd.append(filepath)
    
    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.wait()

'''
Transcodes all audio files with the given extension in the provided directory into flac files. Original files will not be touched.
default extension: wav
'''
async def transcodeAudioFilesToFlac(filesDir: str, ext: str = 'wav'):
    files = os.listdir(filesDir)
    files = [os.path.join(filesDir, i) for i in files if i.lower().endswith('.'+ext)]
    cmd = ['flac', '-8'] + files
    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.wait()


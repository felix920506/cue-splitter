import asyncio
import os

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


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
Splits the provided audio cd bin file using the provided cue file into wav files. Original files will not be touched.
'''
async def splitBinFile(filepath: str, cuepath: str, outname: str = 'track', outpath: str = None):
    outprefix = os.path.join(outpath, outname+'-')
    if outpath is not None:
        try:
            os.makedirs(outpath)
        except:
            pass
    cmd = ['bchunk', '-w', filepath, cuepath, outprefix]
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

'''
Tags numbered audio files with provided extension in the provided path using the provided cue file. Files are modified in place.
supports ogg, flac, mp3
default extension: flac
'''
async def tagAudioFiles(filesDir: str, cuepath: str, ext: str = 'flac'):
    CUETAG_CMD = 'cuetag' # use cuetag.sh for macos homebrew install
    files = os.listdir(filesDir)
    files.sort()
    files = [os.path.join(filesDir, i) for i in files if i.lower().endswith('.'+ext)]
    cmd = [CUETAG_CMD, cuepath] + files
    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.wait()

'''
Main function used for testing
'''
async def main():
    await splitAudioFile('./flac-test/test.flac', './flac-test/test.cue', 'track', './flac-test/out')
    await transcodeAudioFilesToFlac('./flac-test/out/')
    await tagAudioFiles('./flac-test/out/', './flac-test/test.cue')

    await splitBinFile('./bin-test/test.bin', './bin-test/test.cue', 'track', './bin-test/out')
    await transcodeAudioFilesToFlac('./bin-test/out')
    await tagAudioFiles('./bin-test/out/', './bin-test/test.cue')


if __name__ == '__main__':
    asyncio.run(main())

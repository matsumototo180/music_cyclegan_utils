from pathlib import Path
import os
import numpy as np
import soundfile

def getAudioFilesPath(path):
    
    p_path = Path(path)

    if p_path.is_file():
        files_path = list([p_path])
    else:
        files_path = (list(p_path.iterdir()))
        files_path = [f for f in files_path if (f.suffix == ".wav") or (f.suffix == ".mp3")]

    return sorted(files_path)

def getFilesPath(path, suffix = None):
    p_path = Path(path)
    if p_path.is_file():
        files_path = list([p_path])
    else:
        files_path = (list(p_path.iterdir()))
        if suffix != None:
            files_path = [f for f in files_path if (f.suffix == suffix)]

    return sorted(files_path)

def saveNpy(npyarray, output_path):
    output_path = Path(output_path)
    if not output_path.parent.exists():
        os.makedirs(output_path.parent)
    np.save(output_path, npyarray)

def saveWav(wav, output_path, sr):
    output_path = Path(output_path)
    if not output_path.parent.exists():
        os.makedirs(output_path.parent)
    soundfile.write(str(output_path.parent) + "/" + output_path.stem + "_inv.wav", wav, sr)
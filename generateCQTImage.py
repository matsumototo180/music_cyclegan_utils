import librosa
import numpy as np
import soundfile
import argparse
from pathlib import Path
from PIL import Image

def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result

def generateSpecCQT(fpath):

    hop_length = 128
    bins_per_octave = 12 * 12
    n_octaves = 8
    n_bins = bins_per_octave * n_octaves
    
    y, sr = librosa.load(fpath, mono=True)
    C = librosa.cqt(y=y, sr=sr, hop_length=hop_length, n_bins=n_bins, bins_per_octave=bins_per_octave)
    M, P = librosa.magphase(C)
    
    M = (255 * min_max(M)).astype(np.uint8)
    
    return M, P

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate cqt amplitude spectrogram and phase spectrogram')    # 2. パーサを作る

    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('-i', '--input', type=Path, help='input file path')    # 必須の引数を追加
    parser.add_argument('-o', '--output', type=Path, default='./', help='output directory')    # オプション引数（指定しなくても良い引数）を追加

    args = parser.parse_args()    # 4. 引数を解析
    
    ampspec, phspec = generateSpecCQT(args.input)
    
    # np.save(str(args.output) + "/" + Path(args.input).stem + "_amp", ampspec)
    ampspec_img = Image.fromarray(ampspec)
    ampspec_img.save(str(args.output) + "/" + Path(args.input).stem + ".png")
    np.save(str(args.output) + "/" + Path(args.input).stem + "_phase", phspec)
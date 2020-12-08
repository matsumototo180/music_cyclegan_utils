# wavまたはmp3形式のオーディオファイルをCQT変換し、dbスケール変換、-1〜1の値に変換した振幅行列と位相行列を出力する
#
# 【コマンドライン引数】
# --input   入力ファイルのパスまたはディレクトリ ※必須
# --output  出力ディレクトリ（指定したパスが存在しない場合はディレクトリが作られる）
# --sr      サンプリングレート
# --stereo  この引数を指定するとステレオで処理する（未実装）
# --crop    この引数を指定するとSTFT後のデータをclでクロップする
# --wl      STFTのwindow length
# --hl      STFTのhop length
# --cl      クロップする長さ

from options import Options
import utils
import numpy as np
import librosa
from pathlib import Path

def magphaseCQT(cqt_complex, crop = False, cl = 128):
    # crop matrix
    if crop:
        cqt_complex = cqt_complex[:,:cl]

    M, P = librosa.magphase(cqt_complex)
    Mdb = librosa.amplitude_to_db(M)
    # normalize values between -1 and 1
    Mdb_normed = 2*((Mdb - Mdb.min())/(Mdb.max() - Mdb.min())) - 1
    
    return Mdb_normed, P

def wavToCQT(wav_path, output_path, sr, hl, crop, cl, stereo):
    bins_per_octave = 12 * 12
    n_octaves = 8
    n_bins = bins_per_octave * n_octaves
    
    print("reading audio files")
    files_path = utils.getAudioFilesPath(wav_path)
    waves = [librosa.load(i, sr=sr, mono=not stereo) for i in files_path]

    total_length = str(len(waves))
    for i, wav in enumerate(waves):
        cqt = librosa.cqt(wav[0], sr, hop_length=hl, n_bins=n_bins, bins_per_octave=bins_per_octave)
        mag, phase = magphaseCQT(cqt, crop, cl)
        filename = files_path[i].stem
        out_path_amp = Path(output_path) / Path("cqt_amp")
        out_path_phase = Path(output_path) / Path("cqt_phase")
        out_path_amp = (out_path_amp / Path(filename))
        out_path_phase = (out_path_phase / Path(filename))

        print(str(out_path_amp.name) + " [", str(i + 1), "/", total_length, "]", sep="")
        
        if mag.shape[0] % 2 != 0:
            mag = mag[:-1,:]
            phase = phase[:-1,:]
        if mag.shape[1] % 2 != 0:
            mag = mag[:,:-1]
            phase = phase[:,:-1]
        
        utils.saveNpy(mag, out_path_amp)
        utils.saveNpy(phase, out_path_phase)
    return

if __name__ == '__main__':
    opt = Options().parse_cmdargs()
    wavToCQT(opt.input, opt.output, opt.sr, opt.hl, opt.crop, opt.cl, opt.stereo)
# wavまたはmp3形式のオーディオファイルをSTFT変換し、dbスケール変換、-1〜1の値に変換した振幅行列と位相行列を出力する
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

def magphaseSTFT(stft_complex, crop = False, cl = 128):
    # crop matrix
    if crop == True:
        stft_complex = stft_complex[:,:cl]
    
    # extract magnitude spectrogram and phase spectrogram from complex matrix
    M, P = librosa.magphase(stft_complex)
    Mdb = librosa.amplitude_to_db(M)
    # normalize values between -1 and 1
    Mdb_normed = 2*((Mdb - Mdb.min())/(Mdb.max() - Mdb.min())) - 1

    return Mdb_normed, P

def wavToSTFT(wav_path, output_path = "./", sr = 22050, wl = 1024, hl = 512, crop = False, cl = 128, stereo = False):
    print("reading audio files")
    files_path = utils.getAudioFilesPath(wav_path)
    waves = [librosa.load(i, sr=sr, mono=not stereo) for i in files_path]
    
    total_length = str(len(waves))
    for i, wav in enumerate(waves):
        stft = librosa.stft(wav[0], wl, hl, wl)
        mag, phase = magphaseSTFT(stft, crop, cl)
        filename = files_path[i].stem
        out_path_amp = Path(output_path) / Path("stft_amp") / Path(filename)
        out_path_phase = Path(output_path) / Path("stft_phase") / Path(filename)

        print(str(out_path_amp.name) + " [", str(i + 1), "/", total_length, "]", sep="")

        utils.saveNpy(mag[:-1,:], out_path_amp)
        utils.saveNpy(phase[:-1,:], out_path_phase)
    return

if __name__ == '__main__':
    opt = Options().parse_cmdargs()
    wavToSTFT(opt.input, opt.output, opt.sr, opt.wl, opt.hl, opt.crop, opt.cl, opt.stereo)
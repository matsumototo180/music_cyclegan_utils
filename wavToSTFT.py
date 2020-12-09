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
# --amp_only ampファイルのみ出力する

from options import Options
import utils
import numpy as np
import librosa
from pathlib import Path

def magphaseSTFT(stft_complex, crop = False, cl = 128):
    
    # crop matrix
    if crop == True:
        div_num = len(stft_complex[1]) // cl
        if div_num <= 0:
            raise Exception('stft_complex signal length is too short')
        stft_complex_list = [stft_complex[:, i*cl:(i+1)*cl] for i in range(div_num)]
    else:
        stft_complex_list = [stft_complex]

    MP_list = [librosa.magphase(i) for i in stft_complex_list]
    M_list = [np.nan_to_num(i[0]) for i in MP_list]
    P_list = [np.nan_to_num(np.angle(i[1])) for i in MP_list]
    Mdb_list = [librosa.amplitude_to_db(i) for i in M_list]
    Mdb_normed_list = [2*((i - i.min())/(i.max() - i.min())) - 1 for i in Mdb_list]
    MP_list = [(amp, P_list[i]) for i, amp in enumerate(Mdb_normed_list)]

    return MP_list

def alignMagphase(magphase_tuple):
    m_flength = magphase_tuple[0].shape[0]
    m_tlength = magphase_tuple[0].shape[1]

    mag = magphase_tuple[0]
    phase = magphase_tuple[1]

    if m_flength % 2 != 0:
        mag = mag[:-1,:]
        phase = phase[:-1,:]
    if m_tlength % 2 != 0:
        mag = mag[:,:-1]
        phase = phase[:,:-1]
    return (mag, phase)

def wavToSTFT(wav_path, output_path = "./", sr = 22050, wl = 1024, hl = 512, crop = False, cl = 128, stereo = False, amp_only = False):
    print("reading audio files")
    files_path = utils.getAudioFilesPath(wav_path)
    waves = [librosa.load(i, sr=sr, mono=not stereo) for i in files_path]
    div_duration = cl*hl/sr

    total_length = str(len(waves))
    for i, wav in enumerate(waves):
        if crop:
            duration = div_duration
        else:
            duration = len(wav) / 22050

        stft = librosa.stft(wav[0], wl, hl, wl)

        try:
            magphase_list = magphaseSTFT(stft, crop, cl)
        except Exception as e:
            print(e)
        
        magphase_list = [alignMagphase(mp) for mp in magphase_list]
        div_num = len(magphase_list)

        filename_list = [files_path[i].stem + "-" + str(index + 1) for index in range(div_num)] 

        out_path_amp_list = [Path(output_path) / Path("stft_amp") / Path(filename) for filename in filename_list]
        out_path_phase_list = [Path(output_path) / Path("stft_phase") / Path(filename) for filename in filename_list]

        for index, out_path_amp in enumerate(out_path_amp_list):
            print(str(out_path_amp.name) + "\t[", str(i + 1), "/", total_length, "]", "\tsignal duration(sec): ", duration, sep="")
            utils.saveNpy(magphase_list[index][0], out_path_amp)
            utils.saveNpy(magphase_list[index][1], out_path_phase_list[index])

    return

if __name__ == '__main__':
    opt = Options().parse_cmdargs()
    wavToSTFT(opt.input, opt.output, opt.sr, opt.wl, opt.hl, opt.crop, opt.cl, opt.stereo)
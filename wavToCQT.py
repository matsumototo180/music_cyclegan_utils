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
# --amp_only ampファイルのみ出力する

from options import Options
import utils
import numpy as np
import librosa
import json
import datetime
from pathlib import Path

def magphaseCQT(cqt_complex, crop = False, cl = 128):
    # crop matrix
    if crop == True:
        div_num = len(cqt_complex[1]) // cl
        if div_num <= 0:
            raise Exception('cqt_complex signal length is too short')
        cqt_complex_list = [cqt_complex[:, i*cl:(i+1)*cl] for i in range(div_num)]
    else:
        cqt_complex_list = [cqt_complex]

    MP_list = [librosa.magphase(i) for i in cqt_complex_list]
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

def wavToCQT(wav_path, output_path = "./", sr = 22050, hl = 512, crop = False, cl = 128, stereo = False, amp_only = False):
    bins_per_octave = 12 * 12
    n_octaves = 8
    n_bins = bins_per_octave * n_octaves
    
    print("reading audio files")
    files_path = utils.getAudioFilesPath(wav_path)
    waves = [librosa.load(i, sr=sr, mono=not stereo) for i in files_path]
    div_duration = cl*hl/sr
    num_of_segments = 0
    dt_now = datetime.datetime.now()
    dt_now = '{:%Y-%m-%d %H:%m}'.format(dt_now)

    total_length = str(len(waves))
    for i, wav in enumerate(waves):
        if crop:
            duration = div_duration
        else:
            duration = len(wav) / sr

        cqt = librosa.cqt(wav[0], sr, hop_length=hl, n_bins=n_bins, bins_per_octave=bins_per_octave)

        try:
            magphase_list = magphaseCQT(cqt, crop, cl)
        except Exception as e:
            print(e)
        
        magphase_list = [alignMagphase(mp) for mp in magphase_list]
        div_num = len(magphase_list)

        filename_list = [files_path[i].stem + "-" + str(index + 1) for index in range(div_num)] 

        out_path_amp_list = [Path(output_path) / Path("amp") / Path(filename) for filename in filename_list]
        out_path_phase_list = [Path(output_path) / Path("phase") / Path(filename) for filename in filename_list]

        for index, out_path_amp in enumerate(out_path_amp_list):
            print(str(out_path_amp.name) + "\t[", str(i + 1), "/", total_length, "]", "\tsignal duration(sec): ", duration, sep="")
            utils.saveNpy(magphase_list[index][0], out_path_amp)
            utils.saveNpy(magphase_list[index][1], out_path_phase_list[index])
            num_of_segments += 1

    log = {
        "time":                 dt_now,
        "convert_method":       "wavToSTFT",
        "input_path":           str(Path(wav_path)),
        "output_path":          str(Path(output_path)),
        "sr":                   sr,
        "window_length":        "None",
        "hop_length":           hl,
        "crop":                 crop,
        "crop_length":          cl,
        "stereo":               stereo,
        "amp_only":             amp_only,
        "number_of_songs":      total_length,
        "number_of_segments":   num_of_segments}

    with open(Path(output_path) / Path("audioconvert_log.json"), "w") as f:
        json.dump(log, f, indent=4)
    return

if __name__ == '__main__':
    opt = Options().parse_cmdargs()
    wavToCQT(opt.input, opt.output, opt.sr, opt.hl, opt.crop, opt.cl, opt.stereo)
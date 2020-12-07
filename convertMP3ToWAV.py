# mp3形式のオーディオファイルをwav形式に変換する
#
# 【コマンドライン引数】
# --input   入力ファイルのパスまたはディレクトリ ※必須
# --output  出力ディレクトリ（指定したパスが存在しない場合はディレクトリが作られる）
# --sr      出力サンプリングレート
# --stereo  この引数を指定するとステレオで出力する

from options import Options
import utils
import subprocess
import os
from pathlib import Path

def convertMP3ToWAV(path, output, sr, stereo):
    if path.suffix != ".mp3":
        raise Exception('Error: input file is not mp3')
    
    out = Path(output) / Path(path.stem + ".wav")

    if not out.parent.exists():
        os.makedirs(out.parent)

    if out.exists():
        print("file already exists")
        return out

    if not stereo:
        cmd = "ffmpeg -i " + str(path) + " -ar " + str(sr) + " -ac 1 " + str(out)
    else:
        cmd = "ffmpeg -i " + str(path) + " -ar " + str(sr) + " " + str(out)
    runcmd = subprocess.call(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if runcmd != 0:
        print(runcmd)
    return out

if __name__ == '__main__':
    opt = Options().parse_cmdargs()
    files_path = utils.getAudioFilesPath(opt.input)

    mp3files_path = [i for i in files_path if i.suffix == ".mp3"]

    count = 0
    for i in mp3files_path:
        count += 1
        out = convertMP3ToWAV(i, opt.output, opt.sr, opt.stereo)
        print("processing:" + str(count) + "/" + str(len(mp3files_path)) + "   " + str(out))
        
    print("complete")
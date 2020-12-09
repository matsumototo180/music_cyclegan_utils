import argparse
import os

class Options():
    def __init__(self, inverse = False):
        self.default_output = "./"
        self.default_sr = 22050
        self.default_stereo = False
        self.default_crop = False
        self.defalut_wl = 1024
        self.defalut_hl = 512
        self.defalut_cl = 128
        self.default_amp_only = False

        self.inverse = inverse

        self.parser = argparse.ArgumentParser()    # パーサを作る
        self.parser.add_argument('--input', required=True, help='path to audio file or directory')
        # additional parameters
        self.parser.add_argument('--output', default='./', help='path to output directory')
        self.parser.add_argument('--sr', type=int, default='22050', help='sampling rate')
        self.parser.add_argument('--stereo', action='store_true', help='if specified, load audio as stereo source')
        self.parser.add_argument('--crop', action='store_true', help='if specified, crop waveform with cl')
        self.parser.add_argument('--wl', type=int, default='1024', help='window length')
        self.parser.add_argument('--hl', type=int, default='512', help='hop length')
        self.parser.add_argument('--cl', type=int, default='128', help='signal crop length')
        self.parser.add_argument('--amp_only', action='store_true', help='if specified, discard phase output')

        if self.inverse:
            self.parser.add_argument('--phase_input', required=True, help='path to phase file or directory')

    def parse_cmdargs(self):
        self.opt = self.parser.parse_args() 
        return self.opt
    
    def parse(self, input, output = None, sr = None, stereo = None, crop = None, wl = None, hl = None, cl = None, amp_only = None, phase_input = None):

        if self.inverse:
            self.opt = self.parser.parse_args(args=["--input", input, "--phase_input", phase_input])
        else:
            self.opt = self.parser.parse_args(args=["--input", input])

        if output == None:
            self.opt.output = self.default_output
        else:
            self.opt.output = output
        if sr == None:
            self.opt.sr = self.default_sr
        else:
            self.opt.sr = sr
        if stereo == None:
            self.opt.stereo = self.default_stereo
        else:
            self.opt.stereo = stereo
        if crop == None:
            self.opt.crop = self.default_crop
        else:
            self.opt.crop = crop
        if wl == None:
            self.opt.wl = self.defalut_wl
        else:
            self.opt.wl = wl
        if hl == None:
            self.opt.hl = self.defalut_hl
        else:
            self.opt.hl = hl
        if cl == None:
            self.opt.cl = self.defalut_hl
        else:
            self.opt.cl = cl
        if amp_only == None:
            self.opt.amp_only = self.default_amp_only
        else:
            self.opt.amp_only = amp_only

        return self.opt


    # def gather_options(self):
    #     if not self.initialized:  # check if it has been initialized
    #         parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #         parser = self.initialize(parser)

    #     # get the basic options
    #     opt, _ = parser.parse_known_args()

    #     # modify model-related parser options
    #     model_name = opt.model
    #     model_option_setter = models.get_option_setter(model_name)
    #     parser = model_option_setter(parser, self.isTrain)
    #     opt, _ = parser.parse_known_args()  # parse again with new defaults

    #     # modify dataset-related parser options
    #     dataset_name = opt.dataset_mode
    #     dataset_option_setter = data.get_option_setter(dataset_name)
    #     parser = dataset_option_setter(parser, self.isTrain)

    #     # save and return the parser
    #     self.parser = parser
    #     return parser.parse_args()

    #     def parse(self):    
    #         opt = self.gather_options()
    #         opt.isTrain = self.isTrain   # train or test

    #     # process opt.suffix
    #     if opt.suffix:
    #         suffix = ('_' + opt.suffix.format(**vars(opt))) if opt.suffix != '' else ''
    #         opt.name = opt.name + suffix

    #     self.print_options(opt)

    #     # set gpu ids
    #     str_ids = opt.gpu_ids.split(',')
    #     opt.gpu_ids = []
    #     for str_id in str_ids:
    #         id = int(str_id)
    #         if id >= 0:
    #             opt.gpu_ids.append(id)
    #     if len(opt.gpu_ids) > 0:
    #         torch.cuda.set_device(opt.gpu_ids[0])

    #     self.opt = opt
    #     return self.opt

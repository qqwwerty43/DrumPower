import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
import kivy.utils as utils
import math


Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '720')


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class DrumPower(App):
    def build(self):
        self.samplepack = ['rnb', 'trap', 'house']
        self.loop = [SoundLoader.load(f'samplepacks\{self.samplepack[0]}\loop{i+1}.wav') for i in range(8)]
        self.oneshot = [SoundLoader.load(f'samplepacks\{self.samplepack[0]}\oneshot{i+1}.wav') for i in range(16)]
        for i in range(8):
            self.loop[i].loop = True

        self.root.ids['btn_samplepack'].text = self.samplepack[0]

        self.root.ids['lbl_loop_path'].text = self.loop[0].source
        self.root.ids['sld_loop_volume'].value = self.loop[0].volume * 100
        # self.root.ids['sld_loop_pitch'].value = math.log2(self.loop[0].pitch) * 12
        self.root.ids['lbl_loop_volume_value'].text = str(int(self.root.ids['sld_loop_volume'].value))
        # self.root.ids['lbl_loop_pitch_value'].text = str(int(self.root.ids['sld_loop_pitch'].value))

        self.root.ids['lbl_oneshot_path'].text = self.oneshot[0].source
        self.root.ids['sld_oneshot_volume'].value = self.oneshot[0].volume * 100
        # self.root.ids['sld_oneshot_pitch'].value = math.log2(self.oneshot[0].pitch) * 12
        self.root.ids['lbl_oneshot_volume_value'].text = str(int(self.root.ids['sld_oneshot_volume'].value))
        # self.root.ids['lbl_oneshot_pitch_value'].text = str(int(self.root.ids['sld_oneshot_pitch'].value))
    pass

    def change_path(self, sample, path):
        loop = sample.loop
        volume = sample.volume
        pitch = sample.pitch
        sample.unload()
        sample = SoundLoader.load(path)
        sample.loop = loop
        sample.volume = volume
        sample.pitch = pitch
        return sample

    def change_volume_loop(self, name, volume):
        index = int(name.text[5:])
        self.loop[index - 1].volume = volume / 100
        self.root.ids['lbl_loop_volume_value'].text = str(int(volume))

    def change_volume_oneshot(self, name, volume):
        index = int(name.text[9:])
        self.oneshot[index - 1].volume = volume / 100
        self.root.ids['lbl_oneshot_volume_value'].text = str(int(volume))

    # def change_pitch_loop(self, name, pitch):
    #     index = int(name.text[5:])
    #     self.loop[index - 1].pitch = pow(2, pitch / 12)
    #     self.root.ids['lbl_loop_pitch_value'].text = str(int(pitch))
    #
    # def change_pitch_oneshot(self, name, pitch):
    #     index = int(name.text[9:])
    #     self.oneshot[index - 1].pitch = pow(2, pitch / 12)
    #     self.root.ids['lbl_oneshot_pitch_value'].text = str(int(pitch))

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load_loop(self):
        content = LoadDialog(load=self.load_loop, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_loop(self, path, filename):
        # with open(os.path.join(path, filename[0])) as stream:
        self.loop[int(self.root.ids['lbl_loop'].text[5:]) - 1] = self.change_path(
            self.loop[int(self.root.ids['lbl_loop'].text[5:]) - 1], filename[0])
        self.root.ids['lbl_loop_path'].text = filename[0]
        self.dismiss_popup()

    def show_load_oneshot(self):
        content = LoadDialog(load=self.load_oneshot, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_oneshot(self, path, filename):
        # with open(os.path.join(path, filename[0])) as stream:
        self.oneshot[int(self.root.ids['lbl_oneshot'].text[9:]) - 1] = self.change_path(
            self.oneshot[int(self.root.ids['lbl_oneshot'].text[9:]) - 1], filename[0])
        self.root.ids['lbl_oneshot_path'].text = filename[0]
        self.dismiss_popup()

    def change_samplepack(self):
        btn = self.root.ids['btn_samplepack']
        i = self.samplepack.index(btn.text)
        if i != len(self.samplepack) - 1:
            for a in range(8):
                self.loop[a] = self.change_path(
                    self.loop[a], f'samplepacks\{self.samplepack[i + 1]}\loop{a+1}.wav')
            for a in range(16):
                self.oneshot[a] = self.change_path(
                    self.oneshot[a], f'samplepacks\{self.samplepack[i + 1]}\oneshot{a+1}.wav')
            btn.text = self.samplepack[i + 1]
        else:
            for a in range(8):
                self.loop[a] = self.change_path(
                    self.loop[a], f'samplepacks\{self.samplepack[0]}\loop{a+1}.wav')
            for a in range(16):
                self.oneshot[a] = self.change_path(
                    self.oneshot[a], f'samplepacks\{self.samplepack[0]}\oneshot{a+1}.wav')
            btn.text = self.samplepack[0]

    def play_loop(self, id):
        if self.loop[id].state == 'play':
            self.loop[id].stop()
            self.root.ids[f'btn_loop{id+1}'].background_color = utils.get_color_from_hex('#52FFC7')
        else:
            self.loop[id].play()
            self.root.ids[f'btn_loop{id+1}'].background_color = utils.get_color_from_hex('#52C7FF')

    def play_oneshot(self, id):
        self.oneshot[id].play()

    def change_loop_setting_prev(self):
        lbl = int(self.root.ids['lbl_loop'].text[5:])
        pth = self.root.ids['lbl_loop_path']
        if lbl == 1:
            lbl = 8
        else:
            lbl -= 1

        self.root.ids['lbl_loop'].text = self.root.ids['lbl_loop'].text[:5] + str(lbl)
        pth.text = self.loop[lbl - 1].source

        self.root.ids['sld_loop_volume'].value = self.loop[lbl - 1].volume * 100
        # self.root.ids['sld_loop_pitch'].value = math.log2(self.loop[lbl - 1].pitch) * 12
        self.root.ids['lbl_loop_volume_value'].text = str(int(self.root.ids['sld_loop_volume'].value))
        # self.root.ids['lbl_loop_pitch_value'].text = str(int(self.root.ids['sld_loop_pitch'].value))

    def change_loop_setting_next(self):
        lbl = int(self.root.ids['lbl_loop'].text[5:])
        pth = self.root.ids['lbl_loop_path']
        if lbl == 8:
            lbl = 1
        else:
            lbl += 1

        self.root.ids['lbl_loop'].text = self.root.ids['lbl_loop'].text[:5] + str(lbl)
        pth.text = self.loop[lbl - 1].source

        self.root.ids['sld_loop_volume'].value = self.loop[lbl - 1].volume * 100
        # self.root.ids['sld_loop_pitch'].value = math.log2(self.loop[lbl - 1].pitch) * 12
        self.root.ids['lbl_loop_volume_value'].text = str(int(self.root.ids['sld_loop_volume'].value))
        # self.root.ids['lbl_loop_pitch_value'].text = str(int(self.root.ids['sld_loop_pitch'].value))

    def change_oneshot_setting_prev(self):
        lbl = int(self.root.ids['lbl_oneshot'].text[9:])
        pth = self.root.ids['lbl_oneshot_path']
        if lbl == 1:
            lbl = 16
        else:
            lbl -= 1

        self.root.ids['lbl_oneshot'].text = self.root.ids['lbl_oneshot'].text[:9] + str(lbl)
        pth.text = self.oneshot[lbl - 1].source

        self.root.ids['sld_oneshot_volume'].value = self.oneshot[lbl - 1].volume * 100
        # self.root.ids['sld_oneshot_pitch'].value = math.log2(self.oneshot[lbl - 1].pitch) * 12
        self.root.ids['lbl_oneshot_volume_value'].text = str(int(self.root.ids['sld_oneshot_volume'].value))
        # self.root.ids['lbl_oneshot_pitch_value'].text = str(int(self.root.ids['sld_oneshot_pitch'].value))

    def change_oneshot_setting_next(self):
        lbl = int(self.root.ids['lbl_oneshot'].text[9:])
        pth = self.root.ids['lbl_oneshot_path']
        if lbl == 16:
            lbl = 1
        else:
            lbl += 1

        self.root.ids['lbl_oneshot'].text = self.root.ids['lbl_oneshot'].text[:9] + str(lbl)
        pth.text = self.oneshot[lbl - 1].source

        self.root.ids['sld_oneshot_volume'].value = self.oneshot[lbl - 1].volume * 100
        # self.root.ids['sld_oneshot_pitch'].value = math.log2(self.oneshot[lbl - 1].pitch) * 12
        self.root.ids['lbl_oneshot_volume_value'].text = str(int(self.root.ids['sld_oneshot_volume'].value))
        # self.root.ids['lbl_oneshot_pitch_value'].text = str(int(self.root.ids['sld_oneshot_pitch'].value))



if __name__ == '__main__':
    LabelBase.register(name='Lordcorps',
                       fn_regular='Lordcorps[RUSbyPenka220]-Stencil.ttf')
    DrumPower().run()
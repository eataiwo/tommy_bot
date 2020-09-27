import simpleaudio as sa
import wave
from io import StringIO, BytesIO
from picotts import PicoTTS


picotts = PicoTTS()
wav = picotts.synth_wav('omelette du fromage')
#wav = wave.open(BytesIO(wavs), 'rb')

play_obj = sa.play_buffer(wav, 2, 2, 8000)
play_obj.wait_done()

picotts.voice = 'fr-FR'
wav = picotts.synth_wav('omelette du fromage')
play_obj = sa.play_buffer(wav, 2, 2, 8000)
play_obj.wait_done()

picotts.voice = 'en-GB'
wav = picotts.synth_wav('omelette du fromage')
wav = sa.WaveObject(wav, 2, 2, 8000)
another_obj = wav.play()
another_obj.wait_done()

picotts.voice = 'en-GB'
wav = picotts.synth_wav('Hi there, I am tommy. I am ready for an adventure')
wav = sa.WaveObject(wav, 2, 2, 8000)
another_obj = wav.play()
another_obj.wait_done()

picotts.voice = 'fr-FR'
wav = picotts.synth_wav('Hi there, I am tommy. I am ready for an adventure')
wav = sa.WaveObject(wav, 2, 2, 8000)
another_obj = wav.play()
another_obj.wait_done()

#print (wav.getnchannels(), wav.getframerate(), wav.getnframes())




import wave
import pyaudio
from io import StringIO, BytesIO
from picotts import PicoTTS

chunk = 1024

picotts = PicoTTS()
wavs = picotts.synth_wav('Hello World! Doing more testing')
wav = wave.open(BytesIO(wavs), 'rb')

p = pyaudio.PyAudio()

print(wav.getframerate())
print(type(wav.getframerate()))

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = p.get_format_from_width(wav.getsampwidth()),
                channels = wav.getnchannels(),
                rate = 48000,
                output = True)

print(format)

# Read data in chunks
data = wav.readframes(chunk)

# Play the sound by writing the audio data to the stream
while data != '':
    stream.write(data)
    data = wav.readframes(chunk)

# Close and terminate the stream
stream.close()
p.terminate()

print(wav.getnchannels(), wav.getframerate(), wav.getnframes())

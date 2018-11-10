import pyaudio
import wave

CHUNK = 1024
def wave_play(filename):
    wf = wave.open(filename)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)


    data = wf.readframes(CHUNK)
    while data!=b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    
    p.terminate()

def main():
    filename = input("ファイル名を入力してください")
    wave_play(filename)

if __name__=="__main__":
    main()
import pyaudio
import wave
import sys,os,re
from pydub import AudioSegment


CHUNK = 1024
CHAR_UNIT = ['零','一','二','三','四','五','六','七','八','九']
CHAR_UNIT_SP = ['十','百','千','万','亿']
CHAR_SYMBOL = ['负','点']
wave_path = './num_wav'

def get_wav_sequence(input_num):
    wav_list = []
    out_str = ''
    has_minus = False
    if '-' in input_num:
        input_num = input_num.strip('-')
        has_minus = True
    if '.' in input_num:
        input_num, dot_part = input_num.split('.')
        for i in range(len(dot_part)):
            digit = str(dot_part[len(dot_part)-i-1])
            out_str+=CHAR_UNIT[int(digit)]
            wav_list.append(wave_path+'/'+digit+'_xiaoyan.wav')
        wav_list.append(wave_path+'/dot.wav')
        out_str+=CHAR_SYMBOL[1]
    for i in range(len(input_num)):
        if i!=0:
            index = i-1
            if i==8:
                index=4
            elif i>8 and i<12:
                index-=8
            elif i>4 and i<8:
                index-=4
            wav_list.append(wave_path+'/'+str(index+10)+'_xiaoyan.wav')
            out_str+=CHAR_UNIT_SP[index]
        digit = str(input_num[len(input_num)-i-1])
        out_str+=CHAR_UNIT[int(input_num[len(input_num)-i-1])]
        wav_list.append(wave_path+'/'+digit+'_xiaoyan.wav')
    if has_minus:
        wav_list.append(wave_path+'/minus.wav')
        out_str += CHAR_SYMBOL[0]
    wav_list.append(wave_path+'/start.wav')
    wav_list.reverse()
    wav_list.append(wave_path+'/yuan.wav')
    out_str = out_str[::-1]
    return wav_list, out_str


tts_num = sys.argv[1]
wav_list=[]
p = pyaudio.PyAudio()
i = 1

wav_list, out_str = get_wav_sequence(str(tts_num))

print(out_str)

wav_data = AudioSegment.from_wav(wav_list[0])
while i < len(wav_list):
    song = AudioSegment.from_wav(wav_list[i])[:]
    wav_data = wav_data+song
    i+=1
wav_data.export('./temp.wav',format='wav')

wp = wave.open('./temp.wav','rb')
# open stream (2)
stream = p.open(format=p.get_format_from_width(wp.getsampwidth()),
                channels=wp.getnchannels(),
                rate=wp.getframerate(),
                output=True)

# read data
data = wp.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wp.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
#!/usr/bin/python3.6
import pyaudio,wave,signal,os,time,sys
from datetime import datetime
from threading import Thread

Stop = False
Dtime = (datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
OptDir = "NewRecShot-" + str(Dtime)

if os.path.exists(OptDir) is False:
   os.makedirs(OptDir)

def handler(signum, frame):
        global Stop
        Stop = True
        print("Recording has stopped")
 
signal.signal(signal.SIGINT, handler)


def Enum_Devices():
   audio = pyaudio.PyAudio()
   info = audio.get_host_api_info_by_index(0)
   numdevices = info.get('deviceCount')
#   Mic_Name = "USB Microphone: Audio"
   Mic_Name = "pulse"
   Dev_Id = ""
   for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
           print("id(%s):%s"%(i,audio.get_device_info_by_host_api_device_index(0, i).get('name')))
           if Mic_Name in audio.get_device_info_by_host_api_device_index(0, i).get('name'):
              Dev_Id = i
   return(Dev_Id)

def Screenshot():
   print("Screenshooting..")
   while Stop is False:
      Dtime = (datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
      Screename = "SShot-" + str(Dtime) + ".png"
      cmd = "import -window root %s/%s"%(OptDir,Screename)
      os.system(cmd)
      time.sleep(0.2)
   print("Screenshot() has stopped")

def Record():

   Wavname = "Rec-%s.wav"%str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
   audio = pyaudio.PyAudio()
   info = audio.get_host_api_info_by_index(0)
   frames = []
   Mic_Device = Enum_Devices()
   if type(Mic_Device) == int:
       Mic_Rate = int(audio.get_device_info_by_index(Mic_Device).get('defaultSampleRate'))
       stream = audio.open(format=pyaudio.paInt16, channels=1,
                rate=Mic_Rate, input=True,input_device_index = Mic_Device,
                frames_per_buffer=512)
       Thread(target = Screenshot).start()
       print("Recording ...")
       while Stop is False:
                try:
                   chunk = stream.read(512)
                   frames.append(chunk)
                except Exception as e:
                   print("Error:",e)
       stream.stop_stream()
       stream.close()
       audio.terminate()
       try:
          with wave.open(OptDir+"/"+str(Wavname),"wb") as w:
               w.setnchannels(1)
               w.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
               w.setframerate(Mic_Rate)
               w.writeframes(b''.join(frames))
       except Exception as e:
           print("Error:",str(e))
   else:
      print("\n\nMic not found")

   print("Exiting")
   sys.exit()

Record()

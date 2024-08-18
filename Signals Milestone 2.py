import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import math
import sounddevice as sd

t = np.linspace(0, 3, 12*1024)
# 12*1024 is the number of samples
leftFreq = np.array([220, 196, 174.61, 164.81, 130.81])
# frequencies for the left notes
rightFreq = np.array([261.63, 293.66, 440, 392, 493.88])
# frequencies for the right notes
startTime = np.array([0, 0.5, 1, 1.5, 2])
# starting time for each note
interval = np.array([0.5, 0.4, 0.5, 0.4, 0.9])
# interval for each note
i = 0
# index and counter for the while loop
stop = 5
# bec i have 5 notes
sumNotes = 0
# sum of all notes

while (stop > i):
    leftNote = np.sin(2*np.pi*leftFreq[i]*t)
    # ith left note using ith left note frequency
    rightNote = np.sin(2*np.pi*rightFreq[i]*t)
    # ith right note using ith right note frequency
    sumNotes =sumNotes+((leftNote+rightNote)*((t>=startTime[i])&(t<=(startTime[i]+interval[i]))))
    # ((t>=ST)&(t<=(ST+I))) represents the unit step using ith note starting time and ith note interval
    # 𝑥𝑡=෍𝑖=1𝑁[sin2𝜋Ϝ𝑖𝑡+sin2𝜋𝑓𝑖𝑡][𝑢(𝑡−𝑡𝑖)−𝑢(𝑡−𝑡𝑖−𝑇𝑖)]
    i = i+1
    # incrementation

plt.figure()
plt.plot(t, sumNotes)
plt.title('Time Domain Signal 1')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()
# plotting the notes

sd.play(sumNotes,3*1024)

# playing the notes

N = 3*1024  # no of samples
freq = np.linspace(0, 512, int(N/2))  # to only get positive values

x_f = fft(sumNotes)  # complex signal
x_f = 2/N * np.abs(x_f[0:int(N/2)])  # to get the values of the -ve side
# /N (size of sample) to make it relevant to the sample size
plt.figure()
plt.plot(freq, x_f)
plt.title('Frequency Domain Signal 1')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.show()

# random generate values for the noise
fn1, fn2 = np. random. randint(0, 512, 2)
noise = sumNotes + np.sin(2*np.pi*fn1*t) + np.sin(2*np.pi*fn2*t)  # add the noise
plt.figure()
plt.plot(t, noise)
plt.title('Time Domain Signal with noise')
plt.xlabel('Time')
plt.ylabel('Amplitude')
sd.play(noise,3*1024)
plt.show()


noisef = fft(noise)  # complex signal
noisef = 2/N * np.abs(noisef[0:int(N/2)])
plt.figure()
plt.plot(freq, noisef)
plt.title('Frequency Domain Signal with noise')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.show()

# search for the noise add to list
#checks if there's a frequency > the frequencies in the x_f and places them in an array
noiseList = np.where(noisef > math.ceil(np.max(x_f)))
index1 = noiseList[0][0]
index2 = noiseList[0][1]

freq1 = int(freq[index1])  # get value of noise
freq2 = int(freq[index2])  # get value of noise

xfiltered = noise - (np.sin(2*np.pi*freq1*t) +
                     np.sin(2*np.pi*freq2*t))  # remove noise
plt.figure()
plt.plot(t, xfiltered)
plt.title('Time Domain Signal with filter')
plt.xlabel('Time')
plt.ylabel('Amplitude')
sd.play(xfiltered,3*1024)
plt.show()

xfilteredf = fft(xfiltered)
xfilteredf = 2/N * np.abs(xfilteredf[0:int(N/2)])
plt.figure()
plt.plot(freq, xfilteredf)
plt.title('Frequency Domain Signal with filter')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.show()

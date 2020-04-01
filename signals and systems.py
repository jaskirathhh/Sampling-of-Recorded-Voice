import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
import wave
import math
import scipy.io.wavfile
import scipy.fftpack


################################################PART-1################################################################################
'''1. Record your own voice, for different sampling rate (6000, 8000, 10000, 16000, 20000 and 44100
    Hz). Decide a sampling rate for your voice. Name that sampled voice as sampled voice.'''


'''Defining our own parameters required ,like
sampling frequency (Fs) and time for which we
want to record our voive'''

time = 1                                #duration for which sound is recorded
freqs = 6000                           #Sampling Frequency of our voice

#Recording part 

print("Recorder ON")

recordingArray = sd.rec(int(freqs*time),freqs,1,blocking = True)

print("Recorder OFF")

#saving audio to a wave file
scipy.io.wavfile.write("sampled_voice.wav",freqs,recordingArray)


################################################PART-2#################################################################################
'''2. Plot your sampled voice in time domain.'''

#Ploting our recorded audio

recordingArray = np.array(recordingArray)

plt.title("Recording (6000Hz)")
plt.xlabel("n")                                                                     #labeling x axis which are intervals of time 
plt.ylabel("x[n]")                                                                  #these are amplitude of audio at that interval
plt.xlim(1,6000)
plt.plot(abs(recordingArray))
plt.show()
#plt.stem(np.arange(len(recordingArray)),recordingArray,use_line_collection = True)
#plt.show()

#playing back recorded audio to check what has been recorded
sd.play(recordingArray,freqs)


################################################PART-3#################################################################################
'''3. Take the Fourier transform of your sampled voice and plot it in frequency domain. (Write
        your own function for Fourier transform and Inverse Fourier transform) sampled voice freq'''
N = 6000
def DTFT(Array,N):
    
    power = (-1j*2*np.pi)/N
    fourierTransform = []
    for w in range(-3000,3001):
        X_W = 0
        for n in range(0,N):
            X_W += Array[n]*np.exp(power*w*n)

        fourierTransform.append(X_W)
        
    return  np.array(fourierTransform)

fourierTransformArray = DTFT(recordingArray,N)


plt.title("DTFT")
plt.xlabel("ω")                                                                     
plt.ylabel("X(ω)")   
plt.plot(abs(fourierTransformArray))
plt.show()

################################################PART-4#################################################################################
'''4. Report the bandwidth of your sampled voice (Bw)'''
print("Bandwidth is found to be 2500Hz")

################################################PART-5#################################################################################
'''5. Take the inverse Fourier transform of sampled voice freq. Plot this signal, play the voice of
this signal.'''

'''Taking inverse fourier transform'''

def IDTFT(Array,N):
    exp_power = (1j*2*np.pi)/N
    inverseFourierTransform = []
    for n_ in range(0,N):
        x_n = 0
        for w_ in range(-3000,3001):
            x_n += Array[w_]*np.exp(exp_power*n_*w_)
            
        inverseFourierTransform.append(x_n/N)

    return np.array(inverseFourierTransform)

inverseDTFTarray = abs(IDTFT(fourierTransformArray,N))

plt.title("Inverse DTFT")
plt.xlabel("n")                                                                      
plt.ylabel("x[n]")                                                                       
plt.plot((inverseDTFTarray))
plt.show()

#saving recovered audio to a wave file
scipy.io.wavfile.write("recovered_sampled_voice.wav",freqs,inverseDTFTarray)


################################################PART-6#################################################################################
'''6. Remove the higher frequency components from your voice, i.e remove the frequency component
more than 0.8Bw. Plot the time domain signal corresponding to this, play this signal, report
the difference corresponding to the original signal.'''

modified_bandwidth = int(0.8*2500)
new_array_after_removing_higher_freq = []
for i in range(0,len(fourierTransformArray)):
    if i in range(2500,5000):
        new_array_after_removing_higher_freq.append(fourierTransformArray[i])
    else:
        new_array_after_removing_higher_freq.append(0)
        
new_IDTFT = abs(np.array(IDTFT(new_array_after_removing_higher_freq,N)))

plt.title("Inverse DTFT(without higher freq)")
plt.xlabel("n")                                                                      
plt.ylabel("x[n]")                                                                       
plt.plot(new_IDTFT)
plt.show()

scipy.io.wavfile.write("recovered_sampled_voice_with_no_higher_freq.wav",freqs,new_IDTFT)

        

################################################PART-7#################################################################################
'''7. Set the phase response of the sampled voice as 0. Plot the time domain signal corresponding
to this, play this signal, report the difference corresponding to the original signal.'''

new_array = []
for ele in fourierTransformArray:
    new_array.append(np.real(ele))
    
real_inverseDTFT_array = abs(IDTFT(new_array,N))
plt.title("Inverse DTFT(with zero phase)")
plt.xlabel("n")                                                                      
plt.ylabel("x[n]")                                                                       
plt.plot(real_inverseDTFT_array)
plt.show()

scipy.io.wavfile.write("recovered_sampled_voice_with_zero_phase.wav",freqs,real_inverseDTFT_array)

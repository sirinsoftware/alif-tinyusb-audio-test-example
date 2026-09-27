#!/usr/bin/env python3
# This file is derived from the TinyUSB project example
# examples/device/audio_test/src/plot_audio_samples.py, which is distributed
# under the MIT licence; a verbatim copy is provided in LICENSE-MIT.txt.
#
# The modifications in this file were developed for the Alif Semiconductor
# platform. Published by Sirin Software as a collaboration snapshot.
#
# This repository combines material under several licences; see README.md
# and THIRD_PARTY_NOTICES.txt.

import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import platform
import csv

if __name__ == '__main__':

    # If you got "ValueError: No input device matching", that is because your PC name example device
    # differently from tested list below. Uncomment the next line to see full list and try to pick correct one
    # print(sd.query_devices())

    fs = 48000           # Sample rate
    duration = 3    # Duration of recording

    if platform.system() == 'Windows':
        # MME is needed since there are more than one MicNode device APIs (at least in Windows)
        device = 'Microphone (MicNode), Windows WASAPI'
    elif platform.system() == 'Darwin':
        device = 'MicNode'
    elif platform.system() == 'Linux':
        device = 'micnode'
    else:
        device ='default'

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device=device)
    print('Waiting...')
    sd.wait()  # Wait until recording is finished
    print('Done!')

    time = np.arange(0, duration, 1 / fs)  # time vector
    plt.plot(time, myrecording)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('MicNode')
    plt.show()

    samples = np.array(myrecording)
    np.savetxt('Output.csv', samples, delimiter=",", fmt='%s')

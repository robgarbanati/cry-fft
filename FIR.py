from pylab import *
import scipy.signal as signal

#Plot frequency and phase response
def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * log10 (abs(h))
    subplot(211)
    plot(w/max(w),h_dB)
    ylim(-150, 5)
    ylabel('Magnitude (db)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Frequency response')
    subplot(212)
    h_Phase = unwrap(arctan2(imag(h),real(h)))
    plot(w/max(w),h_Phase)
    ylabel('Phase (radians)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Phase response')
    subplots_adjust(hspace=0.5)


#boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen, bohman, blackmanharris, nuttall, barthann, kaiser (needs beta), gaussian (needs std), general_gaussian (needs power, width), slepian (needs width), chebwin (needs attenuation)

n = 65

#Lowpass filter
a = signal.firwin(n, cutoff = 0.1, window = ('kaiser', 1.0))
for i,number in enumerate(a):
    if abs(number) < 1e-15:
	a[i] = 0
print 'roundeda'
print a

##Highpass filter with spectral inversion
#b = - signal.firwin(n, cutoff = 0.5, window = ('kaiser', 1.0)); b[n/2] = b[n/2] + 1
#for i,number in enumerate(b):
    #if abs(number) < 1e-15:
	#b[i] = 0
#print 'roundedb'
#print b
##Combine into a bandpass filter
#d = - (a+b); d[n/2] = d[n/2] + 1
print 'a'
print a
#Frequency response
mfreqz(a)
show()

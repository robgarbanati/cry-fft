

def FIR_bandpass_filter(data, lowcut, highcut):
    y = scipy.signal.convolve(data, d)
    print 'FIRy'
    print y
    return y

def initialize_FIR_BP_filter():
    n = 63
    #Lowpass filter
    a = signal.firwin(n, cutoff = 0.2, window = ('kaiser', 1.0))
    for i,number in enumerate(a):
	if abs(number) < 1e-15:
	    a[i] = 0

    #Highpass filter with spectral inversion
    b = - signal.firwin(n, cutoff = 0.225, window = ('kaiser', 1.0)); b[n/2] = b[n/2] + 1
    for i,number in enumerate(b):
	if abs(number) < 1e-15:
	    b[i] = 0

    FIR_filt = - (a+b); FIR_filt[n/2] = FIR_filt[n/2] + 1
    #print 'FIR_filt'
    #print FIR_filt
    return FIR_filt

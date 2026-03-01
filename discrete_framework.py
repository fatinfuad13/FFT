import numpy as np

class DiscreteSignal:
    """
    Represents a discrete-time signal.
    """
    def __init__(self, data):
        # Ensure data is a numpy array, potentially complex
        self.data = np.array(data, dtype=np.complex128)

    def __len__(self):
        return len(self.data)
        
    def pad(self, new_length):
        """
        Zero-pad or truncate signal to new_length.
        Returns a new DiscreteSignal object.
        """
        # TODO: Implement padding logic
        # Placeholder return to prevent crash
        curr_len = len(self.data)

        if new_length == curr_len:
            return DiscreteSignal(self.data.copy())

        elif new_length < curr_len:
            return DiscreteSignal(self.data[:new_length])

        else:
            padded = np.zeros(new_length,dtype=np.complex128)
            padded[:curr_len] = self.data
            return DiscreteSignal(padded)

    def interpolate(self, new_length):
        """
        Resample signal to new_length using linear interpolation.
        Required for Task 4 (Drawing App).
        """
        # TODO: Implement interpolation logic
        curr_len = len(self.data)

        if curr_len == new_length:
            return DiscreteSignal(self.data.copy())

        old_indices = np.linspace(0,1,curr_len)
        new_indices = np.linspace(0,1,new_length)

        real_part = np.interp(new_indices,old_indices,self.data.real)
        imaginary_part = np.interp(new_indices,old_indices,self.data.imag)

        interpolated = real_part + 1j*imaginary_part
        return DiscreteSignal(interpolated)


class DFTAnalyzer:
    """
    Performs Discrete Fourier Transform using O(N^2) method.
    """
    def compute_dft(self, signal: DiscreteSignal):
        """
        Compute DFT using naive summation.
        Returns: numpy array of complex frequency coefficients.
        """
        N = len(signal)
        # TODO: Implement Naive DFT equation
        # Placeholder: Return zeros so UI doesn't crash
        x = signal.data
        X = np.zeros(N,dtype=np.complex128)

        for k in range(N):
            sum = 0
            for n in range(N):
                angle = (-2j * np.pi * k * n)/N
                sum += x[n] * np.exp(angle)
            X[k] = sum



        return X

    def compute_idft(self, spectrum):
        """
        Compute Inverse DFT using naive summation.
        Returns: numpy array (time-domain samples).
        """
        # TODO: Implement Naive IDFT equation

        X = np.array(spectrum,dtype=np.complex128)
        N = len(X)

        x = np.zeros(N, dtype=np.complex128)

        for n in range(N):
            sum = 0
            for k in range(N):
                angle = (2j * np.pi * k * n)/N
                sum += X[k] * np.exp(angle)
            x[n] = sum/N

        return x



'''signal = DiscreteSignal([1, 2, 3, 4])
dft = DFTAnalyzer()

X = dft.compute_dft(signal)
x_reconstructed = dft.compute_idft(X)

print(signal.data)
print(x_reconstructed)'''

class FastFourierTransform(DFTAnalyzer):
    """
    Radix-2 Decimation-in-Time Cooley-Tukey FFT
    """
    def compute_dft(self, signal: DiscreteSignal):
        """
        Compute FFT using recursive radix-2 DIT.
        Input length must be a power of 2. Zero-pad if necessary.
        Returns: numpy array of complex frequency coefficients.
        """
        x = signal.data
        N = len(x)

        # If N is not a power of 2, pad with zeros
        if not (N != 0 and ((N & (N - 1)) == 0)):
            next_pow2 = 1 << (N-1).bit_length()
            padded = np.zeros(next_pow2, dtype=np.complex128)
            padded[:N] = x
            x = padded
            N = next_pow2

        return self._fft_recursive(x)

    def _fft_recursive(self, x):
     N = len(x)

    # Base case
     if N == 1:
        return x

    # Recursively compute even and odd parts
     X_even = self._fft_recursive(x[0::2])
     X_odd = self._fft_recursive(x[1::2])

    # Allocate output
     X = np.zeros(N, dtype=complex)

    # Combine
     for m in range(N):
        m_alias = m % (N // 2)

        twiddle = np.exp(-2j * np.pi * m / N)

        X[m] = X_even[m_alias] + twiddle * X_odd[m_alias]

     return X

    def compute_idft(self, spectrum):
        """
        Compute inverse FFT.
        """
        N = len(spectrum)
        # Conjugate, compute FFT, then conjugate again
        x_conj = np.conjugate(spectrum)
        result = self._fft_recursive(x_conj)
        return np.conjugate(result) / N
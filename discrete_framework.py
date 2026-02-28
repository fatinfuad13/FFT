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


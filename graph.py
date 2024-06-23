import numpy as np
import matplotlib.pylab as plt

# Define your data (e.g., binary stream)
data = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]  # Example data

# Map data to 4D-PAM5 symbols (you'll need a lookup table)
# For simplicity, assume each symbol lasts for T seconds

# Create time vector
T = 1.0  # Symbol duration (adjust as needed)
time = np.arange(0, len(data) * T, T)

# Generate PAM5 waveform (replace with your mapping logic)
pam5_waveform = []  # List of voltage levels

# ------------------------------------------- CODING -----------------------------------------------_#

for i in range(0, len(data), 2):
    # Extract two bits
    bits = data[i:i + 2]
    
    # Map to PAM5 voltage level
    if bits == [0, 0]:
        pam5_waveform.append(-2)  # -2V
    elif bits == [1, 0]:
        pam5_waveform.append(-1)  # -1V
    elif bits == [0, 1]:
        pam5_waveform.append(1)   # +1V
    elif bits == [1, 1]:
        pam5_waveform.append(2)   # +2V
    else:
        pam5_waveform.append(0)   # probably useless    

# ------------------------------------------- CODING ------------------------------------------------#

# Create time axis
time = np.arange(len(pam5_waveform))

# Upsample PAM5 levels to create a square waveform
square_waveform = np.repeat(pam5_waveform, int(1 / T))

# ------------------------------------------ DECODING -----------------------------------------------#
outBits = []
for i in range(len(pam5_waveform)):
    if pam5_waveform[i] == -2:
        outBits.append(0)
        outBits.append(0)
    elif pam5_waveform[i] == -1:
        outBits.append(1)
        outBits.append(0)
    elif pam5_waveform[i] == 1:
        outBits.append(0)
        outBits.append(1)
    elif pam5_waveform[i] == 2:
        outBits.append(1)
        outBits.append(1)
    elif pam5_waveform[i] == 0:
        print("No signal")  #probably useless
    else:
        print("Invalid")

# ------------------------------------------ DECODING -----------------------------------------------#

#Just checking if the signal are the same
"""
print(outBits)
print(data)
"""


# Plot the waveform
plt.plot(time, square_waveform, drawstyle="steps-pre", marker="o", linestyle="-", color="b", label="PAM5 Signal")
plt.axhline(y=0, color='red', linestyle='--', label='Zero Voltage')
plt.xlabel("Time")
plt.ylabel("Voltage Level")
plt.title("PAM5 Square Waveform")
plt.grid(True)
plt.legend()
plt.show()


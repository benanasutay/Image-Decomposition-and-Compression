import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_frequency_response(h, N, title):
    H = np.fft.fft(h, 512)
    H = np.fft.fftshift(H) 
    freq = np.linspace(-np.pi, np.pi, len(H))
    plt.plot(freq, np.abs(H)**2)
    plt.title(f"{title} - Magnitude Square Frequency Response")
    plt.xlabel('Frequency (radians/sample)')
    plt.ylabel('Magnitude Squared')
    plt.grid()
    plt.show()

def pr_condition(h0, h1, g0, g1):
    N = len(h0)
    delta = np.zeros(N)
    delta[0] = 1

    conv_h0_g0 = np.convolve(h0, g0)
    conv_h1_g1 = np.convolve(h1, g1)
    conv_sum = conv_h0_g0 + conv_h1_g1
    
    return np.allclose(conv_sum[:N], delta)

def apply_filter(image, h):
    
    image = np.array(image)
    output = np.zeros_like(image)
    
    for i in range(image.shape[0]):
        output[i, :] = np.convolve(image[i, :], h, mode='same')
    
    for j in range(image.shape[1]):
        output[:, j] = np.convolve(output[:, j], h, mode='same')
    
    return output

def decompose_image(image, h0, h1, levels):
    sub_bands = []
    current_image = image.copy()

    for _ in range(levels):
        low_pass = apply_filter(current_image, h0)
        high_pass = apply_filter(current_image, h1)
        sub_bands.append(high_pass)
        current_image = low_pass
    
    sub_bands.append(current_image)  
    return sub_bands

def reconstruct_image(sub_bands, g0, g1):
    current_image = sub_bands[-1]
    
    for i in reversed(range(len(sub_bands) - 1)):
        current_image = apply_filter(current_image, g0) + apply_filter(sub_bands[i], g1)
    
    return current_image

def calculate_psnr(original, reconstructed):
    mse = np.mean((original - reconstructed) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * np.log10(255 ** 2 / mse)

def calculate_compression_ratio(original_size, retained_size):
    return original_size / retained_size

def main():
    filters = {
        '4-tap': {
            'h0': [-0.1294, 0.2241, 0.8365, 0.4830],
            'h1': [-0.4830, 0.8365, -0.2241, -0.1294],
            'g0': [0.4830, 0.8365, 0.2241, -0.1294],
            'g1': [-0.1294, -0.2241, 0.8365, -0.4830]
        },
        '6-tap': {
            'h0': [0.0352, -0.0854, -0.1350, 0.4599, 0.8069, 0.3327],
            'h1': [-0.3327, 0.8069, -0.4599, -0.1350, 0.0854, 0.0352],
            'g0': [0.3327, 0.8069, 0.4599, -0.1350, -0.0854, 0.0352],
            'g1': [0.0352, 0.0854, -0.4599, 0.1350, 0.8069, -0.3327]
        },
        '8-tap': {
            'h0': [-0.0106, 0.0329, 0.0308, -0.1870, -0.0280, 0.6309, 0.7148, 0.2304],
            'h1': [-0.2304, 0.7148, -0.6309, -0.0280, 0.1870, 0.0308, -0.0329, -0.0106],
            'g0': [0.2304, 0.7148, 0.6309, -0.0280, -0.1870, 0.0308, 0.0329, -0.0106],
            'g1': [-0.0106, -0.0329, 0.1870, -0.6309, 0.7148, -0.2304, 0.0308, 0.0106]
        }
    }

    image_path = 'Lenna.png'
    image = Image.open(image_path).convert('L')
    image = np.array(image)
    original_size = image.size

    for name, f in filters.items():
        if pr_condition(f['h0'], f['h1'], f['g0'], f['g1']):
            print(f"{name} PR condition is satisfied.")
        else:
            print(f"{name} PR condition is NOT satisfied.")
       
        plot_frequency_response(f['h0'], len(f['h0']), f"{name} Filter h0")

        sub_bands = decompose_image(image, f['h0'], f['h1'], levels=13)

        retained_sub_bands = sorted(sub_bands, key=lambda sb: np.sum(np.abs(sb)**2), reverse=True)[:5]

        reconstructed_image = reconstruct_image(retained_sub_bands, f['g0'], f['g1'])

        psnr_value = calculate_psnr(image, reconstructed_image)
        print(f"{name} PSNR: {psnr_value:.2f} dB")

        retained_size = sum(sb.size for sb in retained_sub_bands)
        compression_ratio = calculate_compression_ratio(original_size, retained_size)
        print(f"{name} Compression Ratio: {compression_ratio:.2f}")

        reconstructed_image = Image.fromarray(reconstructed_image).convert('L')
        reconstructed_image.save(f'reconstructed_image_{name}.png')
        reconstructed_image.show()

if __name__ == "__main__":
    main()

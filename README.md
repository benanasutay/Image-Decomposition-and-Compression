# Image Compression and Reconstruction using Wavelet Filters

This project demonstrates the process of image decomposition and reconstruction using wavelet filters. Specifically, it applies various filters (4-tap, 6-tap, and 8-tap) to decompose an image into sub-bands, retains the most significant sub-bands, and reconstructs the image from these retained sub-bands. The effectiveness of each filter is evaluated using the Peak Signal-to-Noise Ratio (PSNR) and compression ratio metrics.

## Overview

The script performs the following operations:

1. **Image Decomposition**: Decomposes an image into sub-bands using different wavelet filters (`h0`, `h1`) by applying convolution along both dimensions of the image.
   
2. **Wavelet Filter Types**: The project uses three different wavelet filter lengths (4-tap, 6-tap, and 8-tap) for decomposition.
   
3. **Sub-band Retention**: After decomposing the image, the most significant sub-bands are retained based on their energy (sum of squared values).
   
4. **Image Reconstruction**: The image is reconstructed by applying the inverse filters (`g0`, `g1`) to the retained sub-bands.

5. **Performance Evaluation**: The Peak Signal-to-Noise Ratio (PSNR) and compression ratio are computed for each filter to evaluate the quality of the reconstructed image.

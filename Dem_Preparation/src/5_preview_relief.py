#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread("../Data/DEM_prep/white_relief.png")
plt.figure(figsize=(12, 8))
plt.imshow(img)
plt.title("Arabian Peninsula - White Smooth Relief (90 m)")
plt.axis("off")
plt.show()

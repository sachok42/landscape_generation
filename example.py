import png

# Create from array
image_2d = [[255, 0, 0],    # Red pixel
            [0, 255, 0],    # Green pixel
            [0, 0, 255]]    # Blue pixel

# Save as PNG
png.from_array(image_2d, 'RGB').save("output.png")

# Write with more control
writer = png.Writer(width=3, height=3, bitdepth=8, greyscale=True)
with open('output.png', 'wb') as f:
    writer.write(f, image_2d)
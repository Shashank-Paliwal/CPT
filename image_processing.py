from PIL import Image
import numpy as np

def encode_message(image, message):
    # Convert the image to a NumPy array for manipulation
    img_array = np.array(image)

    # Flatten the image array to a 1D array
    flat_array = img_array.flatten()

    # Convert the message to a binary string
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Ensure the image can hide the entire message
    if len(binary_message) > len(flat_array):
        raise ValueError("Message is too long to be encoded in the given image.")

    # Replace the least significant bits with message bits
    for i in range(len(binary_message)):
        flat_array[i] = (flat_array[i] & 0b11111110) | int(binary_message[i])

    # Reshape the array to the original image shape
    encoded_array = flat_array.reshape(img_array.shape)

    # Return the encoded image as a Pillow Image object
    return Image.fromarray(encoded_array.astype(np.uint8))

def decode_message(image):
    # Convert the image to a NumPy array for manipulation
    img_array = np.array(image)

    # Flatten the image array to a 1D array
    flat_array = img_array.flatten()

    # Extract the least significant bits as message bits
    binary_message = ''.join(str(pixel & 1) for pixel in flat_array[:8])

    # Convert the binary message to ASCII characters
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return decoded_message

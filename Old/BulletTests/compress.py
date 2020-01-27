"""
Used to test various compression techniques to figure out which one is the best
Tests: 1) Compressed image length, 2) Compression time
Compression calculated on cameraimg.png (a 3632x5456 RGB image)
Compression time is calculated as the time taken to compress the image 50 times
"""

import cv2
import pickle
import time
import numpy as np

display_dim = (1920 // 2, 1080 // 2)

# Compression length -> 59448740
def pickle_compress(img):
    return pickle.dumps(img)

def pickle_decompress(data):
    img = pickle.loads(data)
    return img

# Compression length ->              4457041, 7838818
# PNG lossless compression length -> 59548600, 19903366
def cv2encode(img):
    _, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return pickle.dumps(encoded)

def cv2decode(data):
    img = pickle_decompress(data)
    img = cv2.imdecode(img, 1)
    return img

def compare(img1, img2):
    diff = cv2.subtract(img1, img2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    total = np.sum(diff)
    print(total)
    print(total / (255 * img1.shape[0] * img1.shape[1]))
#    _, diff = cv2.threshold(diff, 1, 255, cv2.THRESH_BINARY)
#    cv2.imshow("img", cv2.resize(diff, display_dim))
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#    print(xor.shape)
#    blank = np.zeros(img1.shape)
#    diffCoords = np.where((img1 != img2).all(axis=2))
#    print(len(diffCoords[0]))


img = cv2.imread("cameraimg.png")
print(img.shape)
compression_method = cv2encode
decompression_method = cv2decode

start_time = time.time()
for i in range(1):
    data = compression_method(img)
    print(type(data))
    img = decompression_method(data)

print("Compression Length:", len(data))
print("Compression Time:", time.time() - start_time)
print(img.shape)
cv2.imwrite("decoded.png", img)


img1 = cv2.imread("cameraimg.png")
img2 = cv2.imread("decoded.png")
compare(img1, img2)
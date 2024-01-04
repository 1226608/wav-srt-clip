import numpy as np
import imageio
from scipy.spatial.distance import cdist
from concurrent.futures import ThreadPoolExecutor

reader = imageio.get_reader('123.mp4')
fps = reader.get_meta_data()['fps']
writer = imageio.get_writer('output_video.mp4', fps=fps)
colors = np.array([[0, 0, 0],[255, 255, 255],[255, 0, 0],[0, 255, 0],[0, 0, 255],[255, 255, 0],[128, 0, 128],[192, 192, 192],], dtype=np.uint8)

num_frames = reader.get_length()
frame_shape = reader.get_data(0).shape

def process_frame(frame):
    expanded_colors = colors[:, np.newaxis, np.newaxis, :]
    distances = np.sum((frame - expanded_colors) ** 2, axis=3)
    indices = np.argmin(distances, axis=0)
    compressed_frame = colors[indices]
    return compressed_frame

with ThreadPoolExecutor() as executor:
    for i, frame in enumerate(reader):
        print(f'Processing frame {i+1}/{num_frames}')
        compressed_frame = executor.submit(process_frame, frame).result()
        writer.append_data(compressed_frame)
writer.close()
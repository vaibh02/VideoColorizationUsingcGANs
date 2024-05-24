import streamlit as st
import torch
from deoldify._device import _Device
from deoldify.visualize import get_image_colorizer, get_video_colorizer
from pathlib import Path
import urllib.request

import os

# Create the dummy directory if it doesn't exist
os.makedirs('dummy', exist_ok=True)


# Pretrained weights URL
weights_url = 'https://data.deepai.org/deoldify/ColorizeVideo_gen.pth'
weights_path = './models/ColorizeVideo_gen.pth'  # Ensure this is the correct file path

# Download weights if not present
if not Path(weights_path).exists():
    print("Downloading weights...")
    urllib.request.urlretrieve(weights_url, weights_path)
    print("Weights downloaded.")

# Set device to GPU if available
torch.backends.cudnn.benchmark = True
_Device()

# Load the colorizer models
image_colorizer = get_image_colorizer()
# image_colorizer.gen_learner.load(weights_path)

video_colorizer = get_video_colorizer()
# video_colorizer.gen_learner.load(weights_path)

def save_uploadedfile(uploadedfile, directory):
    if uploadedfile.type.startswith('video'):
        directory = 'video/source/uploads'
    else:
        directory = 'uploads'

    os.makedirs(directory, exist_ok=True)
    path = Path(directory) / uploadedfile.name
    with open(path, 'wb') as f:
        f.write(uploadedfile.getbuffer())
    return path

st.title('Black and White to Color with DeOldify')
st.write("Upload a black and white image or video to colorize.")

# uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "mp4"])

# if uploaded_file is not None:
#     file_type = uploaded_file.type.split('/')[0]
#     saved_file_path = save_uploadedfile(uploaded_file, 'uploads')

#     if file_type == 'image':
#         st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
#         st.write("Colorizing...")
#         with st.spinner('Colorizing...'):
#             colorized_image = image_colorizer.get_transformed_image(str(saved_file_path), render_factor=35, post_process=True)
#             colorized_image_path = Path('outputs') / f'colorized_{uploaded_file.name}'
#             colorized_image.save(colorized_image_path)
#             st.image(colorized_image, caption='Colorized Image', use_column_width=True)
#             with open(colorized_image_path, 'rb') as f:
#                 st.download_button('Download Colorized Image', data=f, file_name=colorized_image_path.name)
            
#     elif file_type == 'video':
#         st.video(uploaded_file)
#         st.write("Colorizing...")
#         with st.spinner('Colorizing...'):
#             colorized_video_path = video_colorizer.colorize_from_file_name(str(saved_file_path), render_factor=21)
#             st.video(str(colorized_video_path))
#             with open(colorized_video_path, 'rb') as f:
#                 st.download_button('Download Colorized Video', data=f, file_name=colorized_video_path.name)


uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "mp4"])

if uploaded_file is not None:
    file_type = uploaded_file.type.split('/')[0]
    saved_file_path = save_uploadedfile(uploaded_file, 'uploads')

    # Print the saved file path
    print("Saved file path:", saved_file_path)

    if file_type == 'image':
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.write("Colorizing...")
        with st.spinner('Colorizing...'):
            colorized_image = image_colorizer.get_transformed_image(str(saved_file_path), render_factor=35, post_process=True)
            colorized_image_path = Path('outputs') / f'colorized_{uploaded_file.name}'
            colorized_image.save(colorized_image_path)
            st.image(colorized_image, caption='Colorized Image', use_column_width=True)
            with open(colorized_image_path, 'rb') as f:
                st.download_button('Download Colorized Image', data=f, file_name=colorized_image_path.name)
            
    elif file_type == 'video':
        st.video(uploaded_file)
        st.write("Colorizing...")
        with st.spinner('Colorizing...'):
            print(str(saved_file_path))
            st.write(str(saved_file_path))
            colorized_video_path = video_colorizer.colorize_from_file_name( str(saved_file_path), render_factor=21)
            st.video(str(colorized_video_path))
            with open(colorized_video_path, 'rb') as f:
                st.download_button('Download Colorized Video', data=f, file_name=colorized_video_path.name)

# C:\Users\vaibh\OneDrive\Desktop\Final Year Project\temp\uploads\vaibhav.mp4
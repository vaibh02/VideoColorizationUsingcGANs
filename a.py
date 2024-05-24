import torch
from pathlib import Path
import urllib.request
import streamlit as st
from deoldify._device import _Device,DeviceId
from deoldify.visualize import get_image_colorizer, get_video_colorizer
import pathlib
import time


weights_dir = Path('./weights')
weights_dir.mkdir(parents=True, exist_ok=True)

# URLs for pretrained weights
weights_url = 'https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth'

weights_path = weights_dir / 'ColorizeArtistic_gen.pth'

if not weights_path.exists():
    print("Downloading weights...")
    urllib.request.urlretrieve(weights_url, weights_path)
    print("Weights downloaded.")




# Use GPU if available
torch.backends.cudnn.benchmark = True

    
_Device()
# Load the pretrained model
image_colorizer = get_image_colorizer(artistic=True, pretrain_path=weights_path)
video_colorizer = get_video_colorizer(artistic=True, pretrain_path=weights_path)

def save_uploadedfile(uploadedfile, directory):
    path = pathlib.Path(directory) / uploadedfile.name
    with open(path, 'wb') as f:
        f.write(uploadedfile.getbuffer())
    return path

st.title('Black and White to Color with DeOldify')

st.write("Upload a black and white image or video to colorize.")

uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "mp4"])

if uploaded_file is not None:
    file_type = uploaded_file.type.split('/')[0]
    saved_file_path = save_uploadedfile(uploaded_file, 'uploads')

    if file_type == 'image':
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.write("Colorizing...")
        with st.spinner('Colorizing...'):
            colorized_image = image_colorizer.get_transformed_image(saved_file_path, render_factor=35, post_process=True)
            colorized_image.save(f'output/{uploaded_file.name}')
            st.image(colorized_image, caption='Colorized Image', use_column_width=True)
            st.download_button('Download Colorized Image', data=open(f'output/{uploaded_file.name}', 'rb'), file_name=f'colorized_{uploaded_file.name}')
            
    elif file_type == 'video':
        st.video(uploaded_file)
        st.write("Colorizing...")
        with st.spinner('Colorizing...'):
            colorized_video_path = video_colorizer.colorize_from_file_name(saved_file_path, render_factor=21)
            st.video(colorized_video_path)
            st.download_button('Download Colorized Video', data=open(colorized_video_path, 'rb'), file_name=f'colorized_{uploaded_file.name}')



from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import sys
import time
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import requests
from io import BytesIO

######################################
st.set_option('deprecation.showfileUploaderEncoding', False)
st.beta_set_page_config(
    page_title="Prédiction de la classe d'un iris",
    initial_sidebar_state="expanded",
    )
########################################

# <snippet_vars>
# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# </snippet_vars>

# <snippet_client>
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
# </snippet_client>

def objects_detection(choice):
    objects = []
    fig,ax = plt.subplots(1)
    if choice == 0:
        image = st.file_uploader("Choisir une image (JPG ou PNG)")
        if image is not None:
            # Call API with local image
            detect_objects_results = computervision_client.detect_objects_in_stream(image)
            im = np.array(Image.open(image), dtype=np.uint8)
            # Display the image
            ax.imshow(im)
         
    if choice == 1:
        st.write("L'URL doit se terminer par (JPG ou PNG)")
        # Get URL image with different objects
        image_url = st.text_input("Collez votre URL ICI")
        if len(image_url) > 0:       
            image = requests.get(image_url)
            image = Image.open(BytesIO(image.content))           
            # Call API with URL
            detect_objects_results = computervision_client.detect_objects(image_url)      
            ax.imshow(image)

    # Print results of detection with bounding boxes           
    if st.button('Lancer la détection'):
        st.write("Résultat de la détection")
        if len(detect_objects_results.objects) == 0:
            st.write("No objects detected.")
        else:
            for data in detect_objects_results.objects:
                # Create a Rectangle patch
                rect = patches.Rectangle((data.rectangle.x, data.rectangle.y), data.rectangle.w, data.rectangle.h,linewidth=1,edgecolor='r',facecolor='none')
                objects.append(data.object_property)           
                # Add the patch to the Axes
                ax.add_patch(rect)
        plt.xticks([])
        plt.yticks([])
        st.pyplot(fig)
        st.write('Natures des éléments détectés :', ', '.join(objects))

def main():
    st.sidebar.header("Navigation")
    st.title("Détection d'objects dans une image")
    menu = st.sidebar.selectbox("Source de données :",
                                    ("Image sur mon PC", "Image en ligne (URL)")
                                )
    # Get local image with different objects in it
    if menu == "Image sur mon PC":
        objects_detection(0)          
    if menu == "Image en ligne (URL)":
        objects_detection(1)       

if __name__ == "__main__":
	main()
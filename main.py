import streamlit as st
import cv2
import numpy as np
from PIL import Image

def RGB_image(img):
    return cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    

def grayscale_image(img):
    return cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)


def threshold_image(img , thresh_value):
    retval , img_thresh = cv2.threshold(img , thresh_value, 255 ,cv2.THRESH_BINARY)
    return img_thresh



def brightness_contrast(image, brightness, contrast):
    alpha = (contrast + 100) / 100.0
    beta = brightness
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image



## Function to draw line on image
def draw_line(image , x1 , y1 , x2 , y2 , thickness , color):

    cv2.line(image, (x1 , y1) , (x2 , y2) , color = color, thickness = thickness , lineType = cv2.LINE_AA)
    return(image[:,:,::-1]) 



## Function to draw circle on image
def draw_circle(image , x , y , rad , color , thickness):

    cv2.circle(image, (x , y), radius = rad , color = color, thickness = thickness , lineType = cv2.LINE_AA)
    return(image[:,:,::-1])



## Function to draw rectangle on image
def draw_rectangle(image , x1 , y1 , x2 , y2 , thickness , color):

    cv2.rectangle(image, (x1 , y1) , (x2 , y2) , color = color , thickness = thickness , lineType = cv2.LINE_AA)
    return(image[:,:,::-1]) 



## Function to write text on image
def write_text(image ,text , x, y , thickness , color,  font):

    cv2.putText(image, text  , (x , y) , color = color ,fontFace = cv2.FONT_HERSHEY_PLAIN , fontScale = font , thickness = thickness , lineType = cv2.LINE_AA)
    return(image[:,:,::-1])  



def main():

    st.markdown("<h2 style='text-align: center; color: cyan; font-size : 50px'>Image Processing with OpenCV</h2>" , unsafe_allow_html=True)

    file = st.sidebar.file_uploader("Choose an image file" , type = ["jpg" , "png" , "jpeg"])
    
    if file is not None:
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, 1)

        scale_percent = 80 # percent of original size
        width = int(original_image.shape[1] * scale_percent / 100)
        height = int(original_image.shape[0] * scale_percent / 100)
        dim = (width, height)   
        original_image = cv2.resize(original_image , dim, interpolation= cv2.INTER_AREA)

        st.subheader("Original Image")
        st.image(RGB_image(original_image), use_column_width=True)

        option = 1
        option = st.sidebar.selectbox("Select any option", options = ["RGB" , "Grayscale" , "Binary" , "Brightness/Contrast" , "Annotation"])

        if option == "RGB":
            st.subheader("RGB Image")
            st.image(RGB_image(original_image) , use_column_width= True)


        elif option == "Grayscale":
            st.subheader("Grayscale Image")
            st.image(grayscale_image(original_image) , use_column_width= True)


        elif option == "Binary":
            thresh = st.sidebar.slider("Threshold",min_value = 0  , max_value= 255 , value = 125 , step = 1)
            st.subheader("Binary Image")
            st.image(threshold_image(original_image , thresh) , use_column_width= True)


        elif option == "Brightness/Contrast":
            brightness = st.sidebar.slider("Brightness", min_value = -100, max_value =  100, value = 0 , step = 2)
            contrast = st.sidebar.slider("Contrast",  min_value = -100,max_value =  100, value = 0 , step = 2)
            st.subheader("Brightness/Contrast Image")
            st.image(brightness_contrast(original_image, brightness , contrast) , use_column_width= True)


        elif option == "Annotation":
            st.subheader("Annotation")
            choice = st.sidebar.selectbox("Choose shape" , options=["Line" , "Circle" , "Rectangle", "Text"])
            color = st.sidebar.color_picker("Select any color" , "#00FFAA")
            thickness = st.sidebar.slider("Thickness" , min_value = 1 , max_value = 12 , step = 1)


            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

            color = hex_to_rgb(color)

            if choice in ["Line","Rectangle"]:
                x1 = st.sidebar.number_input("X1" , value = 10)
                y1 = st.sidebar.number_input("Y1" , value = 10)
                x2 = st.sidebar.number_input("X2" , value = 50)
                y2 = st.sidebar.number_input("Y2" , value = 50)
                if choice == "Line":
                    st.image(draw_line(original_image , x1 , y1 , x2 , y2 , thickness , color) , use_column_width= True)
                else:
                    st.image(draw_rectangle(original_image , x1 , y1 , x2 , y2 , thickness , color))
                

            if choice in "Circle":
                x = st.sidebar.number_input("X1" , value = 50)
                y = st.sidebar.number_input("Y1" , value = 50)
                radius = st.sidebar.number_input("Radius" ,value = 50)
                st.image(draw_circle(original_image , x , y , radius , color , thickness) , use_column_width= True)

            if choice in "Text":
                x = st.sidebar.number_input("X", value=150)
                y = st.sidebar.number_input("Y", value=150)
                text = st.sidebar.text_input("Enter text", value="Hello")
                font = st.sidebar.number_input("Enter font size", value = 10)
                st.image(write_text(original_image ,text , x, y , thickness , color , font))
            

if __name__ == "__main__":
    main()
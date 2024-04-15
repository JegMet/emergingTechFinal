from flask import Flask, render_template, request

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests
import io
from forms.forms import UploadImageForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sdadjksahndkjlasjd;jsakl;djskdlas'

# Model info from https://huggingface.co/google/vit-base-patch16-224


@app.route("/", methods=['GET', 'POST'])
def index():
    form = UploadImageForm()
    if request.method == 'POST':
        if(form.validate()):
            #form validates so do work
            # Get the file from the form
            file = form.picture.data

            # Read the file
            image = Image.open(file)


            answer = imageAnalysis(image)
            return render_template('index.html', form=form, answer=answer)
        else:
            answer = "Form didnt validate make sure you use jpg"
            return render_template('index.html', form=form, answer=answer)
    else:
        return render_template('index.html', form=form)
    

def imageAnalysis(image):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    # conditional image captioning
    text = "a photography of"
    inputs = processor(image, text, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))

    # unconditional image captioning
    inputs = processor(image, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))
    return processor.decode(out[0], skip_special_tokens=True)

    
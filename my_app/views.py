from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
import os
from .forms import UploadForm
from .models import Image
from PIL import Image as im
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
global model
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            i = Image.objects.latest('id')
            print(i.img.url)
            return render(request, 'upload.html', {'form' : form,'imgurl':i.img.url,'isup':'1'})

    else:
        form = UploadForm()
        return render(request, 'upload.html', {'form' : form})

def predict(request):
    model = load_model(os.path.join(settings.BASE_DIR,'model.h5'))
    if request.POST:
        imageobj = Image.objects.latest('id')
        
        img_path=settings.BASE_DIR+imageobj.img.url
        print(img_path.replace('\\','/'))
        img = image.load_img(img_path.replace('\\','/'), target_size=(224, 224))

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
       
        a =model.predict(x)
        a=a[0]
        a=[round(x,6) for x in a]


        print(x.shape)









        return render(request, 'upload.html', {'isup':'1','imgurl':imageobj.img.url,'r':a})
    else:
        return HttpResponse("Error")
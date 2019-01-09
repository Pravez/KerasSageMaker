import sagemaker
from sagemaker.tensorflow import TensorFlowPredictor
import numpy as np
from tensorflow.python.keras.preprocessing.image import load_img

remove_endpoint = False
endpoint_name = "[YOUR ENDPOINT]"
predictor = TensorFlowPredictor(endpoint_name)

cat_image = load_img("./tmp/PetImages/Cat/2282.jpg", target_size=(128, 128))
cat_image_array = np.array(cat_image).reshape((1, 128, 128, 3))

print(predictor.predict({ "inputs_input": cat_image_array}))

if remove_endpoint:
    sagemaker.Session().delete_endpoint(predictor.endpoint)

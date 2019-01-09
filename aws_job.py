import os
import sagemaker
import numpy as np
from sagemaker.tensorflow import TensorFlow
from tensorflow.python.keras.preprocessing.image import load_img

ON_SAGEMAKER_NOTEBOOK = False

sagemaker_session = sagemaker.Session()
if ON_SAGEMAKER_NOTEBOOK:
    role = sagemaker.get_execution_role()
else:
    role = "[YOUR ROLE]"


bucket = "cats-n-dogs"
key = "data"
key_output = "output"                   # Path from the bucket's root to the dataset
train_instance_type='ml.p2.xlarge'      # The type of EC2 instance which will be used for training
deploy_instance_type='ml.p2.xlarge'     # The type of EC2 instance which will be used for deployment
hyperparameters={
    "learning_rate": 1e-4,
    "decay": 1e-6
}

train_input_path = "s3://{}/{}/train/".format(bucket, key)
validation_input_path = "s3://{}/{}/validation/".format(bucket, key)

estimator = TensorFlow(
  entry_point=os.path.join(os.path.dirname(__file__), "cats_n_dogs.py"),             # Your entry script
  role=role,
  framework_version="1.12.0",               # TensorFlow's version
  hyperparameters=hyperparameters,
  training_steps=1000,
  evaluation_steps=100,
  train_instance_count=1,                   # "The number of GPUs instances to use"
  train_instance_type=train_instance_type,
)

print("Training ...")
estimator.fit({'training': train_input_path, 'eval': validation_input_path})

print("Deploying ...")
predictor = estimator.deploy(initial_instance_count=1, instance_type=deploy_instance_type)

print("Predictor endpoint name : %s" % predictor.endpoint)

print("Testing endpoint ...")
cat_image = load_img("./tmp/PetImages/Cat/2282.jpg", target_size=(128, 128))
cat_image_array = np.array(cat_image).reshape((1, 128, 128, 3))

print(predictor.predict({'inputs_input': cat_image_array}))

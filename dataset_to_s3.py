import boto3
import os
import zipfile
from PIL import Image
from botocore.exceptions import ClientError

bucket_name = 'cats-n-dogs'

s3 = boto3.client('s3')
try:
    print("Checking bucket ...")
    s3.head_bucket(Bucket=bucket_name)
except ClientError as e:
    print("Bucket not existing, creating it ...")
    s3.create_bucket(Bucket=bucket_name, ACL="private", CreateBucketConfiguration={'LocationConstraint': 'EU'})

zip_dataset = "kagglecatsanddogs_3367a.zip"
tmp_dest = os.path.join(os.path.dirname(__file__), "tmp")
data_dir = os.path.join(os.path.dirname(__file__), "cats_n_dogs")

if not os.path.exists(tmp_dest):
    os.mkdir(tmp_dest)

if len(os.listdir(tmp_dest)) <= 0:
    print("Unzipping archive ...")
    with zipfile.ZipFile(zip_dataset, 'r') as zip_ref:
        zip_ref.extractall(tmp_dest)

# The archive contains a main folder named "PetImages" followed by two folders "Cat" and "Dog"
# We will take only ~ 1000 images for each class to stay light.

dog_dir = tmp_dest + "/PetImages/Dog"
cat_dir = tmp_dest + "/PetImages/Cat"

train_dir = data_dir + "/train/"
validation_dir = data_dir + "/validation/"

print("Checking directories ...")
for dir in [data_dir, train_dir, validation_dir]:
    if not os.path.exists(dir):
        os.mkdir(dir)


def move_and_check_files(origin, dest_train, dest_valid, quantity_train=1000, quantity_valid=200):
    moved = 0
    for file in os.listdir(origin):
        try:
            # Before moving the file we check if the image is readable
            im = Image.open(os.path.join(origin, file))
            im.verify()
            os.rename(
                os.path.join(origin, file),
                os.path.join(dest_train if moved < quantity_train else dest_valid, file)
            )
            moved += 1
        except Exception as e:
            print("Bad image : %s" % file)

        if moved >= quantity_train + quantity_valid:
            break

print("Organizing and checking files ...")
for category in [(cat_dir, 'cat'), (dog_dir, 'dog')]:
    train = train_dir + category[1]
    valid = validation_dir + category[1]
    os.mkdir(train)
    os.mkdir(valid)
    move_and_check_files(category[0], train, valid)

print("Done !")

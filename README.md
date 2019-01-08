# KerasSageMaker
Support repository for medium article "Keras in the cloud with Amazon SageMaker

- `cats_n_dogs.py`: the entry script which contains the 4 main functions for SageMaker.
- `dataset_to_t3.py`: the script to import prepare and send the dataset to Amazon S3.
- `aws_job.py`: the job to send work to SageMaker and try the service.

The files should be executed in the following order : `dataset_to_s3.py` and `aws_job.py`.
You can find required python libraries to install with `pip` under `requirements.txt`.

Thank you for reading !

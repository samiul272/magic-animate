import os
import subprocess
import tempfile
from pathlib import Path

import fastapi.staticfiles
import firebase_admin
import modal
import requests
from firebase_admin import credentials, storage
from modal import Function
from modal import web_endpoint

stub = modal.Stub("single-view-impersonator")

dockerfile_image = modal.Image.from_dockerfile("Dockerfile")


def upload_file_to_firebase(file_path, destination_path):
    """
    Uploads a file to Firebase Storage and returns the downloadable URL.

    :param file_path: str, Local path to the file to be uploaded
    :param destination_path: str, Path in Firebase Storage where the file should be uploaded
    :return: str, Downloadable URL
    """
    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    # Make the file publicly accessible
    blob.make_public()

    # Get the downloadable URL
    download_url = blob.public_url

    return download_url


def download_file_from_url(url, local_path):
    """
    Downloads a file from the given URL and saves it to the specified local path.

    :param url: str, The URL of the file to download
    :param local_path: str, The local path where the file should be saved
    """

    # Send a HTTP request to the URL of the file, stream=True ensures that the file is downloaded efficiently
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a binary file in write mode
        with open(local_path, 'wb') as file:
            # Write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print('File downloaded successfully')
    else:
        print('Failed to download the file')


@stub.function(
    gpu="T4",
    image=dockerfile_image,
    secret=modal.Secret.from_name("firebase_secret"),
    timeout=3600,
)
@web_endpoint()
def predict(src_url: str,
            ref_url: str,
            steps: str
            ):
    """Run a single prediction on the model"""

    command = ["git", "pull", "--rebase"]
    #
    # # Set the working directory
    working_directory = "/magic-animate"

    cred = eval(os.environ["firebase_json"])

    cred = credentials.Certificate(cred)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'twerkai.appspot.com'
    })

    src_name = next(tempfile._get_candidate_names())
    ref_name = next(tempfile._get_candidate_names())
    src_path = f'{src_name}.PNG'
    ref_path = f'{ref_name}.MP4'
    subprocess.run(command, cwd=working_directory)
    command = ['python vid2densepose/main.py -i input/applications/akun1.mp4 -o input/applications/output_video.mp4']
    subprocess.run(command, cwd=working_directory)
    print(f"done {src_url}, {ref_url}, {steps}")
    return f"done {src_url}, {ref_url}, {steps}"


# @stub.local_entrypoint()
# def main():
#     cred = eval(os.environ["firebase_json"])
#     cred = credentials.Certificate(cred)
#
#     # Initialize the app with the credentials
#     firebase_admin.initialize_app(cred, {
#         'storageBucket': 'twerkai.appspot.com'
#     })
#     src_image = upload_file_to_firebase('./iPERCore/assets/samples/sources/donald_trump_2/00000.PNG',
#                                         'assets/samples/sources/donald_trump_2/00000.PNG')
#     ref_vid = upload_file_to_firebase('./iPERCore/assets/samples/references/akun_1.mp4',
#                                       'assets/samples/references/akun_1.mp4')
#     print(src_image, ref_vid, )
#     p = predict(src_image,
#                      ref_vid, 256)
#
#     print(p)
# # https://storage.googleapis.com/twerkai.appspot.com/assets/samples/sources/donald_trump_2/00000.PNG https://storage.googleapis.com/twerkai.appspot.com/assets/samples/references/akun_1.mp4
# # https://vrl-inc--single-view-impersonator-predict-samiul272-dev.modal.run
# # curl --location "https://vrl-inc--single-view-impersonator-predict-samiul272-dev.modal.run?image_size=512&src_url=https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Ftwerkai.appspot.com%2Fo%2Fusers%252FtUZIbt0M9MSl5jDuSXqFxlqAGOG2%252Fimages%252F00000.PNG%3Falt%3Dmedia%26token%3D8f406a68-b610-4d97-87cc-58c7a63fd264&ref_url=https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Ftwerkai.appspot.com%2Fo%2Fdances%252F001_18_2.mp4%3Falt%3Dmedia%26token%3D1a28b73a-e254-4076-89a7-6472f7557b23"
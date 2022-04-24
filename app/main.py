from typing import Optional

from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import os, subprocess
import shutil
import glob
import codecs
import pdftotext
import starlette

import boto3

import io
import numpy
import pickle

'''
accepts a pdf byte file and uuid string
convert pdf to text, saves it to s3 bucket

'''

print('loading 😊 pdftotext api')

# initializing environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region_name = os.getenv('AWS_REGION_NAME')


# connect with the s3 resource to dump embeddings and text files
s3 = boto3.resource("s3", aws_access_key_id=aws_access_key_id , aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)

# init app
app = FastAPI()

# add cors origins rules 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes defined here
@app.post("/convert-pdf")
def convert_pdf(hash: str = Form(...), file: UploadFile = Form(...)):
    print('⚡ request recieved ⚡: hash: ',hash)

    # extract text from file
    text = file.file._file
    pdf = pdftotext.PDF(text)
    content="\n\n".join(pdf)

    # upload to s3
    s3.Object('readneedobjects', 'v2/'+hash+'/file.txt').put(Body=content)

    return {"file_id": hash, "upload": True}
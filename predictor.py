# this is an example for cortex release 0.21 and may not deploy correctly on other releases of cortex

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
and adds uuid to sqs queue for further processing

'''

class PythonPredictor:

    def __init__(self, config):

        print('loading 😊 pdftotext api')

        # initializing environment variables
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region_name = os.getenv('AWS_REGION_NAME')

        # connect with the s3 resource to dump embeddings and text files
        self.s3 = boto3.resource("s3", aws_access_key_id=self.aws_access_key_id , aws_secret_access_key=self.aws_secret_access_key)
        self.client = boto3.client('sqs',  aws_access_key_id=self.aws_access_key_id , aws_secret_access_key=self.aws_secret_access_key, region_name=self.aws_region_name)


        self.queues = self.client.list_queues(QueueNamePrefix='readneed_encode_jobs.fifo') # we filter to narrow down the list
        self.readneed_encode_jobs_url = self.queues['QueueUrls'][0]

        
    def predict(self, payload):
        

        print('⚡ request recieved ⚡')
        
         
        payload_pdf = payload.getlist('pdf-file')


        #filename = payload[0].filename

        # starlette.datastructures.UploadFile has file attribute to access a
        # SpooledTemporaryFile, which contains _file attribute, giving access to io.BytesIO

        text = payload_pdf[0].file._file
        print('text at _ file:', type(text))

        # io.BytesIO file converted to bytes by the read() method
        
        #bytes_text = text.read()
        #print('text at bytes_text:', type(bytes_text))
        
        #with open("tmp/test.pdf", "wb") as f:
            #f.write(bytes_text)


        #with open("tmp/test.pdf", "rb") as f:
            #print('parsing to pdf time: ', type(f))

        pdf = pdftotext.PDF(text)

        uuid = payload.getlist('uuid')[0]

        content="\n\n".join(pdf)
        self.s3.Object('readneedobjects', 'v2/'+uuid+'/text_content.txt').put(Body=content)
        

        enqueue_response = self.client.send_message(QueueUrl=self.readneed_encode_jobs_url, 
                                           MessageBody=uuid,
                                          MessageGroupId='readneed_jobs')

        # the response contains MD5 of the body, a message Id, MD5 of message attributes, and a sequence number (for FIFO queues)
        job_id=enqueue_response['MessageId']
      

        return job_id



'''
        # to create a new FIFO queue programatically
        self.client.create_queue(QueueName='readneed_encode_jobs.fifo', Attributes={
        'FifoQueue': 'true'
        })
'''
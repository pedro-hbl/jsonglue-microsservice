import sys
import time

import boto3
import json
import os


class InstanceService:

    def main(self):
        sqs_client = boto3.client('sqs')

        start = time.time()
        arguments = sys.argv

        response = sqs_client.receive_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-semantica-jsonglue',
            MaxNumberOfMessages=1,
        )

        message_response = json.loads(response['Messages'][0]['Body'])

        filenum = int(message_response['FilesPerPod']) + 1

        if message_response['podNumberSemantic'] == 1:
            fileRanges = message_response['rangesPod1']
        else:
            fileRanges = message_response['rangesPod2']

        filenameGlobal = []

        dir_path = r'/files/*.*'

        for path in os.scandir(dir_path):
            if path.is_file():
                filenameGlobal.append(path.name)

        startIndex = fileRanges[0]

        filename = []
        for file in range(fileRanges[1] - fileRanges[0]):
            filename.append(filenameGlobal[startIndex])
            startIndex += 1


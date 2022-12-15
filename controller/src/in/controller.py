from dataclasses import dataclass

import boto3
import json


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')

    # processos permitidos: half(2 instancias), quarter(4 instancias), full(1 instancia)

    quantidadeDePodsSemantico = 2
    quantidadeDePodsInstancia = 2
    quantidadeDePodsLinguistico = 2

    tamanhoMaquinaSemantica = 'm5.2xlarge'
    tamanhoMaquinaInstancia = 'c7g.2xlarge'
    tamanhoMaquinaLinguistica = 'm5.2xlarge'

    semantic_ranges = 0
    semantic_indexes = []

    filenum = 8
    filesPerPod = filenum / quantidadeDePodsInstancia

    message_body = {'FilesPerPod': filesPerPod, 'rangesPod1': [0, 4], 'rangesPod2': [4, 8]}
    # DISPARAR MENSAGENS COM METADADOS DE EXECUCAO

    for pods in range(quantidadeDePodsSemantico):
        semantic_indexes.append(tuple(filesPerPod, str(pods)))
        message_body['podNumberSemantic'] = pods + 1
        message_body_json = json.dumps(message_body)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-semantica-jsonglue',
            DelaySeconds=0,
            MessageAttributes={
                'Header': {
                    'DataType': 'String',
                    'StringValue': 'Pod: ' + str(pods)
                }
            },
            MessageBody=message_body_json
        )
        semantic_ranges += 1
        print(send_message['MessageId'])

    instance_ranges = 0
    instance_indexes = []
    for pods in range(quantidadeDePodsInstancia):
        instance_indexes.append(tuple(filesPerPod, str(pods)))
        message_body['podNumberInstance'] = pods + 1
        message_body_json = json.dumps(message_body)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-instancia-jsonglue',
            DelaySeconds=0,
            MessageAttributes={
                'Header': {
                    'DataType': 'String',
                    'StringValue': 'Pod: ' + str(pods)
                }
            },
            MessageBody=message_body_json
        )
        instance_ranges += 1
        print(send_message['MessageId'])

    linguistic_ranges = 0
    linguistic_indexes = []
    for pods in range(quantidadeDePodsLinguistico):
        linguistic_indexes.append(tuple(filesPerPod, str(pods)))
        message_body['podNumberLinguistic'] = pods + 1
        message_body_json = json.dumps(message_body)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-linguistica-jsonglue',
            DelaySeconds=0,
            MessageAttributes={
                'Header': {
                    'DataType': 'String',
                    'StringValue': 'Pod: ' + str(pods)
                }
            },
            MessageBody=message_body_json
        )
        linguistic_ranges += 1
        print(send_message['MessageId'])

    # ATÉ AQUI OK

    print('Mensagens de Metadado enviadas com Sucesso!')

    return {
        'statusCode': 200,
        'body': 'Processamento Inicial executado com sucesso'
    }

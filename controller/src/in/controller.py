import boto3

sqs_client = boto3.client('sqs')

ecs_client = boto3.client('ecs')


sqs_queue = sqs_client.get_queue_by_name(QueueName='InputQueueJSONGLUE')

#processos permitidos: half(2 instancias), quarter(4 instancias), full(1 instancia)

quantidadeDePodsSemantico = 2
quantidadeDePodsInstancia = 2
quantidadeDePodsLinguistico = 2

tamanhoMaquinaSemantica = 'm5.2xlarge'
tamanhoMaquinaInstancia = 'c7g.2xlarge'
tamanhoMaquinaLinguistica = 'm5.2xlarge'

semantic_ranges = 0
semantic_indexes = []
for pods in range(quantidadeDePodsSemantico):

    semantic_indexes.append(semantic_ranges)
    send_message = sqs_client.send_message(
        QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-semantica-jsonglue',
        DelaySeconds=0,
        MessageAttributes={
            'Header': {
                'DataType': 'String',
                'StringValue': 'Pod: ' + str(pods)
            }
        },
        MessageBody=semantic_indexes
    )
    semantic_ranges+=1
    print(send_message['MessageId'])


instance_ranges = 0
instance_indexes = []
for pods in range(quantidadeDePodsInstancia):
    instance_indexes.append(instance_ranges)
    send_message = sqs_client.send_message(
        QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-instancia-jsonglue',
        DelaySeconds=0,
        MessageAttributes={
            'Header': {
                'DataType': 'String',
                'StringValue': 'Pod: ' + str(pods)
            }
        },
        MessageBody=instance_indexes
    )
    instance_ranges+=1
    print(send_message['MessageId'])


linguistic_ranges = 0
linguistic_indexes = []
for pods in range(tamanhoMaquinaLinguistica):
    linguistic_indexes.append(linguistic_ranges)
    send_message = sqs_client.send_message(
        QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-linguistica-jsonglue',
        DelaySeconds=0,
        MessageAttributes={
            'Header': {
                'DataType': 'String',
                'StringValue': 'Pod: ' + str(pods)
            }
        },
        MessageBody=linguistic_indexes
    )
    linguistic_ranges+=1
    print(send_message['MessageId'])


#ATÉ AQUI OK



for i in range(quantidadeDePodsSemantico):
    inicia_tasks_semanticas = ecs_client.create_service(
    cluster= 'jsonGlueCluster',
    serviceName= 'semanticJSONGlueService',
    taskDefinition= 'semanticFamily',

    serviceRegistries=[
        {
            'registryArn': 'string',
            'port': 123,
            'containerName': 'string',
            'containerPort': 123
        },
    ],
    desiredCount= quantidadeDePodsSemantico,
    launchType='EC2',
    capacityProviderStrategy=[
        {
            'capacityProvider': 'string',
            'weight': 123,
            'base': 123
        },
    ],
    role='string',
    deploymentConfiguration={
        'deploymentCircuitBreaker': {
            'enable': False,
            'rollback': False
        },
        'maximumPercent': 100,
        'minimumHealthyPercent': 10
    },
    placementConstraints=[
        {
            'type': 'distinctInstance'|'memberOf',
            'expression': 'string'
        },
    ],
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'string',
            ],
            'securityGroups': [
                'string',
            ],
            'assignPublicIp': 'ENABLED'
        }
    },
    healthCheckGracePeriodSeconds=10,
    schedulingStrategy='REPLICA',
    enableExecuteCommand= True
)



#dado os metadados -> startar quantidade de tasks solicitadas pela mensagem e ranges de processamento de arquivo informados

for quantidade in 


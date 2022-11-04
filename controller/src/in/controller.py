import boto3

sqs_client = boto3.client('sqs')

ecs_client = boto3.client('ecs')


sqs_queue = sqs_client.get_queue_by_name(QueueName='InputQueueJSONGLUE')

metadado_mensagem = client.receive_message(
    QueueUrl=sqs_queue.get_queue_url(),
    AttributeNames=['All'],
    MessageAttributeNames=[
        'string',
    ],
    MaxNumberOfMessages=1
)

rangeSemantico = metadado_mensagem.message_attributes.get('rangeSemantico').get('StringValue')
rangeInstancia = metadado_mensagem.message_attributes.get('rangeInstancia').get('StringValue')
rangeLinguistico = metadado_mensagem.message_attributes.get('rangeLinguistico').get('StringValue')

quantidadeDePodsSemantico = metadado_mensagem.message_attributes.get('quantidadeDePodsSemantico').get('StringValue')
quantidadeDePodsInstancia = metadado_mensagem.message_attributes.get('quantidadeDePodsInstancia').get('StringValue')
quantidadeDePodsLinguistico = metadado_mensagem.message_attributes.get('quantidadeDePodsLinguistico').get('StringValue')

tamanhoMaquinaSemantica = metadado_mensagem.message_attributes.get('quantidadeDePodsSemantico').get('StringValue')
tamanhoMaquinaInstancia = metadado_mensagem.message_attributes.get('tamanhoMaquinaInstancia').get('StringValue')
tamanhoMaquinaLinguistica = metadado_mensagem.message_attributes.get('tamanhoMaquinaLinguistica').get('StringValue')

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


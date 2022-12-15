import sys
import time
import multiprocessing as mp
import boto3
import json
import os
import networkx as nx
from functools import partial

from controller.src.out.responseAdapter import printResults
from controller.src.utils import comp as cp
from controller.src.utils import data as dt
from controller.src.utils import grafo as gr
from controller.src.utils.normalizationModules import removeSpaces, createRandomJSON1, loadNamingStd, auxMultipro, \
    cleanString, formatName, formatTime


class InstanceService:
    def main(self):
        sqs_client = boto3.client('sqs')

        start = time.time()
        arguments = sys.argv

        response = sqs_client.receive_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-instancia-jsonglue',
            MaxNumberOfMessages=1,
        )

        message_response = json.loads(response['Messages'][0]['Body'])

        filenum = int(message_response['FilesPerPod']) + 1

        if message_response['podNumberInstance'] == 1:
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

        jstring = ""

        graphs_dict = {}  # holds the file name as key and graph as value,  the graph name will be the file name
        graphs_size = {}

        graphs_names = {}  # holds every name of every schema

        for x in range(0, filenum - 1):
            graphs_dict.update({filename[x]: nx.Graph()})
            graphs_size.update({filename[x]: 0})

        # MODULO DE NORMALIZACAO ( RODA EM TODOS OS PODS )

        node_number = 0
        for x in range(0, filenum - 1):
            node_number = 0
            try:
                with open(filename[x], "r") as f:
                    jstring = f.read()
                jstring = removeSpaces(jstring)
                final = gr.Pro(jstring, 0, 0, 0, graphs_dict.get(filename[x]))
                graphs_size.update({filename[x]: final[3]})
            except FileNotFoundError:  # Ja foi verificado, mas vale deixar aqui ainda
                print("Arquivo %s não encontrado." % filename[x])  # Ja criou o filename no dict

        # DEPRECADO TODOS ARQUIVOS ESTARAO NO S3
        # if '-r' in flags:
        #    createRandomJSON1(1000)
        #    createRandomJSON2(1000)
        #    createRandomJSON3(1000)
        #    sys.exit()

        std = loadNamingStd()

        controller_leitura_multiprocessada = True

        if controller_leitura_multiprocessada:
            cores = mp.cpu_count()
            files = len(filename)
            if files > cores:
                pool1 = mp.Pool(cores)
            else:
                pool1 = mp.Pool(files)

            print('Leitura multiprocessada iniciada.')

            for i in filename:
                x = partial(dt.applyData2Graph, graph=graphs_dict[i], nodes=graphs_size[i])
                pool1.apply_async(auxMultipro, args=(i, graphs_dict[i], graphs_size[i]), callback=x)

            pool1.close()
            pool1.join()

            print('Leitura multiprocessada encerrada.')

        else:
            print('Leitura sequencial iniciada.')
            for i in filename:
                print('Arquivo', i, 'iniciado.')
                a = dt.returnDataList(i, graphs_dict[i], graphs_size[i])
                if a == None:
                    dt.applyData2Graph(a, graphs_dict[i], graphs_size[i])
                else:
                    b = dt.returnAver(a)
                    c = dt.buildHist(b)
                    d = dt.normData(c)
                    dt.applyData2Graph(d, graphs_dict[i], graphs_size[i])
                print('Arquivo', i, 'encerrado.')
            print('Leitura sequencial encerrada')

        for i in filename:
            k = graphs_size[i]
            for j in range(0, k):
                graphs_dict[i].nodes[j]['orig'] = graphs_dict[i].nodes[j]['name']
                tmp = cleanString(graphs_dict[i].nodes[j]['name'])
                # graphs_dict[i].nodes[j]['name'] = cleanString(graphs_dict[i].nodes[j]['name'])
                names = tmp.split()
                for x in range(0, len(names)):
                    new = std.get(names[x])
                    if new == None:
                        continue
                    else:
                        names[x] = new
                graphs_dict[i].nodes[j]['name'] = ' '.join(names)

        full = []
        header = []
        comp = []

        if (filenum == 1):
            print("Não foi passado nenhum arquivo ou os arquivos não existem.")
        elif (filenum > 2):  # TODO verificar se Jaro-winkler e instance based inicia aqui
            print('\nComparação de schemas iniciada.')
            if controller_leitura_multiprocessada:
                pool = mp.Pool(mp.cpu_count())
                schemacomb = []
                for x in range(0, filenum - 1):
                    for y in range(x + 1, filenum - 1):
                        schemacomb.append((x, y))
                comp = [pool.apply_async(cp.compGraph, args=(
                    graphs_dict[filename[x]], graphs_dict[filename[y]], graphs_size[filename[x]],
                    graphs_size[filename[y]], x,
                    y)) for (x, y) in schemacomb]
                comp = [r.get() for r in comp]
                pool.close()
                pool.join()

                for i in comp:  # TODO reescrever usando formatName
                    file1 = filename[i[0][0]]
                    file2 = filename[i[0][1]]
                    a1 = file1.rfind('/', 0)
                    a2 = file2.rfind('/', 0)
                    if a1 == -1:
                        header.append(file1)
                    else:
                        header.append(file1[a1 + 1:len(file1)])
                    if a2 == -1:
                        header.append(file2)
                    else:
                        header.append(file2[a2 + 1:len(file2)])
                    header.append(i[1])
                    full.append(header)
                    header = []
            else:
                for x in range(0, filenum - 1):
                    for y in range(x + 1, filenum - 1):
                        header.append(formatName(filename[x]))
                        header.append(formatName(filename[y]))
                        comp = cp.compGraph(graphs_dict[filename[x]], graphs_dict[filename[y]],
                                            graphs_size[filename[x]],
                                            graphs_size[filename[y]], x, y)
                        header.append(comp[1])
                        full.append(header)
                        header = []
        else:
            print("Apenas um arquivo foi recebido")

        # print("Printando dados\n")
        # [print(i, end='\n\n') for i in dt.returnDataList(filename[0], graphs_dict[filename[0]], graphs_size[filename[0]])]

        end = time.time()

        printResults(full)
        if controller_leitura_multiprocessada:
            print("Time multiprocess : " + formatTime(end - start))
        else:
            print("Time sequential : " + formatTime(end - start))

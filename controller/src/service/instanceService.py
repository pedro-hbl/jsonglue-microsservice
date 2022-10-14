import sys
import boto3

class InstanceService:

    def main():
        start = time.time()
        arguments = sys.argv
        queueClient = boto3.sqs.client(region, queueName)
        Messages = queueClient.get()[Payload]
        flags = []
        arguments = sys.argv #arguments should now be obtained from sqs message(queue)

        for arg in arguments:
                if arg[0] == '-':
                    flags.append(arg)

        for f in flags:
                if f in arguments:
                    arguments.remove(f)

        filenum = len(arguments)#holds the number of files entered + 1
        filename = [] #filename is a list that holds the file names

        #if argv is a file, appends it to the filename list
        #if not decreases filenum variable
        for x in range(1, filenum):
            if(os.path.isfile(arguments[x])):
                filename.append(arguments[x])
            else:
                filenum = filenum - 1

        jstring = ""

        graphs_dict = {} # holds the file name as key and graph as value,  the graph name will be the file name
        graphs_size = {}
        graphs_names = {} # holds every name of every schema

        for x in range(0, filenum - 1):
            graphs_dict.update({filename[x]:nx.Graph()})
            graphs_size.update({filename[x]: 0})

        node_number = 0
        
        for x in range(0, filenum - 1):
            node_number = 0
            try:
                with open(filename[x], "r") as f:
                    jstring = f.read()
                jstring = removeSpaces(jstring)
                final = gr.Pro(jstring, 0, 0, 0, graphs_dict.get(filename[x]))
                graphs_size.update({filename[x]:final[3]})
            except FileNotFoundError:   #Ja foi verificado, mas vale deixar aqui ainda
                print("Arquivo %s não encontrado." % filename[x])#Ja criou o filename no dict

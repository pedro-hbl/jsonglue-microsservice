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
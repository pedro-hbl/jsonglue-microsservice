
def createRandomJSON1(qnt): # Creates 'qnt' JSON files in documents/ folder 
    if os.path.isdir('documents') == False: os.system('mkdir documents')
    pth = 'documents/caso1-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc1(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise


def createRandomJSON2(qnt): # Creates 'qnt' JSON files in documents/ folder 
    if os.path.isdir('documents') == False: os.system('mkdir documents')
    pth = 'documents/caso2-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc2(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise

def createRandomJSON3(qnt): # Creates 'qnt' JSON files in documents/ folder 
    if os.path.isdir('documents') == False: os.system('mkdir documents')
    pth = 'documents/caso3-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc3(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise
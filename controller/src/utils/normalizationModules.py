import os
import jsongenerator as jg

def formatTime(t):
    s = t% 60
    t = t / 60
    m = t % 60
    t = t / 60
    h = t
    return "{:02d}".format(int(h)) + 'h' + "{:02d}".format(int(m)) + 'm' + "{:02d}".format(int(s)) + 's'


def loadNamingStd():
    d_Names = {}

    with open("NamingStandards.txt") as f:
        for line in f:
            (val, key) = line.split()
            d_Names[key] = val
    return d_Names


def cleanString(in_str):
    if not isinstance(in_str, str):
        return None
    # Remove Special Char, Number....
    clean_str = re.sub('[^A-Za-z]+', ' ', in_str.lower())
    # Remove additional space between words
    clean_str = re.sub(' +', ' ', clean_str)
    # Extract Stop words
    stop_words = set(stopwords.words('english'))
    # Extract Stop words
    tokens = word_tokenize(clean_str)
    str_list = [w for w in tokens if not w in stop_words]
    return ' '.join(map(str, str_list))


def removeSpaces(js):
    ret = ''
    f = 1
    for i in js:
        if ((i == ' ' or i == '\n') and f == 1):
            continue
        elif (i == '"'):
            ret += i
            f *= -1
        else:
            ret += i
    return ret


def formatName(name):
    a = name.rfind('/')
    b = name.rfind('.')
    return name[a + 1:b]


def formatName2(name):
    a = name.rfind('/')
    return name[a + 1:]


def everyName(filename, x, graphs_dict, graphs_size, graphs_names):
    g = graphs_dict[filename[x]]  # The wanted graph
    size = graphs_size[filename[x]]  # The graph's size
    namelist = []
    for i in range(0, size):
        namelist.append(g.node[i]['name'])  # For every node, take it's name
    graphs_names.update({filename[x]: namelist})


def createRandomJSON1(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('documents') == False: os.system('mkdir documents')
    pth = 'documents/caso1-file.json'
    if os.path.isfile(pth) == True: os.system('rm  ' +pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc1(qnt))
    except:
        print('Erro ao salvar documento JSON em  '+ pth + ' .')
        raise


def createRandomJSON2(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('documents') == False: os.system('mkdir documents')
    pth = 'documents/caso2-file.json'
    if os.path.isfile(pth) == True: os.system('rm  ' +pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc2(qnt))
    except:
        print('Erro ao salvar documento JSON em  '+ pth + ' .')
        raise

def createRandomJSON3(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('documents') == False: os.system('mkdir documents')
    pth = 'documents/caso3-file.json'
    if os.path.isfile(pth) == True: os.system('rm  ' +pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc3(qnt))
    except:
        print('Erro ao salvar documento JSON em  '+ pth + ' .')
        raise
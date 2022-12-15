from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import os
import sys
import networkx as nx
import comp as cp
import grafo as gr
import time
import os.path
import sem
import jsongenerator as jg
import multiprocessing as mp
import data as dt
from colorama import Fore, Back, Style
import re  # regular expression
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from functools import partial



def loadNamingStd ():
    d_Names = {}

    with open("../controller/src/utils/NamingStandards.txt") as f:
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
    clean_str = re.sub(' +',' ',clean_str)
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
        if ((i == ' ' or i == '\n') and f == 1): continue
        elif(i == '"'):
            ret += i
            f *= -1
        else: ret +=i
    return ret
    

def formatName(name):
    a = name.rfind('/')
    b = name.rfind('.')
    return name[a+1:b]

def formatName2(name):
    a = name.rfind('/')
    return name[a+1:]

def everyName(filename, x, graphs_dict, graphs_size, graphs_names):
    g = graphs_dict[filename[x]] # The wanted graph
    size = graphs_size[filename[x]] # The graph's size
    namelist = []
    for i in range(0, size):
        namelist.append(g.node[i]['name']) # For every node, take it's name
    graphs_names.update({filename[x]:namelist})

def printResults(full):
    print('\n')
    for filecomp in full:
        print("             ==================        Schema " + Back.BLACK + Fore.WHITE + filecomp[0] + Style.RESET_ALL + ' vs Schema ' + Back.BLACK + Fore.WHITE + filecomp[1] + Style.RESET_ALL + '       ==================\n' )
        #print("========        Schema " + filecomp[0] + ' vs Schema ' + filecomp[1] + '       ========\n')
        for comparison in filecomp[2]:
            printAux(comparison)
            print("             ", end="")
            print(comparison[:3], end='')
            print('      -      ', end='')
            print(comparison[3:6], '\n')
            print("            ", comparison[6:len(comparison)])
            print('\n')
        print('\n\n')
        print("Press the <ENTER> key to continue...")
        input()


def printAux(comparison):
    print('               Form' + (' '*(len(comparison[0]))), end='')
    print('Sem'+ (' '*(len(str(comparison[1]))+1)), end='')
    print('Orig' + (' '*(len(str(comparison[2]))+13)), end='')
    print('Form' + (' '*(len(comparison[3]))), end='')
    print('Sem'+ (' '*(len(str(comparison[4]))+1)), end='')
    print('Orig')

    
def formatTime(t):
    s = t%60
    t = t/60
    m = t%60
    t = t/60
    h = t
    return "{:02d}".format(int(h))+'h'+"{:02d}".format(int(m))+'m'+"{:02d}".format(int(s))+'s'

def auxMultipro(a, x, y):
        b = dt.returnDataList(a, x, y)
        c = dt.returnAver(b)
        d = dt.buildHist(c)
        e = dt.normData(d)
        return e


def showName(name):
    i = name.rfind('/')
    if i == -1: return name
    return name[i+1:]


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('1000x800')
        self.schemas = []
        self.schema_flag = 0
        self.pg = 0
        self.mp = False
        self.results = []
        self.done = False
        self.pack()
        self.create_widgets()
        


    def returnFile(self):
        #self.master.progress.step(10)
        if self.done == True: 
            self.schemas = []
            self.master.listbox.delete(0, 'end')
            self.done = False
        file = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file")
        if file == (): return
        self.schemas.append(file)
        self.master.listbox.delete(0, 'end')
        if len(self.schemas) == 0: return
        else: 
            for x, i in enumerate(self.schemas): self.master.listbox.insert(x, showName(i))

    def addResults(self):
        # each list holds the comp of a pair of schemas
        #[file1, file2, [atr11, atr12, atr13, atr21, atr22, atr23, sin, sem, [av, dv, hist]], []]
        for i in self.results:
            line = 0
            tmp = Listbox(height = 10,  width = 30)
            #self.master.results_tabs.append(tmp)
            header = " "+i[0]+ " x " + i[1]            
            for x in i[2]:
                atr = str(x[0]) +', '+ str(x[1]) +', '+ str(x[2])
                tmp.insert(line, atr)
                line += 1
                atr = str(x[3])+', '+ str(x[4])+', '+ str(x[5])
                tmp.insert(line, atr)
                line += 1
                if len(x) == 7: res = 'None'
                else: 
                    res = '[sin =' + str(x[6]) + ', sem = ' + str(x[7]) + ', dados = '
                    if len(x[8]) == 4: res += '[ None ]]'
                    else : res += '[ ' + str(x[8][0]) + ', ' + str(x[8][1]) + ', ' + str(x[8][2]) + ']]'
                tmp.insert(line, res)
                line += 1
                tmp.insert(line, ' ')
                tmp.itemconfig(line, {'bg':'black'})
                line += 1
            self.master.results.add(tmp, text=header)


    def create_widgets(self):
        self.master.title('JSONGlue')
        self.master.schemaw_title = Label(text = 'Schemas', width = 30, anchor=CENTER)
        self.master.schemaw_title.place(x=730, y= 0)
        self.master.listbox = Listbox(height = 10,  width = 30)
        self.master.listbox.place(x=730, y= 30)
        self.master.fileButton = Button(text="Browser", width = 30, command=self.returnFile).place(x=730, y =200)
        self.master.toggle_m = Checkbutton(text='Multiprocessamento', command=self.mAux, var=self.mp)
        self.master.toggle_m.place(x=730, y=250)
        self.master.start = Button(text="START", width = 30, command=self.runJSONGlue)
        self.master.start.place(x=730, y=300)
        self.master.results = Notebook(width = 700, height = 780) 
        self.master.results.place(x=0, y=0)
        #self.master.progress = Progressbar(orient = 'horizontal', length = '650')
        #self.master.progress.place(x=0, y=780)

    def mAux(self):
        if self.mp == True: self.mp = False
        else: self.mp = True
        print(self.mp)


    def runJSONGlue(self):

        start = time.time()
        arguments = []
        for i in self.schemas:
            arguments.append(i)
        
        filenum = len(arguments)
        filename = [] 

        for x in range(0, filenum):
            if(os.path.isfile(arguments[x])):
                filename.append(arguments[x])
            else:
                filenum = filenum - 1

        jstring = ""

        graphs_dict = {}
        graphs_size = {}

        for x in range(0, filenum):
            graphs_dict.update({filename[x]:nx.Graph()})
            graphs_size.update({filename[x]: 0})


        node_number = 0
        for x in range(0, filenum):
            node_number = 0
            try:
                with open(filename[x], "r") as f:
                    jstring = f.read()
                jstring = removeSpaces(jstring)
                final = gr.Pro(jstring, 0, 0, 0, graphs_dict.get(filename[x]))
                graphs_size.update({filename[x]:final[3]})
            except FileNotFoundError:   #Ja foi verificado, mas vale deixar aqui ainda
                print("Arquivo %s não encontrado." % filename[x])#Ja criou o filename no dict

        std = loadNamingStd()

        if self.mp == True:
            print('MULTI')
            cores = mp.cpu_count()
            files = len(filename)
            if files > cores:pool1 = mp.Pool(cores)
            else:            pool1 = mp.Pool(files)

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
                if a == None: dt.applyData2Graph(a, graphs_dict[i], graphs_size[i])
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
                #graphs_dict[i].nodes[j]['name'] = cleanString(graphs_dict[i].nodes[j]['name'])
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

        if(filenum == 0):
            print("Não foi passado nenhum arquivo ou os arquivos não existem.")
        elif(filenum > 1):
            print('\nComparação de schemas iniciada.')
            if self.mp == True:
                pool = mp.Pool(mp.cpu_count())
                schemacomb = []
                for x in range(0, filenum):
                    for y in range(x+1, filenum):
                        schemacomb.append((x, y))
                comp = [pool.apply_async(cp.compGraph, args=(graphs_dict[filename[x]], graphs_dict[filename[y]], graphs_size[filename[x]], graphs_size[filename[y]], x, y)) for (x, y) in schemacomb]
                comp = [r.get() for r in comp]
                pool.close()
                pool.join()

                for i in comp: # TODO reescrever usando formatName
                    file1 = filename[i[0][0]]
                    file2 = filename[i[0][1]]
                    a1 = file1.rfind('/', 0)
                    a2 = file2.rfind('/', 0)
                    if a1 == -1:
                        header.append(file1)
                    else: header.append(file1[a1+1:len(file1)])
                    if a2 == -1:
                        header.append(file2)
                    else: header.append(file2[a2+1:len(file2)])
                    header.append(i[1])
                    full.append(header)
                    header = []
            else:
                for x in range(0, filenum):
                    for y in range(x+1, filenum):
                        header.append(formatName(filename[x]))
                        header.append(formatName(filename[y]))
                        comp = cp.compGraph(graphs_dict[filename[x]], graphs_dict[filename[y]], graphs_size[filename[x]], graphs_size[filename[y]], x, y)
                        header.append(comp[1])
                        full.append(header)
                        header = []
        else:
            print("Apenas um arquivo foi recebido")


        end = time.time()
        self.results = full
        self.done = True

        if len(self.results) != 0:
            f = self.master.results.tabs()
            for i in f: self.master.results.forget(i)

        self.addResults()
        

        if self.mp == True:print("Time multiprocess : "+ formatTime(end - start))
        else:            print("Time sequential : " + formatTime(end - start))
        return


root = Tk()
app = App(master=root)
app.mainloop()
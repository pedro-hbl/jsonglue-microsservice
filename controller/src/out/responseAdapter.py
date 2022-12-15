from colorama import Fore, Back, Style

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
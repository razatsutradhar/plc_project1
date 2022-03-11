from REParser import parser
from RENode import RENode
import getopt, sys

charID = -1
allNodes = []
followPos = {}
root = None
endNode = None
IdToChar = {}
CharToID = {}
DFA = {}
argumentList = sys.argv[1:]
options = "d:"
long_options = ["dfa"]

def eval_expression(tree):
    global allNodes
    global charID
    global followPos
    global endNode
    global IdToChar
    global CharToID

    # print(followPos)
    if tree[0] == 'char':
        charID = charID + 1
        followPos.update({charID: set()})

        if tree[1] not in CharToID.keys():
            CharToID[tree[1]] = set()
        CharToID[tree[1]].add(charID)

        n = RENode(_op='leaf', _sy=tree[1], _pos=charID)
        tree[1] = n
        allNodes.append(n)
        IdToChar.update({charID: tree[1]})
        if tree[1] == "#":
            endNode = charID
        return tree[1]
    elif tree[0] == 'cat':
        l = eval_expression(tree[1])
        r = eval_expression(tree[2])
        n = RENode(_op='.', _lc=l, _rc=r)
        allNodes.append(n)
        # print(l)
        for lp in l._lastpos:
            for fp in r._firstpos:
                followPos[lp].add(fp)
        return n

    elif tree[0] == 'union':
        # print(tree)
        l = eval_expression(tree[1])
        r = eval_expression(tree[2])
        n = RENode(_op='+', _lc=l, _rc=r)
        return n

    elif tree[0] == 'kleene':
        # print(tree)
        l = eval_expression(tree[1])
        # print(followPos)
        n = RENode(_op='*', _lc=l)
        for lp in l._lastpos:
            for fp in l._firstpos:
                followPos[lp].add(fp)
        return n


def constructDFA(followPos):
    global root
    global endNode
    global IdToChar
    global CharToID
    global DFA


    DFA = {}
    #{dict (key = tuple of nodes ids, value = dict(key = char, value = set of followpos ids) )
    DFAQueue = []
    DFAQueue.append(set(root._firstpos))
    # print(DFAQueue)
    while len(DFAQueue) > 0:
        currentSet = DFAQueue.pop()
        if endNode not in currentSet:
            possibleChars = {}
            #dict (key = char, value = set of node ids)
            for i in currentSet:
                node = IdToChar[i]
                if node._symbol not in possibleChars.keys():
                    possibleChars.update({node._symbol: {i}})
                else:
                    possibleChars[node._symbol].add(i)

            next_set = {}
            for k in possibleChars.keys():
                v = possibleChars[k]
                #k is char, v is node ids
                fp_set = set()

                # print("k: " + str(k) + " v: " + str(v))
                for id in v:
                    fp_set = fp_set.union(followPos[id])
                    # print(followPos[id])
                fp_set = tuple(fp_set)
                # print(fp_set)

                if fp_set not in DFA.keys():
                    DFAQueue.append(fp_set)
                next_set[k] = fp_set
            DFA[tuple(currentSet)] = next_set
            # print(DFAQueue)


    return DFA




def read_RE():
    result = ''
    while True:
        data = input('RE: ').strip()
        if ';' in data:
            i = data.index(';')
            result += data[0:i]
            result += "#;"
            # print(result)
            break
        else:
            result += data + ' '
    return result


def read_str():
    result = ''
    data = input('str: ').strip()
    if ';' in data:
        i = data.index(';')
        result += data[0:i]
    else:
        result += data + ' '

    # print(result)
    result.replace(" ", "")
    return result

def main():
    dfaToggle = False
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-d", "--dfa", "-dfa"):
            dfaToggle = True
            print("Displaying DFA")

    REset = False
    while True:
        global allNodes
        global charID
        global followPos
        global root
        charID = -1
        allNodes = []
        followPos = {}


        if not REset:
            data = read_RE()
            if data == 'exit#;':
                break
            try:
                # data += "#"
                tree = parser.parse(data)
            except Exception as inst:
                print(inst.args[0])
                continue
            try:
                answer = eval_expression(tree)
                root = answer
                DFA = constructDFA(followPos)
                if dfaToggle:
                    print(DFA)
                if isinstance(answer, str):
                    print('\nEVALUATION ERROR: ' + answer + '\n')
                else:
                    print('\nThe value is \n' + str(answer) + '\n')
                    REset = True
            except Exception as inst:
                print(inst.args[0])
        else:
            while True:
                data = read_str()
                # print(data)
                if data == 'exit':
                    REset = False
                    break
                else:
                    data += "#"

                data = list(data)
                data.reverse()
                # print(data)
                accept = True
                current_set = None
                while len(data) > 0:
                    if current_set == None:
                        current_char = data.pop()
                        if dfaToggle:
                            print("Current char: " + str(current_char))
                        if current_char not in CharToID.keys():
                            accept = False
                            break
                        char_nodes = CharToID[current_char]
                        current_set = root._firstpos
                        if char_nodes.intersection(current_set) == 0:
                            accept = False
                            break
                        else:

                            possibles = DFA[tuple(current_set)]
                            if current_char in possibles.keys():
                                current_set = possibles[current_char]
                                if dfaToggle:
                                    print("Current set: " + str(current_set))
                                    print("Possibilites: " + str(DFA[tuple(current_set)]) + "\n")

                            else:
                                accept = False
                                break
                    else:
                        current_char = data.pop()
                        possibles = DFA[tuple(current_set)]
                        if dfaToggle:
                            print("Current char: " + str(current_char) )
                            print("Current set: " + str(current_set) )
                            print("Possibilites: " + str(DFA[tuple(current_set)]) + "\n")
                        if current_char in possibles.keys():
                            current_set = possibles[current_char]
                            if dfaToggle:
                                print("Current char: " + str(current_char))
                                print("Current set: " + str(current_set))
                                print("Possibilites: " + str(DFA[tuple(current_set)]) + "\n")
                        else:
                            if dfaToggle:
                                print("Current char: " + str(current_char))
                                print("Current set: " + str(current_set))
                                print("Possibilites: " + str(DFA[tuple(current_set)]) + "\n")
                            accept = False
                            break

                if accept:
                    print("Accept")
                else:
                    print("Reject")








main()

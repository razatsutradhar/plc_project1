from REParser import parser
from RENode import RENode

charID = -1
allNodes = []
followPos = {}
root = None
endNode = None
IdToChar = {}


def eval_expression(tree):
    global allNodes
    global charID
    global followPos
    global endNode
    global IdToChar

    # print(followPos)
    if tree[0] == 'char':
        charID = charID + 1
        followPos.update({charID: set()})
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
    DFA = []
    DFAQueue = []
    DFA.append(set(root._firstpos))
    DFAQueue.append(set(root._firstpos))

    while len(DFAQueue) > 0:
        currentSet = DFAQueue.pop()
        possibleChars = {}
        for i in currentSet:
            node = IdToChar[i]
            if node._symbol not in possibleChars.keys():
                possibleChars.update({node._symbol: {i}})
            else:
                possibleChars[node._symbol].add(i)
        for charset in
    print(IdToChar.values())



def read_input():
    result = ''
    while True:
        data = input('RE: ').strip()
        if ';' in data:
            i = data.index(';')
            result += data[0:i + 1]
            break
        else:
            result += data + ' '
    return result


def main():
    while True:
        global allNodes
        global charID
        global followPos
        charID = -1
        allNodes = []
        followPos = {}

        data = read_input()
        if data == 'exit;':
            break
        try:
            tree = parser.parse(data)
        except Exception as inst:
            print(inst.args[0])
            continue
        try:
            answer = eval_expression(tree)
            root = answer
            constructDFA(followPos)
            print(followPos)

            if isinstance(answer, str):
                print('\nEVALUATION ERROR: ' + answer + '\n')
            else:
                print('\nThe value is \n' + str(answer) + '\n')
        except Exception as inst:
            print(inst.args[0])


main()

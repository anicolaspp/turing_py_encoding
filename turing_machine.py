class State:
    def __init__(self, tag, dictionary, isFinal):
        self.tag = tag
        self.function = dictionary
        self.isFinal = isFinal

    def Transaction(self, char):
        if self.function.__contains__(char):
            return self.function[char]
        else:
            return None

    def __str__(self):
        return self.tag + ': ' +str(self.isFinal)


class Config:
    def __init__(self, state, pos, tape):
        self.state = state
        self.pos = pos
        self.tape = tape

    def __Conv__(self, l):
        x = ''
        for i in l:
            x += str(i)
        return x

    def __str__(self):
        return '(' + str(self.state) + ', ' + str(self.__Conv__(self.tape)) + ', ' + str(self.pos) + ')'

    def __eq__(self, other):
        if self.state.tag == other.state.tag and self.tape == other.tape and self.pos == other.pos:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Machine:
    def __init__(self, tape, states, initState, description = ''):
        self.tape = tape
        self.states = states
        self.initState = initState
        self.description = description

        self.currentPos = 0
        self.count = 0
        self.currentState = self.initState

    def get_Config(self):
        return Config(self.currentState, self.currentPos, self.tape)

    def __set_State__(self, tag):
        for item in self.states:
            if item.tag == tag:
                return item

        raise 'El estado al cual se hace referencia en la transaccion no es parte de los estados de la maquina'
        
    def MoveNext(self):
        prox = self.currentState.Transaction(self.tape[self.currentPos])
        if prox != None:
            self.currentState = self.__set_State__(prox[1])
            self.tape[self.currentPos] = prox[0]
            self.count += 1
            if prox[2] == -1:
                if self.currentPos > 0:
                    self.currentPos -= 1
            else:
                self.currentPos += prox[2]
                
            return True
        else:
            return False

class Debuger:
    def __init__(self, machine):
        self.machine = machine
        self.record = []

    def __CicleDetect__(self):
        for i in range(len(self.record) - 1):
            for j in range(i + 1, len(self.record)):
                if self.record[i] == self.record[j]:
                    return True
        return False

    def Run(self):
        prox = self.machine.get_Config()
        print prox
        self.record.append(prox)
        while self.machine.MoveNext():
            prox = self.machine.get_Config()
            print prox 
            self.record.append(prox)
           
            if self.__CicleDetect__():
                print 'La maquina no reconoce el lenguage, cae en un ciclo infinito'
               
                return
        
        t = self.machine.get_Config()
        if t.state.isFinal:
            print 'La maquina reconoce el lenguage'
          
            return 
        else:
            print 'No se reconoce el lenguage, se llega a un estado para el cual no hay transaccion y tampoco es final'
            
            return 

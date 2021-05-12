# qlearningAgents.py
# ------------------

import util, os, random, time, datetime
from game import Agent
from game import Directions
from distanceCalculator import Distancer
from bustersAgents import BustersAgent
from learningAgents import ReinforcementAgent


""" CONSTANTS """
TABLE_FOLDER           = 'qtables'
path_qTable        = 'pacman_qtable.txt'
POSSIBLE_ACTIONS        = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]


class QLearningAgent(BustersAgent, ReinforcementAgent):
    
    def __init__(self, **args):
        # Iniciamos el agente BusterAgents por una parte con sus argumentos
        busters_agent_args = {}
        busters_agent_args['ghostAgents'] = args['ghostAgents']

        # Iniciamos el agente ReinforcementAgent por otra parte con sus argumentos
        reinforcement_agent_args = {}
        reinforcement_agent_args['alpha'] = args['alpha']
        reinforcement_agent_args['epsilon'] = args['epsilon']
        reinforcement_agent_args['gamma'] = args['gamma']
        reinforcement_agent_args['actionFn'] = self.getPossibleActions
        
        # Los inicializo a los dos
        BustersAgent.__init__(self, **busters_agent_args)
        ReinforcementAgent.__init__(self, **reinforcement_agent_args)

        "Cargamos la Q-Table"
        if not os.path.exists("qtable.txt"):
            self.qtableInicial("qtable.txt")
        
        self.path_qTable = open("qtable.txt", 'r+')
        self.qtable = self.readQtable()
        self.writeQtable()

        # Guardo valores relevantes sobre el estado del juego
        self.score_final=0
        self.num_updates=0
        

    def getPossibleActions(self, state):
        return POSSIBLE_ACTIONS

    #NEW
    def registerInitialState(self, gameState):
        ReinforcementAgent.registerInitialState(self, gameState)
        BustersAgent.registerInitialState(self, gameState)
        self.countActions = 0
    
    def __del__(self):
        "Destructor. Invokation at the end of each episode"
        self.writeQtable()
        self.path_qTable.close()

    #NEW
    # Función que nos permite crear el fichero qTable vacio
    def qtableInicial(self, path):
        file = open(path, 'w')
        file.flush()
        file.close()

    #MODIFIED
    def readQtable(self):
        "Read qtable from disc"
        table = self.path_qTable.readlines()
        extra_table = {}

        # Realizamos un bucle respecto al numero de filas de la qtable, que son los estados
        for i, line in enumerate(table):
            #Separamos las filas del fichero
            row = line.split()
            #Selecciono el estado
            state = row[0]
            actions = []
            #Recorremos las acciones incluidas en el estado y almacenamos su valor
            for n in range(1, len(row)):
                actions.append(float(row[n]))
            # Añadimos la lista de acciones al estado correpondiente
            extra_table[state] = actions

        return extra_table

    #UPDATED (ellos cambian mas cosas)
    """def writeQtable(self):
        #Si no se permite la actualización de la tabla
        if self.alpha == 0:
            return

        "Write qtable to disc"
        self.path_qTable.seek(0)
        self.path_qTable.truncate()

        for line in self.qtable:
            for item in line:
                self.path_qTable.write(str(item)+" ")
            self.path_qTable.write("\n")

        self.path_qTable.flush()
    """
    #UPDATED
    def writeQtable(self):
        # Si no hay tasa de aprendizaje -> la tabla no se va a modificar
        if self.alpha == 0: 
            return

        #Nos situamos al principio del fichero y borramos todos los valores de qtable.txt actuales
        self.path_qTable.seek(0)
        self.path_qTable.truncate()


        # Ordenamos los estados de la qtable y los recorremos para escribirlos
        for i, (k, v) in enumerate(self.qtable.items()):
            
            # Recorro cada accion y añado su valor
            vstr = ' '.join(['{:.3f}'.format(x) for x in v])
            self.path_qTable.write(k + ' ' + vstr + '\n')

        self.path_qTable.flush()

    #MODIFIED
    def printQtable(self):
        "Print qtable"
        for line in self.qtable.items():
            print(line)
        print("\n")    

    


    #NEW --> AQUI DEFINIMOS EL ESTADO QUE QUERAMOS!!
    def definicionEstado(self, gameState):
            # Adjacents : 3 values (empty, wall, useful) ^ 8 (positions)
            pacman_position = gameState.getPacmanPosition()
            posicion_fantasmas = gameState.getGhostPositions()

            state = '[('
            # Miro lo que tengo a los lados
            for i in range (-1, 3, 2):
                if gameState.hasWall(pacman_position[0] + i, pacman_position[1]):
                    state += 'W'
                elif (pacman_position[0] + i, pacman_position[1]) in posicion_fantasmas:
                    state += 'G'
                else:
                    state += 'E'
                # Miro las casillas que tengo encima y debajo del lado al que me haya movido --> la diagonal al pacman   
                for k in range (-1, 3, 2):
                    if gameState.hasWall(pacman_position[0] + i, pacman_position[1] + k):
                        state += 'W'
                    elif (pacman_position[0] + i, pacman_position[1] + k) in posicion_fantasmas:
                        state += 'G'
                    else:
                        state += 'E'

            
            # Miro lo que tengo encima y debajo
            for j in range (-1, 3, 2):
                if gameState.hasWall(pacman_position[0], pacman_position[1]+j):
                    state += 'W'
                elif (pacman_position[0], pacman_position[1]+j) in posicion_fantasmas:
                    state += 'G'
                else:
                    state += 'E'
            state += ')'
            

            
            if any(x != None for x in gameState.data.ghostDistances):
                fantasma_index = gameState.data.ghostDistances.index(min(x for x in gameState.data.ghostDistances if x is not None))
                distancer = Distancer(gameState.data.layout)
                state += '(' + str(distancer.getDistance(pacman_position, posicion_fantasmas[fantasma_index])) + ')'
            
            

            """ for i in range(-1,2,1):
                for j in range(-1,2,1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if gameState.hasWall(pacman_position[0] + i, pacman_position[1] + j):
                            state += 'W'
                        elif (pacman_position[0] + i, pacman_position[1] + j) in ghosts_positions:
                            state += 'G'
                        elif gameState.hasFood(pacman_position[0] + i, pacman_position[1] + j):
                            state += 'F'
                        else:
                            state += 'E'
                    except:
                        state += 'W'
            """
            #state += ')'

            # Rel pos closest ghost
            #getDistanceNearestFood
            """
            if any(x != None for x in gameState.data.ghostDistances):
                ghost_index = gameState.data.ghostDistances.index(min(x for x in gameState.data.ghostDistances if x is not None))
                diff_x, diff_y = (p - g for p, g in zip(ghosts_positions[ghost_index], pacman_position))
                if diff_y > 0:
                    if diff_x > 0:
                        state += '(UR)'
                    elif diff_x < 0:
                        state += '(UL)'
                    else:
                        state += '(U)'
                elif diff_y < 0:
                    if diff_x > 0:
                        state += '(DR)'
                    elif diff_x < 0: 
                        state += '(DL)'
                    else:
                        state += '(D)'
                else:
                    if diff_x > 0: 
                        state += '(R)'
                    elif diff_x < 0:
                        state += '(L)'
                    else:
                        state += '(O)'
                distancer = Distancer(gameState.data.layout)
                state += '(' + str(distancer.getDistance(pacman_position, ghosts_positions[ghost_index]))
            state += ')(' + ('last' if len([living for living in gameState.getLivingGhosts() if living is True]) == 1 else 'more')
            """

            # getDistanceNearestFood
            """state += ')'
            if(gameState.getNumFood() > 0):
                minDistance = 900000
                minPosition = ()
                for i in range(gameState.data.layout.width):
                    for j in range(gameState.data.layout.height):
                        if gameState.hasFood(i, j):
                            foodPosition = i, j
                            distance = util.manhattanDistance(pacman_position, foodPosition)
                            if distance < minDistance:
                                minPosition = foodPosition
                                minDistance = distance
                diff_x, diff_y = (p - g for p, g in zip(minPosition, pacman_position))
                if diff_y > 0:
                    if diff_x > 0:
                        state += '(UR)'
                    elif diff_x < 0:
                        state += '(UL)'
                    else:
                        state += '(U)'
                elif diff_y < 0:
                    if diff_x > 0:
                        state += '(DR)'
                    elif diff_x < 0: 
                        state += '(DL)'
                    else:
                        state += '(D)'
                else:
                    if diff_x > 0: 
                        state += '(R)'
                    elif diff_x < 0:
                        state += '(L)'
                    else:
                        state += '(O)'
                state += '(' + str(minDistance)
            else:
                state += '()('
            """    
            #state += ')(' + ('1' if gameState.getNumFood() > 0 else '0')

            return state + ')]'

    #MODIFIED
    def getQValue(self, state, action):

        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        # Si no existe ese estado, lo generamos con 0 a todas las posibles acciones que se permiten
        if state not in self.qtable:
            self.qtable[state] = [float(0) for x in POSSIBLE_ACTIONS]
        
        # Devolvemos el valor de la qtable para ese estado con esa accion
        return self.qtable[state][POSSIBLE_ACTIONS.index(action)]

    
    

    #MODIFIED
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legalActions = self.getLegalActions(state)
        # Si no quedan acciones --> estamos en el estado final --> 0
        if len(legalActions) == 0:
          return 0
        # Si el estado no existe se devuelve un valor 0
        if state not in self.qtable:
            return 0
        # Devuelve la acción con mayor valor q en ese estado
        return max(self.qtable[state])

    #NOT MODIFIED
    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = self.getLegalActions(state)

        if len(legalActions)==0:
          return None

        best_actions = [legalActions[0]]
        best_value = self.getQValue(state, legalActions[0])

        for action in legalActions:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value

        return random.choice(best_actions)

    #MODIFIED --> getAction --> getActionQLearning
    def getActionQLearning(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """

        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None

        if len(legalActions) == 0:
             return action

        flip = util.flipCoin(self.epsilon)

        if flip:
            return random.choice(legalActions)
        
        return self.getPolicy(state)

    #MODIFIED
    def update(self, state, action, nextState, reward):
        '''
        if terminal_state:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        else:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))
        '''
        # Calculamos el estado actual
        qstate_actual = self.definicionEstado(state)
        # Calculamos el siguiente estado
        qstate_siguiente = self.definicionEstado(nextState)
        
        # Miramos cual es la acción que se solicita actualizar
        column = POSSIBLE_ACTIONS.index(action)

        # Si el estado no exisste crearemos esa fila con 0
        if qstate_actual not in self.qtable:
            self.qtable[qstate_actual] = [float(0) for _ in POSSIBLE_ACTIONS]
        
        # Obtemos el qvalue actual de esa acción en ese estado
        qValue = self.qtable[qstate_actual][column]

        if len(self.getLegalActions(nextState)) == 0:
            self.qtable[qstate_actual][column] = (1-self.alpha)*qValue + self.alpha* (reward + 0)
        else:
            # Lo actualizamos
            self.qtable[qstate_actual][column] = (1-self.alpha)*qValue + self.alpha* (reward + self.discount*self.getValue(qstate_siguiente))
        
        #print("Update State ["+ str(qstate_actual) +"]")
        #print("Update State [" + str(qstate_actual) + "][" + action + "]=>[" + str(qstate_siguiente) + "] r=" + str(reward))
        self.num_updates += 1

        # TRACE for updated q-table. Comment the following lines if you do not want to see that trace
        #print("Q-table:")
        #self.printQtable()

    def getPolicy(self, state):
        "Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        "Return the highest q value for a given state"
        return self.computeValueFromQValues(state)

    #NEW 
    """Función para ejecutar el final de un episodio"""
    def final(self, state):
        self.score_final = state.getScore()

        print('Estadísticas episodio ' + str(self.episodesSoFar)+": ")
        print('num_updates acumulado:  '+str(self.num_updates)+", score final: "+str(self.score_final))

        return ReinforcementAgent.final(self, state)

    

    """ """
    def chooseAction(self, gameState):
        #Cogemos el estado del juego
        key_state = self.definicionEstado(gameState)
        #Seleccionamos la mejor opcion de la qstate
        action = self.getActionQLearning(key_state)

        
        #Mandamos realizar la accion
        ReinforcementAgent.doAction(self, gameState, action)

        
        legal = gameState.getLegalPacmanActions()
        if action not in legal:
            return random.choice(legal)
        
        return action
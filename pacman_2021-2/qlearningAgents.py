# qlearningAgents.py
# ------------------

import util, os, random, time, datetime
from game import Agent
from game import Directions
from distanceCalculator import Distancer
from bustersAgents import BustersAgent
from learningAgents import ReinforcementAgent


""" CONSTANTS """
QTABLE_FOLDER           = 'qtables'
QTABLE_FILENAME         = 'pacman_qtable.txt'

POSSIBLE_ACTIONS        = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

""" FLAGS """
TRACE_SHOW_QTABLE       = False
TRACE_ACTION_DECISION   = False
TRACE_UPDATE            = False
TRACE_BEST_ACTION       = False
TRACE_STATE             = False

class QLearningAgent(BustersAgent, ReinforcementAgent):
    
    def __init__(self, **args):
        # BusterAgents arguments
        busters_agent_args = {}
        busters_agent_args['ghostAgents'] = args['ghostAgents']

        # ReinforcementAgent arguments
        reinforcement_agent_args = {}
        for attr in ['alpha', 'epsilon', 'gamma']:
            reinforcement_agent_args[attr] = args[attr]
        reinforcement_agent_args['actionFn'] = self.getPossibleActions

        "Initialize Agents"
        BustersAgent.__init__(self, **busters_agent_args)
        ReinforcementAgent.__init__(self, **reinforcement_agent_args)

        "Q-Table"
        if not os.path.exists("qtable.txt"):
            self.createInitialQTable("qtable.txt")

        self.table_file = open("qtable.txt", 'r+')
        self.qtable = self.readQtable()
        self.writeQtable()

        # Agent stats
        self.stats = {
            'final_score'     : 0,
            'qtable_updates'  : 0,
        }

    #NEW
    """ """
    def registerInitialState(self, game_state):
        BustersAgent.registerInitialState(self, game_state)
        self.countActions = 0
    
    """ """    
    def __del__(self):
        "Destructor. Invokation at the end of each episode"
        self.writeQtable()
        self.table_file.close()

    #NEW
    def createInitialQTable(self, path):
        file = open(path, 'w')
        file.flush()
        file.close()

    #MODIFIED
    def readQtable(self):
        "Read qtable from disc"
        table = self.table_file.readlines()
        q_table = {}

        for i, line in enumerate(table):
            row = line.split()
            state = row[0]
            actions = []
            for n in range(1, len(row)):
                actions.append(float(row[n]))
            q_table[state] = actions

        return q_table

    #UPDATED (ellos cambian mas cosas)
    """def writeQtable(self):
        #Si no se permite la actualización de la tabla
        if self.alpha == 0:
            return

        "Write qtable to disc"
        self.table_file.seek(0)
        self.table_file.truncate()

        for line in self.qtable:
            for item in line:
                self.table_file.write(str(item)+" ")
            self.table_file.write("\n")

        self.table_file.flush()
    """
    """ UPDATES QTABLE FILE """
    def writeQtable(self):
        if self.alpha == 0: 
            return

        self.table_file.seek(0)
        self.table_file.truncate()

        if TRACE_SHOW_QTABLE: 
            self.trace("\n\nQTABLE>\n")

        for i, (k, v) in enumerate(sorted(self.qtable.items())):
            vstr = ' '.join(['{:.4f}'.format(x) for x in v])
            self.table_file.write(k + ' ' + vstr + '\n')

            if TRACE_SHOW_QTABLE:
                self.trace('[' + k + '] =' + '(' + vstr + ')')

        self.table_file.flush()

    def printQtable(self):
        "Print qtable"
        for line in self.qtable.items():
            print(line)
        print("\n")    

     #NEW       
    def getPossibleActions(self, state):
        return POSSIBLE_ACTIONS

    #NEW --> AQUI DEFINIMOS EL ESTADO QUE QUERAMOS!!
    def computeQLearningState(self, game_state):
            # Adjacents : 3 values (empty, wall, useful) ^ 8 (positions)
            pacman_position = game_state.getPacmanPosition()
            ghosts_positions = game_state.getGhostPositions()

            state = '[('
            for i in range(-1,2,1):
                for j in range(-1,2,1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if game_state.hasWall(pacman_position[0] + i, pacman_position[1] + j):
                            state += 'W'
                        elif (pacman_position[0] + i, pacman_position[1] + j) in ghosts_positions:
                            state += 'G'
                        elif game_state.hasFood(pacman_position[0] + i, pacman_position[1] + j):
                            state += 'F'
                        else:
                            state += 'E'
                    except:
                        state += 'W'

            state += ')'

            # Rel pos closest ghost
            #getDistanceNearestFood

            if any(x != None for x in game_state.data.ghostDistances):
                ghost_index = game_state.data.ghostDistances.index(min(x for x in game_state.data.ghostDistances if x is not None))
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
                distancer = Distancer(game_state.data.layout)
                state += '(' + str(distancer.getDistance(pacman_position, ghosts_positions[ghost_index]))
            state += ')(' + ('last' if len([living for living in game_state.getLivingGhosts() if living is True]) == 1 else 'more')


            # getDistanceNearestFood
            state += ')'
            if(game_state.getNumFood() > 0):
                minDistance = 900000
                minPosition = ()
                for i in range(game_state.data.layout.width):
                    for j in range(game_state.data.layout.height):
                        if game_state.hasFood(i, j):
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
                
            #state += ')(' + ('1' if game_state.getNumFood() > 0 else '0')

            return state + ')]'

    #MODIFIED
    def getQValue(self, state, action):

        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        if state not in self.qtable:
            self.qtable[state] = [float(0) for x in POSSIBLE_ACTIONS]
        

        return self.qtable[state][POSSIBLE_ACTIONS.index(action)]

    #NEW
    def setQValue(self, state, action, value):
        value_ = float(0)
        if state in self.qtable:
            value_ = value
        
        column = POSSIBLE_ACTIONS.index(action)
        self.qtable[state][column] = value_

        return value_
    """
    def computePosition(self, state):
        
        #Compute the row of the qtable for a given state.
        #For instance, the state (3,1) is the row 7
        
        return state[0]+state[1]*4
    """
    

    #MODIFIED
    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legalActions = self.getLegalActions(state)
        if len(legalActions)==0:
          return 0
        if state not in self.qtable:
            return 0
        #return max(self.q_table[self.computePosition(state)])
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
        print("Entro en update")
        '''
        if terminal_state:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        else:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))
        '''
        qstate = self.computeQLearningState(state)
        qnextState = self.computeQLearningState(nextState)
        

        column = POSSIBLE_ACTIONS.index(action)

        
        
        if qstate not in self.qtable:
            self.qtable[qstate] = [float(0) for _ in POSSIBLE_ACTIONS]

        qValue = self.qtable[qstate][column]
        
        self.qtable[qstate][column] = (1-self.alpha)*qValue + self.alpha* (reward + self.discount*self.getValue(qnextState))
        
        print("Update State ["+ str(qstate) +"]")
        print("Update State [" + str(qstate) + "][" + action + "]=>[" + str(qnextState) + "] r=" + str(reward))
        self.stats['qtable_updates'] += 1

        # TRACE for updated q-table. Comment the following lines if you do not want to see that trace
        print("Q-table:")
        self.printQtable()

    def getPolicy(self, state):
        "Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        "Return the highest q value for a given state"
        return self.computeValueFromQValues(state)

    #NEW 
    """Función para ejecutar el final de un episodio"""
    def final(self, state):
        self.stats['final_score'] = state.getScore()

        print('Final Statictics:')
        for stat in enumerate(self.stats):
            print('  '+str(stat[0])+"/"+str(stat[1]))

        return ReinforcementAgent.final(self, state)

    

    """ """
    def chooseAction(self, game_state):
        #Cogemos el estado del juego
        key_state = self.computeQLearningState(game_state)
        #Seleccionamos la mejor opcion de la qstate
        action = self.getActionQLearning(key_state)

        
        #Mandamos realizar la accion
        ReinforcementAgent.doAction(self, game_state, action)

        
        legal = game_state.getLegalPacmanActions()
        if action not in legal:
            return random.choice(legal)
        
        return action
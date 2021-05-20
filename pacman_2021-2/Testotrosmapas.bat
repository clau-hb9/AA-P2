
"Ejecutar: Test.bat"
@echo off
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l oneHunt -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l openHunt -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l BigHunt -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l testClassic -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l newmap -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l mimapa -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l tryckyClassic -m 2500
python busters.py -p QLearningAgent -a "alpha=0,epsilon=0,gamma=0" -t 0 -n 1 -k 3 -l minimaxClassic -m 2500

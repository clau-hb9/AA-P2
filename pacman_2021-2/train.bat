
"Ejecutar: train.bat"
@echo off
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 100 -k 1 -l labAA1 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 100 -k 2 -l labAA2 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 100 -k 1 -l labAA3 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 200 -k 2 -l labAA3 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 200 -k 3 -l labAA3 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 100 -k 1 -l labAA4 -m 2500 
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 200 -k 2 -l labAA4 -m 2500 
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 200 -k 3 -l labAA4 -m 2500 
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 100 -k 1 -l labAA5 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 200 -k 2 -l labAA5 -m 2500
python busters.py -p QLearningAgent -a "alpha=0.8,epsilon=0.2,gamma=0.9" -t 0 -n 200 -k 3 -l labAA5 -m 2500

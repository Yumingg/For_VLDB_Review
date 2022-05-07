# Paper \#132 submitted to VLDB 2023

## Description

This repository assists reviewers reproduce the Monte Carlo simulation results and system experiments in Paper \#132.
We provide the source code files of both Monte carlo simulation, system repository and a detailed guidebook so that the experiments can be reproduced by reviewers. 

## Repository Content
List experiment/simulation codes:

```
1. System_Experiment
	-- nxt % The modified NXT evaluation client
	-- Single_Player %  Pool Management Tool for Single Attacker Case
	-- Two_Player %  Pool Management Tool for Two Player Case
	-- Five Player %  Pool Management Tool for Five Player Case
2. Simulation
	-- One Pool Experiment  %  Simulation of One Pool Experiment
	-- More_Two_Attacker  %  More Experiments on Singe Attacker scenario
	-- More_Two_Attacker_solo %  More Experiments on Two Player scenario
	-- More_Five_player_game %  More Experiments on Five Attacker scenario
	-- More_Ten_player_game %  More Experiments on Ten Attacker scenario
```

## System Experiments
Ethereum and NXT client are opensourced projects. The sourcecode of three systems can be in the links below. Our PoS mining experiment modifies the current NXT client, to reproduce the experiment shown in Paper. The modified NXT client can be found in this repository. 

[Nxt Blockchain Creation Kit](https://bitbucket.org/Jelurida/nxt-clone-starter/src/master/)

[Geth Client](https://github.com/ethereum/go-ethereum) 

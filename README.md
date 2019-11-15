# hpcdrsim

HPC Demand Response Simulator

Description:
A demand response HPC job simulator, with resource optimization
framework.

Data:
Sample data can be found inside “data” folder.
Job trace file collected from parallel workload archive
(https://www.cs.huji.ac.il/labs/parallel/workload/).
Power and runtime information collected from literature (such as,
Auweter, Axel, et al. "A case study of energy aware scheduling on
supermuc." International Supercomputing Conference. Springer, Cham,
2014.)

Simulation test cases:
Sample test cases can be found inside “simulation_tests” folder.

Power and performance prediction model:
Regression models are used to predict application power and
performance for unknown values (e.g., unknown processor frequency).
Details of the models can be found in this article: Ahmed, Kishwar,
Jason Liu, and Xingfu Wu. "An energy efficient demand-response model
for high performance computing systems." 2017 IEEE 25th International
Symposium on Modeling, Analysis, and Simulation of Computer and
Telecommunication Systems (MASCOTS). IEEE, 2017.

Simulation framework:
Simulus - A Discrete-Event Simulator in Python (https://simulus.readthedocs.io/)





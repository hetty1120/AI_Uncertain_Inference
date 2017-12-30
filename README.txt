Readme!Work is done with python 3For four python files:1) Run them in terminal;2) Make sure that python files and XML/BIF files are under same folder;3) Input format (the order is important, one sentence every time): for exact inference, type the name of file which has information about variables and probability, the query variable, names and values of evidence variables (examples are shown below). For approximate inference, type the name of file which has information about variables and probability, the sampling times, the query variable, names and values of evidence variables (examples are shown below). 4) The program will show the probability distribution of the query variable given evidence variables and running time.5) If there are is no more problem, type ¡°END¡± to exit.  Queries:For Exact inference(exact-inference.py):

aima-alarm.xml B J true M true

aima-wet-grass.xml R S true

insurance.bif Accident Mileage TwentyThou Age Adult AntiTheft True Cushioning Fair DrivingSkill SubStandard ThisCarCost TenThou CarValue TenThou HomeBase City DrivHist One ThisCarDam Mild RiskAversion Psychopath MedCost Thousand ILiCost Thousand


For approximate inference(three algorithms have same input format, rejection/likelihood/gibbs.py):

aima-alarm.xml 5000 B J true M true

aima-wet-grass.xml 1000 R S true

alarm.bif 10000 LVEDVOLUME HRBP NORMAL TPR NORMAL

insurance.bif 10000 Accident Mileage TwentyThou Age Adult AntiTheft True Cushioning Fair DrivingSkill SubStandard ThisCarCost TenThou CarValue TenThou HomeBase City DrivHist One ThisCarDam Mild RiskAversion Psychopath MedCost Thousand ILiCost Thousand

insurance.bif 20000 Age AntiTheft True Cushioning Fair DrivingSkill SubStandard ThisCarCost TenThou CarValue TenThou SocioEcon Middle Mileage TwentyThou MakeModel Economy OtherCarCost Thousand
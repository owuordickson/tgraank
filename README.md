## T-GRAANK
A python implementation of the <i>Temporal-GRAdual rANKing</i> algorithm.<br>
<!-- Research paper published at FuzzIEEE 2019 International Conference on Fuzzy Systems (New Orleans): link<br> -->

### Getting Started:
Example Python program (file: UserMain.py)<br>
```python
from python.algorithm.UserMain import *
main("data/test.csv", 0, 0.1, 0.98)
```
The input parameters are: <i>main(file, referenceItem, minimumSupport, minimumRepresentativity).</i> You are required to choose <strong>file</strong> in csv format, make sure the timestamp column is the first. You specify:
* <strong>reference item</strong> - column\attribute that is the base of the temporal transformations
* <strong>minimum support</strong> - the threshold count of frequent FtGPs
* <strong>mimimum representativity item</strong> - the threshold of the number of transfomations on the data-set

Output:
```
Dataset Ok
{'Transformation': 'n+1', 'Representativity': 0.98, 'Included Rows': 49, 'Total Rows': 50}
1 : exercise_hours**
2 : stress_level
Pattern : Support
{'1+', '2+'} : 0.2814625850340136 | ~ +2.0 days : 1.0
{'2-', '1+'} : 0.1870748299319728 | ~ +1.4 days : 1.0
---------------------------------------------------------
```

### Credits:
1. Prof. Anne Laurent - LIRMM <i>Université de Montpellier 2</i><br>
2. Dr. Joseph Orero - Faculty of IT, <i>Strathmore University<br>
 
### License:
MIT

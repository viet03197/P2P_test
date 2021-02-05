# P2P_test
Simple P2P system in python

TODO
- [x] Basic concept (connection, broadcast...)
- [ ] Port management
- [ ] Puzzle
- [ ] Work
- [ ] Data structure
- [ ] Command Exchange
- [ ] Comment the code

Libraries used:
- socket for socket use
- sys for input from the command line

Example:
* Create first node: 
``` python node.py 8000```
* Create new node connecting to 8000: 
``` python node.py r 8000```
* Use of wallet
  * Consult connected peers:
 ```python wallet.py consult 8000```
 ``` python wallet.py consult 8001```
  * Broadcast messages:
 ``` python wallet.py chat 8000```


import socket
import sys
import threading

is_first = len(sys.argv) == 2    # Easy way to know if a node is first one
host = socket.gethostname()
port = sys.argv[-1]
class Node:
    def __init__(self, host, port, peers=[], peers_assigned=[], connections=dict()):
        self.host = host
        self.port = port
        self.connections = connections
        self.peers = peers
        self.peers_assigned = peers_assigned    
    # ============================================================================== #
    def set_port(self, p):
        self.port = p
    # ============================================================================== #
    def set_peers(self, p, conn, p_a):
        self.peers.append(p)
        self.connections[p] = conn
        self.peers_assigned.append(p_a)
    # ============================================================================== #
    def generate_next_listen_port(self):
        return self.port%8000*3 + len(self.peers) + 8001
    # ============================================================================== #
    def broadcast(self, msg):
        """ Send msg to all the peers of this node
        """
        for p in self.peers:
            if p != self.port:
                self.connections[p].send(msg)
    # ============================================================================== #
    def generate_connected_peers(self):
        msg = f'Current connected peers are :'
        for p in self.peers:
            msg += str(p) + ' '
        msg = bytes(msg, 'utf-8')
        return msg
    # ============================================================================== #
    def listening(self, p=None):
        """ Set up a socket for listening to other peers
        """
        if p == None: p = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, p))
        print(f'Initializing connection on port {p}')
        s.listen(3)
        while True:
            new_connection, peer_address = s.accept()
            if peer_address[1] != 10000 and peer_address[1] != 10001:
                assign_port = self.generate_next_listen_port()
                print(f'Peer {peer_address[1]} is connecting to me! Listen port {assign_port}')
                msg = f'A new peer {peer_address[1]} has connected to port {p}'
                msg = bytes(msg, 'utf-8')
                self.broadcast(msg) # Inform all connected peers
                msg = self.generate_connected_peers()
                new_connection.send(msg) # Send the list of connected peers to new peer
                msg = bytes(str(assign_port), 'utf-8')
                print(f'Assigning a new port {assign_port} to this node')
                new_connection.send(msg) # Send the assigned port to the peer (listening port)
                self.peers_assigned.append(assign_port)
                self.peers.append(peer_address[1])
                self.connections[peer_address[1]] = new_connection
            elif peer_address[1] == 10000:
                msg = self.generate_connected_peers()
                new_connection.send(msg) # Send the list of connected peers to the wallet
                new_connection.shutdown(socket.SHUT_RDWR)
                new_connection.close()
            elif peer_address[1] == 10001:
                print('Attempt to connect with wallet!')
                msg = self.receiving_tmp(10002)
                print('Received wallet message!')
                if msg != None:
                    msg = bytes(msg, 'utf-8')
                    self.broadcast(msg)
    # ============================================================================== #
    def receiving(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, int(port)))
        assign_port = 0
        print(f'I am connecting to the port {self.port}. My address is {s.getsockname()[1]}.')
        while True:
            msg = s.recv(1024).decode('utf-8')
            if len(msg) > 0:
                if len(msg) == 4:   # Get the assigned port for listening
                    assign_port = int(msg)
                    print(f'My listening port is {assign_port}')
                    try:
                        self.set_peers(self.port, s, self.port)
                        self.set_port(assign_port)
                        t3 = threading.Thread(target=self.listening, args=[assign_port])
                        t3.start()
                    except:
                        print(f'Thread failed to start!!!')
                else:
                    print(msg)
    # ============================================================================== #
    def receiving_tmp(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(1)
        while True:
            msg = s.recv(1024).decode('utf-8')
            if len(msg) > 0:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                return msg
        return None
    # ============================================================================== #

node = Node(host, int(port))
if is_first:
    t1 = threading.Thread(target=node.listening)
    t1.start()
else:
    t2 = threading.Thread(target=node.receiving)
    t2.start()    
        
from simulator import *
import random

# Shared state
token_holder = [None]              # Who currently holds the token
hosts_registry = {}                # Map node_id to Host instance
waiting_hosts = set()              # Hosts that have requested CS

class Host(Node):
    def __init__(self, sim, node_id, name=''):
        super().__init__(sim, node_id, name)
        self.host_id = node_id
        self.has_token = False
        self.waiting = False
        self.next_node_id = node_id % 10 + 1  # Next host in the ring (1-10)
        hosts_registry[self.host_id] = self

    def receive_message(self, frm, message, time):
        # if recieve TOKEN message the host now has the token
        if message.mtype == 'TOKEN':
            self.has_token = True
            token_holder[0] = self.host_id
            if self.waiting:
                self.enter_CS()
            else:
                # Not waiting, pass token immediately
                print(f'{self.sim.time:5} :: Host {self.host_id:2} received token and passes it to next host without entering CS')
                self.exit_CS()

    def enter_CS(self):
        if self.waiting == False:
            print(f'{self.sim.time:5} :: Host {self.host_id:2} wants to enter CS*****')
            # waiting for the token/entry to CS
            self.waiting = True
            # add to waiting hosts
            waiting_hosts.add(self.host_id)
        if self.has_token and self.waiting:
            print(f'{self.sim.time:5} :: Host {self.host_id:2} has token and enters CS++++')
            self.sim.call_after(random.randint(10, 20), self.exit_CS)

    def exit_CS(self):
        print(f'{self.sim.time:5} :: Host {self.host_id:2} exits CS----')
        self.has_token = False
        self.waiting = False
        waiting_hosts.discard(self.host_id)

        # if there are other hosts waiting, pass the token
        if waiting_hosts:
            # Pass to next node in sequence
            next_host = hosts_registry[self.next_node_id]
            msg = Message(1001, self, next_host, 'TOKEN', None)
            self.send_message(next_host, msg)
            print(f'{self.sim.time:5} :: Host {self.host_id:2} passed token to Host {next_host.host_id}')
        # if no more hosts waiting, end simulation
        else:
            print(f'{self.sim.time:5} :: No more hosts waiting - ending simulation')
            return
        
if __name__ == '__main__':
    sim = Simulator(debug=False, random_seed=1224)
    
    # Create 10 hosts and let them try to enter CS in some random time
    for i in range(10):
        host = Host(sim, i + 1)
        print(f'{sim.time:5} :: Host {host.host_id:2} is created')
        if i == 0:
            # The first host gets the token at the start
            host.has_token = True
            # Assign the token_holder to current holder
            token_holder[0] = host.host_id
            print(f'{sim.time:5} :: Host {host.host_id:2} starts with the token')
        sim.call_after(sim.rng.randint(10, 200), host.enter_CS)

    # Starts the simulation and runs forever; well, technically until all events are done
    sim.run()
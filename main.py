import sys
import random
import heapq
from collections import deque
import numpy as np

    

class Request:
    def __init__(self, time, event_type, server=None):
        self.time = time
        self.event_type = event_type
        self.chosenServer = server

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time
    
class Server:
    def __init__(self, id, queue_size, service_rate):
        self.serverID = id
        self.maxQueueSize = queue_size
        self.serverServiceRate = service_rate
        self.queue = deque()
        self.is_busy = False
    


class Simulator:
    def __init__(self, T, N, P, arrival_rate, Q, mu):
        self.Timeout = T
        self.NumberOfServers = N
        self.ServersProbabilites = P
        self.SimulatorArrivalRate = arrival_rate
        self.servers = [Server(i, Q[i], mu[i]) for i in range(N)]
        self.event_queue = []
        self.current_time = 0
        self.requests_served = 0
        self.requests_dropped = 0
        self.total_wait_time = 0
        self.total_service_time = 0

    def run(self):
        self.schedule_arrival(0)
        
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            
            if event.event_type == "arrival":
                self.handle_arrival()
            elif event.event_type == "departure":
                self.handle_departure(event.chosenServer)
            
            if self.current_time >= self.Timeout:
                break
        
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            if event.event_type == "departure":
                self.current_time = event.time
                self.handle_departure(event.chosenServer)

    def schedule_arrival(self, time):
        if time < self.Timeout:
            next_arrival = time + random.expovariate(self.SimulatorArrivalRate)
            heapq.heappush(self.event_queue, Request(next_arrival, "arrival"))

    def handle_arrival(self):
        server = self.select_server()
        if server.is_busy:
            if len(server.queue) < server.maxQueueSize:
                server.queue.append(self.current_time)
            else:
                self.requests_dropped += 1
        else:
            server.is_busy = True
            service_time =  random.expovariate(server.serverServiceRate)
            heapq.heappush(self.event_queue, Request(self.current_time + service_time, "departure", server))
            self.total_service_time += service_time
        
        self.schedule_arrival(self.current_time)

    def handle_departure(self, server):
        self.requests_served += 1
        if server.queue:
            wait_time = self.current_time - server.queue.popleft()
            self.total_wait_time += wait_time
            service_time = random.expovariate(server.serverServiceRate)
            heapq.heappush(self.event_queue, Request(self.current_time + service_time, "departure", server))
            self.total_service_time += service_time
        else:
            server.is_busy = False

    def select_server(self):
        r = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(self.ServersProbabilites):
            cumulative_prob += prob
            if r <= cumulative_prob:
                return self.servers[i]

    def get_results(self):
        total_requests = self.requests_served + self.requests_dropped
        avg_wait_time = self.total_wait_time / self.requests_served if self.requests_served > 0 else 0
        avg_service_time = self.total_service_time / self.requests_served if self.requests_served > 0 else 0
        return (self.requests_served, self.requests_dropped, self.current_time, avg_wait_time, avg_service_time)

def main():
    if len(sys.argv) < 7:
        print("Usage: python simulator.py T N P1 P2 ... PN lambda Q1 Q2 ... QN mu1 mu2 ... muN")
        sys.exit(1)

    T = float(sys.argv[1])
    N = int(sys.argv[2])
    P = [float(x) for x in sys.argv[3:3+N]]
    arrival_rate = float(sys.argv[3+N])
    Q = [int(x) for x in sys.argv[4+N:4+2*N]]
    mu = [float(x) for x in sys.argv[4+2*N:]]

    simulator = Simulator(T, N, P, arrival_rate, Q, mu)
    
    simulator.run()
    results = simulator.get_results()
    
    print(" ".join(map(str, results)))

if __name__ == "__main__":
    main()
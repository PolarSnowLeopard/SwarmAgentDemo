from swarm.repl import run_demo_loop
from agents import microservices_agent

if __name__ == "__main__":
    run_demo_loop(microservices_agent, stream=True)
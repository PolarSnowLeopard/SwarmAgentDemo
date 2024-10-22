from swarm.repl import run_demo_loop
from agents import assistant_agent

if __name__ == "__main__":
    run_demo_loop(assistant_agent, stream=True)

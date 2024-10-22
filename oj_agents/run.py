from swarm.repl import run_demo_loop
from agents import oj_agent

if __name__ == "__main__":
    run_demo_loop(oj_agent, stream=True)

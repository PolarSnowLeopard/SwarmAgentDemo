from swarm.repl import run_demo_loop
from autonomous_agent import microservices_agent
from cooperate_agents import assistant_agent

if __name__ == "__main__":
    # autonomous agent
    # run_demo_loop(microservices_agent, stream=True, debug=False)

    # cooperate agents
    run_demo_loop(assistant_agent, stream=True, debug=False)
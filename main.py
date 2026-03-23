from time import sleep
from tetr_env import Env
from tetris_agent import TetrisPlayer


def main():
    agent = TetrisPlayer(cost_strategy='min_height')
    env = Env()

    # Piezas iniciales.
    percept = env.act_and_sense([], last_n=5)
    act = agent.compute(percept)
    sleep(3)    # Suponiendo que se inicia justo cuando comienza el contador.

    # Caso especial tras primera pieza.
    percept = env.act_and_sense(act, last_n=2)
    act = agent.compute(percept)

    # Ciclo general: Solo última pieza.
    while act:  # len(act) > 0
        percept = env.act_and_sense(act)
        act = agent.compute(percept)
        print(agent._state)     ##### DEBUG #####
    print(f"¡El agente {agent.__class__.__name__} se ha detenido!")

    ### TODO: Tomar captura del score final ###


if __name__ == "__main__":
    main()

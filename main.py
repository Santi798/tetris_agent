from time import sleep
from tetr_env import Env
from tetris_agent import TetrisPlayer
from tetris_agent2 import TetrisPlayer2


N_IMAGES = 8
TETRIS_PLAYER = TetrisPlayer2

FILL_R_COST = 'fill_rows'
MIN_H_COST = 'min_height'


def main():
    agent = TETRIS_PLAYER(cost_strategy=FILL_R_COST)
    env = Env(n_images=N_IMAGES)

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
    print(f"¡El agente {agent.__class__.__name__} se ha detenido!")

    # Mostrar puntaje final
    env.show_score(n_images=N_IMAGES//2)



if __name__ == "__main__":
    main()

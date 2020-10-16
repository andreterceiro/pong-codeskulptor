import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
largura = 600
altura = 400
raio_da_bola = 10
largura_pad = 8
altura_pad = 80
metade_altura_pad = altura_pad / 2

posicao_bola = [largura / 2, altura / 2]
velocidade_bola = [0, 0]
posicao_paddle1 = float(altura / 2)
posicao_paddle2 = float(altura / 2)
paddle1_velocidade = 0.0
paddle2_velocidade = 0.0
placar1 = 0
placar2 = 0

def iniciar_bola(direita):
    global posicao_bola, velocidade_bola

    posicao_bola = [largura / 2, altura / 2]

    if direita:
        velocidade_bola = [random.randrange (120, 240) // 60, -random.randrange (60, 180) // 60]
    else:
        velocidade_bola = [-random.randrange (120, 240) // 60, -random.randrange (60, 180) // 60]

def new_game():
    global posicao_paddle1, posicao_paddle2, paddle1_velocidade, paddle2_velocidade, placar1, placar2

    placar1 = 0
    placar2 = 0

    posicao_paddle1 = float(altura / 2)
    posicao_paddle2 = float(altura / 2)
    paddle1_velocidade = 0.0
    paddle2_velocidade = 0.0

    if not random.randint(0, 1):
        lado_inicio = False
    else:
        lado_inicio = True

    iniciar_bola(lado_inicio)

# event handlers
def draw(c):
    global placar1, placar2, posicao_paddle1, posicao_paddle2, posicao_bola, velocidade_bola

    # os paddle devem ficar no campo e sua posição vertical deve ser atualizada
    posicao_paddle1 += paddle1_velocidade
    if posicao_paddle1 - metade_altura_pad < 0:
        posicao_paddle1 = metade_altura_pad
    if posicao_paddle1 + metade_altura_pad > altura:
        posicao_paddle1 = altura - metade_altura_pad

    # desenhando o campo
    c.draw_polygon([(0, 0), (largura, 0), (largura, altura), (0, altura)], 1, "Green", "Green")

    posicao_paddle2 += paddle2_velocidade
    if posicao_paddle2 - metade_altura_pad < 0:
        posicao_paddle2 = metade_altura_pad
    if posicao_paddle2 + metade_altura_pad > altura:
        posicao_paddle2 = altura - metade_altura_pad

    # desenhando os extremos e a linha do meio
    c.draw_line([largura / 2, 0],[largura / 2, altura], 1, "Blue")
    c.draw_line([largura_pad, 0],[largura_pad, altura], 1, "Blue")
    c.draw_line([largura - largura_pad, 0],[largura - largura_pad, altura], 1, "Blue")

    # desenhando os gols
    c.draw_polygon([(0                    , altura / 4), (largura_pad          , altura / 4),(largura_pad, altura - (altura / 4)) , (0,       altura - (altura / 4))], 1, "Violet", "Violet")
    c.draw_polygon([(largura - largura_pad, altura / 4), (largura, altura / 4)              ,(largura, altura - (altura / 4))     , (largura - largura_pad, altura - (altura / 4))], 1, "Violet", "Violet")

    # desenhando os paddles
    c.draw_polygon([(0, posicao_paddle1 - metade_altura_pad), (largura_pad, posicao_paddle1 - metade_altura_pad),
                    (largura_pad, posicao_paddle1 + metade_altura_pad), (0, posicao_paddle1 + metade_altura_pad)],
                1, "Red", "Grey")

    c.draw_polygon([(largura - largura_pad, posicao_paddle2 - metade_altura_pad), (largura, posicao_paddle2 - metade_altura_pad),
                    (largura, posicao_paddle2 + metade_altura_pad), (largura - largura_pad, posicao_paddle2 + metade_altura_pad)],
                1, "Red", "Grey")

    # atualiza a posição da bola
    # verificando se a bola bateu no topo
    if posicao_bola[1] <= raio_da_bola or posicao_bola[1] >= altura - raio_da_bola:
        velocidade_bola[1] *= -1

    # posicao_bola[1] -> de 9.8 a 391,06
    # posicao_paddle1 -> de 40 a 359
    # altura_pad -> 80
    # verificando o gol de um lado

    if posicao_bola[0] <= raio_da_bola + largura_pad:
        if (posicao_bola[1] > altura / 4 and posicao_bola[1] < (altura - altura/4)):
            if ((posicao_bola[1] > altura / 4) and (posicao_bola[1] < (altura - altura / 4))):
                if ( posicao_bola[1] > (posicao_paddle1 - altura_pad + metade_altura_pad) ):
                    if ( posicao_bola[1] < (posicao_paddle1 - metade_altura_pad) ):
                        placar2 += 1
                        iniciar_bola(False)
        else:
            # invertendo a posição horizontal da bola e aumentando a velocidade
            velocidade_bola[0] *= -1.05
            velocidade_bola[1] *= 1.05

    # verificando o gol do outro
    if posicao_bola[0] >= (largura - 1) - largura_pad - raio_da_bola:
        if (posicao_bola[1] > altura / 4 and posicao_bola[1] < (altura - altura/4)):
            if ((posicao_bola[1] > altura / 4) and (posicao_bola[1] < (altura - altura / 4))):
                if ( posicao_bola[1] > (posicao_paddle1 - altura_pad + metade_altura_pad) ):
                    if ( posicao_bola[1] < (posicao_paddle1 - metade_altura_pad) ):
                        placar1 += 1
                        iniciar_bola(True)
        else:
            # invertendo a posição horizontal da bola e aumentando a velocidade
            velocidade_bola[0] *= -1.1
            velocidade_bola[1] *= 1.1

    posicao_bola[0] += velocidade_bola[0]
    posicao_bola[1] += velocidade_bola[1]

    # desenhando a bola e o placar
    c.draw_circle(posicao_bola, raio_da_bola, 1, "Yellow", "Yellow")

    c.draw_text(str(placar1), (largura / 4 - 10, 50), 40, "Pink")
    c.draw_text(str(placar2), (largura / 4 * 3 - 10, 50), 40, "Pink")

def keydown(key):
    global paddle1_velocidade, paddle2_velocidade
    if key == simplegui.KEY_MAP['q']:
        paddle1_velocidade = -12

    if key == simplegui.KEY_MAP['a']:
        paddle1_velocidade = 12

    if key == simplegui.KEY_MAP['up']:
        paddle2_velocidade = -12

    if key == simplegui.KEY_MAP['down']:
        paddle2_velocidade = 12

def keyup(key):
    global paddle1_velocidade, paddle2_velocidade
    if key == simplegui.KEY_MAP['q']:
        paddle1_velocidade = 0
    elif key == simplegui.KEY_MAP['a']:
        paddle1_velocidade = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_velocidade = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_velocidade = 0

# Criando o frame e inciando
frame = simplegui.create_frame("", largura, altura)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reiniciar o jogo", new_game, 200)
frame.start()
new_game()
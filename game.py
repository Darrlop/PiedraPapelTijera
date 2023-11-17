from enum import Enum
from os import system  # para borrar/limpiar el terminal
from colorama import init, Fore, Back, Style  # para modificar estilo de fondo y letras

# Uso de clase Enum en vez de constantes para definir esto
# EL profe le llama UserChoice a la clase 
class UserChoice(Enum):
    INVALID_CHOICE = -1
    PAPER = 0
    ROCK = 1
    SCISSORS = 2
    QUIT = 3
# Accediendo a los miembros del Enum
# print(Option.PAPER)  # Salida: Opcion.PAPER <- el enum en sí
# print(Option.PAPER.name)  # Salida: PAPER <- sólo el nombre
# print(Option.PAPER.value)  # Salida: 0 <- sólo el valor asociado

traducciones = {"PAPER" : "Papel", "ROCK" : "Piedra", "SCISSORS" : "Tijeras"}


def dibujar_cabecera()->None:
    ''' Dibuja las cabeceras del juego'''

    print(Fore.LIGHTBLUE_EX)
    print("======================================")
    print("========== HARRI, ORRI, AR! ==========")
    print("======================================")
    print(Fore.RESET)
    
    print("-----------------------")
    print(Fore.CYAN + "Selecciona una opción:" + Fore.RESET)
    print("-----------------------")
    print()



def adornar(user_choice, comp_choice):
    '''
    Devuelve la frase adecuada para ilustrar una magna victoria o una triste derrota
    por medio de una matriz de frases conectoras en base a la matriz de jugadas

                PA  RO   SCI
                0    1    2
        PA  0 ["0", "v", "x"] 
        PI  1 ["x", "0", "v"] 
        SCI 2 ["v", "x", "0"]
    
    '''
    tabla_frases = [[" contra ", " envuelve a ", " es cortado por "], 
                    [" es envuelta por ", " contra ", " rompe a "], 
                    [" cortan a ", " son rotas por ", " contra "]]
    
    return tabla_frases[user_choice.value][comp_choice.value]


def read_user_choice()->UserChoice:
    '''
    Imprime un menú presentando las opciones de jugada y recoge la elección del usuario
    mediante una llamada a `input`. Devuelve la elección realizada.
    '''
    user_choice = UserChoice.INVALID_CHOICE

    while user_choice == UserChoice.INVALID_CHOICE:
        
        print(f"Papel:\t\t{Fore.CYAN}{UserChoice.PAPER.value}{Fore.RESET}")
        print(f"Piedra: \t{Fore.CYAN}{UserChoice.ROCK.value}{Fore.RESET}")
        print(f"Tijeras: \t{Fore.CYAN}{UserChoice.SCISSORS.value}{Fore.RESET}")
        print(f"{Style.DIM}\n[Salir del juego: {UserChoice.QUIT.value}]{Style.NORMAL}")

        try:
            # como voy a ir comparando user_choice con elementos de UserChoice, he de 
            # convertirlo a int pero luego a UserChoice
            print(Back.CYAN)
            user_choice = UserChoice(int(input("Elige una opción: ")))
            print(Back.RESET)
        except ValueError as error:  # El dato introducido no puede reconvertirse a int
            print(Style.RESET_ALL)
            print(f"Error de introducción {error}")
            print()
            user_choice = UserChoice.INVALID_CHOICE
    
    return user_choice


def is_exit(game_choice: UserChoice)->bool:
    '''
    Predicado que recibe la respuesta del usuario y devuelve `True` si 
    elige la opción de abandonar el juego
    '''
    return game_choice == UserChoice.QUIT


def generate_computer_choice()->UserChoice:
    '''
    Genera una jugada aleatoria para el ordenador, que podrá ser piedra, papel o tijera
    usamos "from random import choice" para usar choice y elegir al azar una opción de la lista
    '''
    from random import choice  # Hacemps aquí el import porque sólo va a ser usado en este ámbito 

    return choice([UserChoice.PAPER, UserChoice.ROCK, UserChoice.SCISSORS])   
    

def evaluate_move(user_choice, comp_choice)->str:
    '''
    Recibe 2 jugadas y las compara a fin de determinar cual ha ganado en base a la siguiente
    matriz de reglas (0 empate, v victoria, x derrota) y siempre desde el punto de vista
    del jugador humano (filas) contra el computador (columnas):
    
                PA  RO   SCI
                0    1    2
        PA  0 ["0", "v", "x"] 
        PI  1 ["x", "0", "v"] 
        SCI 2 ["v", "x", "0"]
    '''
    jugada = ""
    tabla_reglas = [["0", "v", "x"], 
                    ["x", "0", "v"], 
                    ["v", "x", "0"]]
    
    jugada = tabla_reglas[user_choice.value][comp_choice.value]    
    return jugada


def print_result(result: str, user_choice: UserChoice, comp_choice: UserChoice)->None:
    '''
    Recibe el resultado (0,v,x), así cómo las jugadas del humano y el computador.
    Presenta visualmente el resultado. No retorna nada.
    '''
    print()
    print (f"Has jugado {traducciones[user_choice.name]} y el computador {traducciones[comp_choice.name]}")
    print (traducciones[user_choice.name] + adornar(user_choice, comp_choice) + traducciones[comp_choice.name] + ":")
    print()
    if result == "0":
        print(Fore.BLUE + "¡Habéis EMPATADO!" + Fore.RESET)
    elif result == "v":
        print(Fore.GREEN + "¡¡¡Has GANADO!!!" + Fore.RESET)
    elif result == "x":
        print(Fore.RED + "Has PERDIDO miserablemente..." + Fore.RESET)


def game_loop()->None:
    ''' Inicia el juego, manteniendo el bucle principal del mismo hasta que se decide terminar'''
    
    # Limpia de pantalla e inicio de colorama
    #system('cls')
    init()

    while True:
        system('cls')
        # Inicializo colorama y muestro cabecera 
        dibujar_cabecera()
        # Recojo la selección del usuario jugador (piedra-papel-tijera ó salir del juego)
        user_choice = read_user_choice()
        # Siempre y cuando no quiera salir
        if not is_exit(user_choice):
            # Genero una jugada del ordenador
            comp_choice = generate_computer_choice()
            # Evalúo la jugada
            result = evaluate_move(user_choice, comp_choice)
            # Muestro el ganador y retornamos al inicio del bucle
            print_result(result, user_choice, comp_choice)
            input(Style.DIM+"\n<Pulsa Enter para continuar>"+Style.NORMAL)
            # Borro pantalla
            system('cls')
        else:
            # Salimos
            break
    print (Back.RED + "<<Fin del Programa>>" + Back.RESET)




# If para asegurarnos que se ejecute sólo cuando se ejecuta como programa principal y no por import
if __name__ == "__main__":
    #Este try except captura errores que no se han capturado antes y acaban llegando al "main" del programa.
    try:
        game_loop()
    except Exception as error:
        #log_error(error) # <- supuestamente esto es una func que envía el error a Sentry o similar. Ahora uso print
        print(f"Excepción capturada en main/game_loop: {error}")
    finally:
        print(Style.RESET_ALL)



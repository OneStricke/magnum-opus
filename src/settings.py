import pygame_menu
import src.constants as const


def sett(screen):
    def play():
        try:
            const.G = float(grav_input.get_value())
            const.min_astr_mass, const.max_astr_mass = astr_input.get_value()
        except ValueError:
            pass
        menu.disable()

    menu = pygame_menu.Menu('Welcome', 400, 300,
                            theme=pygame_menu.themes.THEME_BLUE)

    grav_input = menu.add.text_input('Grav Const :', default=str(const.G),
                                     valid_chars=['0', '1', '2', '3', '4',
                                                  '5', '6', '7', '8',
                                                  '9', 'e', '-', '.'])

    astr_input = menu.add.range_slider('Pick a range',
                                       (1, 100), (1, 100), 1,
                                       value_format=lambda x: str(int(x)))

    menu.add.button('Play', play)

    menu.mainloop(screen)

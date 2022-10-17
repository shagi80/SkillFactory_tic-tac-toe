from random import randint

MODE_ONE_PLAYER = 1
MODE_TWO_PLAEYER = 2
SM_CROSS = "X"
SM_ZERO = "O"
DIFFICULTY_LEVEL_EASY = 1
DIFFICULTY_LEVEL_NORMAL = 2
DIFFICULTY_LEVEL_HARD = 3

game_mode = 0
difficulty_level = 0
numbers = [str(i) for i in range(9)]
game_area = numbers.copy()


def input_command(help_text, data_type=None, data_max=None):
    result = None
    while not result:
        string = input(help_text)
        if string.upper() == 'СТОП':
            quit()
        if data_type:
            if data_type == 'int' and string.isdigit() and data_max >= int(string) >= 1:
                result = int(string)
            if data_type == 'coordinate':
                result_list = list(string.split())
                if (len(result_list) == 2 and result_list[0].isdigit() and result_list[1].isdigit()
                        and 2 >= int(result_list[0]) >= 0 and 2 >= int(result_list[1]) >= 0):
                    result = list(map(int, result_list))
        else:
            result = string
        if not result:
            print('Ваш выбор непонятен, попробуйте еще раз.')
    return result


def print_game_area():
    print('\n  0 1 2')
    for y in range(3):
        print(y, ' '.join(list(map(lambda symbol: '-' if symbol in numbers else symbol, game_area[y * 3:y * 3 + 3]))))


# Перевод введенных координат а индекс списка (нужно было запихнуть в input_command, но поздно)
def ind_by_coordinate(coordinate):
    return coordinate[0] * 3 + coordinate[1]


# Все возможные вариаеты победы для текущей ситуации
def get_victory_lines():
    result = []
    for i in range(3):
        result.append(''.join(game_area[i*3:i*3+3]))
        result.append(''.join([game_area[i], game_area[i+3], game_area[i+6]]))
    result.append(''.join([game_area[0], game_area[4], game_area[8]]))
    result.append(''.join([game_area[2], game_area[4], game_area[6]]))
    return result


# Проверка победы символа
def check_win(symbol):
    lines = get_victory_lines()
    for line in lines:
        if line == symbol*3:
            return True
    return False


# Получение списка пустых индексов
def get_empty_field(area):
    return list(filter(lambda sm: sm in numbers, area))


# Случайный ход rjvgm.nthf
def get_random_index(area):
    fields = get_empty_field(area)
    if fields:
        return int(fields[randint(0, len(fields) - 1)])
    return -1


# Проверка возможности победы следующим ходом
def get_victory_field(symbol):
    lines = get_victory_lines()
    for line in lines:
        if line.count(symbol) == 2:
            field = get_empty_field(line)
            if field:
                return int(field[0])
    return -1


# Выбор хода на основании последнего хода игрока
def get_cpu_logic(human_last):
    # сначала пытаемся занять дальний от последнего хода игрока угол
    clockwise = [0, 1, 2, 5, 8, 7, 6, 3]
    index = clockwise.index(human_last)
    if human_last%2 == 0:
        index += 4
    else:
        index += 3
    if index > 7:
        index -= 7
    empty_fields = get_empty_field(game_area)
    if str(clockwise[index]) in empty_fields:
        return clockwise[index]
    # Если дальний угол занят занимаем первый свободный угол
    else:
        for index in ['0', '2', '8', '6']:
            if index in empty_fields:
                return int(index)
        # Если все углы заняты занимаем первую свободную клетку
        else:
            for index in ['1', '3', '5', '7']:
                if index in empty_fields:
                    return int(index)
    return -1


# Тело программы
print('\nКРЕСТИКИ-НОЛИКИ')
print('_' * 20)
print('Для выхоа из игры на любой вопрос компьютера ответьте "стоп".')

# Устанавилваем режим игры "игрок против компьютера" или "два игрока"
while not game_mode:
    print('\nВыберите режим игры:')
    print('1 - игрок против компрьютера')
    print('2 - два игрока')
    game_mode = input_command('Ваш выбор: ', 'int', 2)

# Устанавливаем уровень сложности при игре против компьютера
if game_mode == MODE_ONE_PLAYER:
    print('\nВыберите уповень сложности:')
    print('1 - простой (все ходы компьютера случайны)')
    print('2 - нормальный (компьютер выигрывает, когда победа очевидно и не дает победить, когда очевидна',
          'победа игрока)')
    print('3 - сложный (у компьютера есть стратегия, начиная "крестиками" он не проигрывает)')
    difficulty_level = input_command('Ваш выбор: ', 'int', 3)

# Запрашиваем имена игроков, определяем игровые символы для игроков
if game_mode == MODE_ONE_PLAYER:
    player_one_name = input_command('\nВведите свое имя: ').capitalize()
    player_second_name = 'Компьютер'
    print(f'\n{player_one_name}, выберите фигуру:')
    print('1 - крестики')
    print('2 - нолики')
    command = input_command('Ваш выбор: ', 'int', 2)
    if command == 1:
        player_one_symbol, player_second_symbol = SM_CROSS, SM_ZERO
    else:
        player_one_symbol, player_second_symbol = SM_ZERO, SM_CROSS
else:
    player_one_name = input_command('\nИгрок, играющий за "крестики", введите свое имя: ').capitalize()
    player_one_symbol = 'X'
    player_second_name = input_command('\nИгрок, играющий за "нолики", введите свое имя: ').capitalize()
    player_second_symbol = 'O'
print(f'\nХорошо, {player_one_name} играет "{player_one_symbol}",',
      f'{player_second_name} играет "{player_second_symbol}".')

# Главный игровой цикл
while True:
    print('\nНачали. Координаты каждого своего очередного хода вводите как "номер строки - пробел - номер столбца".')
    print('"Крестики" ходят первыми.')

    # Если игрок играет с компьютером и компьютер играет "крестиками" компьютер делает первый ход
    if game_mode == MODE_ONE_PLAYER and player_second_symbol == SM_CROSS:
        if difficulty_level == DIFFICULTY_LEVEL_HARD:
            # На уровне сложности HARD компьютер ходит в середину
            game_area[4] = player_second_symbol
        else:
            # На уровнях сложности EASY и NORMAL компьютер ходит в случайнуюю клетку
            ind = get_random_index(game_area)
            game_area[ind] = player_second_symbol
    print_game_area()

    # Цикл текущей игры
    while True:

        # Ход первого игрока - это всегда человек
        index = ind_by_coordinate(input_command(f'\n{player_one_name}, ваш ход: ', 'coordinate'))
        empty_field = get_empty_field(game_area)
        if not game_area[index] in empty_field:
            print('\nЭта клетка уже занята !')
            continue
        game_area[index] = player_one_symbol
        last_human_step = index # Это нужно запомнить дла стратегии компрьютера
        # Печатаем игровое поле и проверяем завершение игры первым игроком
        print_game_area()
        if check_win(player_one_symbol):
            print(f'\nИгра окончана ! {player_one_name} победил!')
            break
        if not get_empty_field(game_area):
            print(f'\nИгра окончана ! Ничья! Победила дружба !')
            break

        # Ход второго игрока зависит от режима игры - или это компрьютер или человек
        if game_mode == MODE_TWO_PLAEYER:
            # Если второй игрок человек
            index = ind_by_coordinate(input_command(f'\n{player_second_name}, ваш ход: ', 'coordinate'))
            if not game_area[index] in empty_field:
                print('\nЭта клетка уже занята !')
                continue
            game_area[index] = player_second_symbol
        else:

            # Если второй игрок компьютер
            if difficulty_level == DIFFICULTY_LEVEL_EASY:
                # На уровен сложности EASY все ходы компьютера случайны
                ind = get_random_index(game_area)
                if ind != -1:
                    game_area[ind] = player_second_symbol
                else:
                    print(f'{player_second_symbol} не нашел вариантов для хода и пропускает ход.')
                    continue
            elif difficulty_level == DIFFICULTY_LEVEL_NORMAL:
                # На уровен сложности NORNAL компьютер имеет зачатки логики
                # Во-первых компьютер выигрывает если для выигрыша остался один ход
                ind = get_victory_field(player_second_symbol)
                if ind != -1:
                    game_area[ind] = player_second_symbol
                else:
                    # Во-вторых комрьютер не дает человеку выиграть если человек в одном шакге от победы
                    ind = get_victory_field(player_one_symbol)
                    if ind != -1:
                        game_area[ind] = player_second_symbol
                    else:
                        # Остальные ходы случайны
                        ind = get_random_index(game_area)
                        if ind != -1:
                            game_area[ind] = player_second_symbol
                        else:
                            print(f'{player_second_symbol} не нашел вариантов для хода и пропускает ход.')
                            continue
            else:
                # На уровен сложности HARD компьютер имеет зачатки логики
                # Если вдруг середина не занята компьютер занимает середну
                if game_area[4].isdigit():
                    game_area[4] = player_second_symbol
                else:
                    # Как и на уровне NORMAl компьютер пытается выиграть ближайшим ходом
                    ind = get_victory_field(player_second_symbol)
                    if ind != -1:
                        game_area[ind] = player_second_symbol
                    else:
                        # Как и на уровне NORMAL компьютер пытается не дать выиграть игроку
                        ind = get_victory_field(player_one_symbol)
                        if ind != -1:
                            game_area[ind] = player_second_symbol
                        else:
                            # Если первым ходом человек занял середину - занимаем угол
                            if last_human_step == 4:
                                game_area[0] = player_second_symbol
                            else:
                                # Все остальные ходы компрьютера случайны
                                ind = get_cpu_logic(last_human_step)
                                if ind != -1:
                                    print('res=', ind)
                                    game_area[ind] = player_second_symbol
                                else:
                                    print(f'{player_second_symbol}  не нашел вариантов для хода и пропускает ход.')
                                    continue

        # Печатаем игровое поле и проверяем завершение игры вторым игроком
        print(f'\n {player_second_name} сделал ход:')
        print_game_area()
        if check_win(player_second_symbol):
            print(f'\nИгра окончана ! {player_second_name} победил!')
            break
        if not get_empty_field(game_area):
            print(f'\nИгра окончана ! Ничья! Победила дружба !')
            break

    # Eсли игра завершена предлагаем попробовать еще раз
    print('\n')
    print('1 - играть снова')
    print('2 - выйти из игры')
    command = input_command('Ваш выбор: ', 'int', 2)
    if command == 1:
        game_area = numbers.copy()
    else:
        break

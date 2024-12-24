class Cube:
    def __init__(self, values):
        self.values = values  # Состояния в виде списка (0, 1 или '-' для не определенных)
        
    def __repr__(self):
        return ''.join(str(v) for v in self.values)
    
    def combine(self, other):
        """Combine if differs by exactly one bit."""
        diff = [i for i in range(len(self.values)) if self.values[i] != other.values[i]]
        if len(diff) == 1:
            new_values = self.values.copy()
            new_values[diff[0]] = '-'  # Используем '-' для обозначения не определенного значения
            return Cube(new_values)
        return None

def minimize(partially_defined, num_vars):
    # Шаг 1: Разделяем значения на 1 и 0
    ones = [Cube(list(format(i, f'0{num_vars}b'))) for i in range(len(partially_defined)) if partially_defined[i] == 1]
    zeros = [Cube(list(format(i, f'0{num_vars}b'))) for i in range(len(partially_defined)) if partially_defined[i] == 0]
    
    # Шаг 2: Генерация начального списка кусочков (квертов)
    prime_implicants = ones.copy()
    
    # Шаг 3: Сжатие до простых импликантов
    while True:
        new_prime_implicants = []
        combined = set()
        used = set()

        for i in range(len(prime_implicants)):
            for j in range(i + 1, len(prime_implicants)):
                combined_cube = prime_implicants[i].combine(prime_implicants[j])
                if combined_cube:
                    combined.add(tuple(combined_cube.values))
                    used.add(tuple(prime_implicants[i].values))
                    used.add(tuple(prime_implicants[j].values))
                    new_prime_implicants.append(combined_cube)

        # Добавляем непросмотренные кверты
        for pi in prime_implicants:
            if tuple(pi.values) not in used:
                new_prime_implicants.append(pi)

        prime_implicants = new_prime_implicants

        if not combined:
            break

    # Возвращаем простые импликанты
    return prime_implicants
   

def make_to_word(words:list[str],alf_N:list[str])->list[str]:
    un_bar = '\u0305'  
    result = []
    for word in words:
        r = ''
        for i,w in enumerate(word):
            if w == '1':
                r+=alf_N[i]
            elif w == '0': 
                r+=un_bar+alf_N[i]
        result.append(r)
    return result

# Пример частично определенной функции F = (1110**01)
N = 'xyz'
partially_defined = '111***01'
if 2**len(N) == len(partially_defined) and partially_defined.count('1') > 1 and partially_defined.count('0') > 0:
    # Получаем минимальные кверты
    prime_implicants = minimize(list(map(int, list(partially_defined.replace('*','1')))), len(N))

    minimal_dnf_result = list(map(str,prime_implicants))

    print(f"Минимальная ДНФ для частично определенной функции F = ({partially_defined}) в виде интервалов:")
    print(make_to_word(list(set(minimal_dnf_result)),list(N)))
else:
    print('Ошибка ввода')
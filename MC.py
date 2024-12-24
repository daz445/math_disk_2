from itertools import combinations

class QuineMcCluskey:
    def __init__(self, minterms, num_vars):
        self.minterms = minterms  # Список минимальных (истинных) значений
        self.num_vars = num_vars    # Количество переменных
        self.prime_implicants = []  # Список простых импликантов

    def _binary(self, num):
        """Конвертировать число в двоичное представление."""
        return format(num, f'0{self.num_vars}b')

    def _group_minterms(self):
        """Группировать минтермы по количеству единиц."""
        groups = {}
        for minterm in self.minterms:
            count = self._binary(minterm).count('1')
            if count not in groups:
                groups[count] = []
            groups[count].append(self._binary(minterm))
        return groups

    def _combine(self, group1, group2):
        """Объединить два группы минтермов, которые отличаются только одним битом."""
        new_group = []
        paired = []  # Для отслеживания пар
        for m1 in group1:
            for m2 in group2:
                diff = sum(1 for a, b in zip(m1, m2) if a != b)
                if diff == 1:
                    paired.append((m1, m2))
                    new_group.append(self._replace_diff(m1, m2))
        return new_group, paired

    def _replace_diff(self, m1, m2):
        """Заменить различающийся бит на '-'. """
        return ''.join(a if a == b else '-' for a, b in zip(m1, m2))

    def _find_prime_implicants(self, groups):
        """Находите простые импликанты."""
        new_groups = []
        marked = set()
        
        while groups:
            new_group = []
            for i in range(len(groups) - 1):
                combined, pairs = self._combine(groups[i], groups[i + 1])
                if combined:
                    new_group.extend(combined)
                    for m1, m2 in pairs:
                        marked.add(m1)
                        marked.add(m2)
            new_groups.append(new_group)
            groups = new_groups[-1]  # Новый список групп минтермов

        # Определение простых импликантов
        all_implicants = [implicant for group in new_groups for implicant in group]
        self.prime_implicants = [implicant for implicant in all_implicants if implicant not in marked]

    def get_prime_implicants(self):
        """Получить сокращенную ДНФ (простые импликанты) по алгоритму Квайна-Макласки."""
        groups = self._group_minterms()
        group_list = [groups[i] for i in sorted(groups)]
        self._find_prime_implicants(group_list)

    def display_primes(self):
        """Вывод простых импликантов."""
        return self.prime_implicants

# Пример использования
minterms = [0, 1, 2, 5, 6]  # Минки: 000, 001, 010, 101, 110 (например)
num_vars = 3                 # Количество переменных

qm = QuineMcCluskey(minterms, num_vars)
qm.get_prime_implicants()
result = qm.display_primes()
print("Сокращенная ДНФ (СДНФ):", result)

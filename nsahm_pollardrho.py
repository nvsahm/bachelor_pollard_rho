import random
import multiprocessing

generator = 0
modulo_value = 0
start_x = 0
subsets = []
group = []


def clean_number_input():
    while 1:
        try:
            ret = int(input())
            return ret
        except ValueError:
            print("Input was not a Number, try again")
            continue


def get_inputs():
    global generator
    global modulo_value
    print("Enter Generator")
    generator = clean_number_input()
    print("Enter modulo_value")
    modulo_value = clean_number_input()


def get_manual():
    global group
    print("Do you want to enter u ,v manual? Type Yes or No.")
    man = input().lower()
    while 1:
        if man == "yes":
            while 1:
                print("Enter u")
                u = clean_number_input()
                print("Enter v")
                v = clean_number_input()
                if u in group and v in group:
                    multiple = 1
                    break
                print("u, v must be from the following group:")
                print(group)
            break
        elif man == "no":
            u = random.sample(group, 1)[0]
            v = random.sample(group, 1)[0]
            print("How many Runs do you want to run? (With changing u, v values)")
            multiple = clean_number_input()
            break
        print(f"Your Input {man} was not expected. Please Type Yes or No")
        man = input()
    auto = False
    if multiple > 1:
        auto = get_auto()
    return u, v, multiple, auto


def get_auto():
    print("Do you want to run in multiprocessing mode? Uses a lot of computing power and calculate all cases. Type Yes or No.")
    man = input().lower()
    while 1:
        if man == "yes":
            return True
        elif man == "no":
            return False
        print(f"Your Input {man} was not expected. Please Type Yes or No")
        man = input()


def get_x_manual():
    global group
    print("Do you want to enter x manual? Type Yes or No.")
    man = input().lower()
    while 1:
        if man == "yes":
            while 1:
                print("Enter x")
                x = clean_number_input()
                if x in group:
                    break
                print("x must be from the following group:")
                print(group)
            break
        elif man == "no":
            x = random.sample(group, 1)[0]
            break
        print(f"Your Input {man} was not expected. Please Type Yes or No")
        man = input()
    return x


def generate_sub_group(j, rj, local_generator, local_modulo_value, return_dict):
    global group
    l = []
    for i in rj:
        print(i)
        l.append(((local_generator ** i) % local_modulo_value))
    return_dict[j] = l


def generate_group():
    global generator
    global modulo_value
    local_modulo_value = modulo_value
    local_generator = generator
    flag = False
    if local_modulo_value > 1:
        for i in range(2, local_modulo_value):
            if (local_modulo_value % i) == 0:
                flag = True
                break
    if not flag:
        return list(range(1, local_modulo_value))
    jobs = []
    g = []
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    r = split_list(range(1, local_modulo_value), 10)
    for j in range(10):
        proc = multiprocessing.Process(target=generate_sub_group,
                                       args=(j, r[j], local_generator, local_modulo_value, return_dict))
        jobs.append(proc)
        proc.start()
    for process in jobs:
        process.join()
    for i in range(10):
        g.extend(return_dict.values()[i])
    return g


def split_list(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def p(z, p_u, p_v, start_x_local, generator_local, modulo_value_local, group_local, subsets_local):
    if z in subsets_local[0]:
        z = start_x_local * z
        p_u = p_u + 1
    elif z in subsets_local[1]:
        z = z * z
        p_u = 2 * p_u
        p_v = 2 * p_v
    else:
        z = generator_local * z
        p_v = p_v + 1
    z = z % modulo_value_local
    p_u = p_u % len(group_local)
    p_v = p_v % len(group_local)
    return z, p_u, p_v


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def failure_exception(w, sigma_u, tau_u, sigma_v, tau_v, y, line, generator_local, modulo_value_local, group_local, start_x_local):
    print("Trying the Exception Case")
    d = len(group_local) / w
    u = sigma_u - tau_u
    v = tau_v - sigma_v
    if (u / w) != 0:
        b = ((v / w) * ((u / w) ** -1)) % d
        for i in range(0, w):
            if (int(generator_local) ** int(int(b) + int(i) * int(d))) % modulo_value_local == start_x_local:
                return b + i * d,  line
    print("The Exception Case failed")
    return "Failure", "Failure"


def iterate(u, v, large_mode, start_x_local, generator_local, modulo_value_local, group_local, subsets_local):
    x = int((int(int(start_x_local) ** int(u)) * int(generator_local ** v) % modulo_value_local))
    y = x
    sigma_u = u
    sigma_v = v
    tau_u = u
    tau_v = v
    k = 0
    while 1:
        if not large_mode:
            print(f'{k}| x={x} y={y} sigma={sigma_u}t + {sigma_v} tau={tau_u}t + {tau_v}')
        if k != 0 and x == y:
            greatest_common_divisor = gcd(sigma_u - tau_u, len(group_local))
            print(f"The Greatest Common Divisor is {greatest_common_divisor}")
            if greatest_common_divisor != 1:
                return failure_exception(greatest_common_divisor, sigma_u, tau_u, sigma_v, tau_v, y, f'{k}| x={x} y={y} sigma={sigma_u}t + {sigma_v} tau={tau_u}t + {tau_v}', generator_local, modulo_value_local, group_local, start_x_local)
            if sigma_u - tau_u == 0:
                print("sigma_u - tau_u = 0")
                return "Failure", "Failure"
            a = ((tau_v - sigma_v) * ((sigma_u - tau_u) ** -1)) % len(group_local)
            if a == 0 or round(a) != a:
                return "Failure", "Failure"
            return int(a), f'{k}| x={x} y={y} sigma={sigma_u}t + {sigma_v} tau={tau_u}t + {tau_v}'
        x, sigma_u, sigma_v = p(x, sigma_u, sigma_v, start_x_local, generator_local, modulo_value_local, group_local,
                                subsets_local)
        y, tau_u, tau_v = p(
            *p(y, tau_u, tau_v, start_x_local, generator_local, modulo_value_local, group_local, subsets_local),
            start_x_local, generator_local, modulo_value_local, group_local, subsets_local)
        k += 1


def input_birthday():
    print("Please enter your Birthday in the following Format: YYYYMMDD. Example Date: 15.02.1999 Format: 19990215")
    birthday = clean_number_input()
    birthday_str = str(birthday)
    while 1:
        if len(birthday_str) == 8 and int(birthday_str[4:5]) <= 12 and int(birthday_str[6:7]) <= 31:
            return birthday
        print(f"Your Input {birthday} was not expected. Please Type in the correct Format and as a possible Date")
        birthday = clean_number_input()
        birthday_str = str(birthday)


def check_birthday_mode():
    global group
    global generator
    global modulo_value
    global start_x
    print("Do you want to enter the Birthday Mode? Type Yes or No")
    mode = input().lower()
    while 1:
        if mode == "yes":
            birthday_mode = True
            generator = 2
            modulo_value = 1000003
            birthday = input_birthday()
            n = 2 ^ 16 + 1
            m_a = birthday % n
            start_x = (m_a + ((birthday - m_a) / n)) % n
            break
        elif mode == "no":
            birthday_mode = False
            break
        print(f"Your Input {mode} was not expected. Please Type Yes or No")
        mode = input()
    return birthday_mode


def iterate_multiple(j, u, v, start_x_local, generator_local, modulo_value_local, group_local, subsets_local,
                     return_dict):
    a, line = iterate(u, v, True, start_x_local, generator_local, modulo_value_local, group_local, subsets_local)
    l = [a, line]
    return_dict[j] = l


def print_success(a, line):
    global start_x
    print(f"The result of the Pollard Rho method is {a}")
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    gen = str(generator).translate(sub)
    print(f"The successful line was: {line}")
    print(f"The complete formula is now: dlog{gen}({start_x}) = {a}")


def main():
    global generator
    global modulo_value
    global group
    global start_x
    birthday_mode = check_birthday_mode()
    if not birthday_mode:
        get_inputs()
    print("Generating Group. (This can take a while when using large Modulo Values which are no prime numbers")
    group = generate_group()
    print("Removing Duplicates")
    group = list(dict.fromkeys(group))
    print("Sorting List")
    group.sort()
    global subsets
    print("Creating Subsets")
    subsets = split_list(group, 3)
    if not birthday_mode:
        start_x = get_x_manual()
    u, v, multiple, auto = get_manual()
    if not auto:
        for i in range(1, multiple + 1):
            print(f"Calculating Run {i}/{multiple}")
            a, line = iterate(u, v, False, start_x, generator, modulo_value, group, subsets)
            if a == "Failure":
                print("The Pollard Rho algorithm could not find a solution for the given values.")
            else:
                print_success(a, line)
                break
            u = random.sample(group, 1)[0]
            v = random.sample(group, 1)[0]
    else:
        print(f"Calculating {multiple} Runs parallel")
        manager = multiprocessing.Manager()
        jobs = []
        return_dict = manager.dict()
        for j in range(multiple):
            u = random.sample(group, 1)[0]
            v = random.sample(group, 1)[0]
            proc = multiprocessing.Process(target=iterate_multiple, args=(j, u, v, start_x, generator, modulo_value, group, subsets, return_dict))
            jobs.append(proc)
            proc.start()
        for process in jobs:
            process.join()
        for i in range(multiple):
            if return_dict.values()[i][0] != "Failure":
                print_success(return_dict.values()[i][0], return_dict.values()[i][1])


if __name__ == '__main__':
    main()

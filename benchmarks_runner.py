def read_benchmark(content):
    lines = content.splitlines()
    name = lines[0]
    P = []
    N = []
    currently_positive = True
    for line in lines[1:]:
        print(P)
        if line == "++":
            currently_positive = True
        elif line == "--":
            currently_positive = False
        elif currently_positive:
            P.append(line)
        else:
            N.append(line)
    return name, P, N
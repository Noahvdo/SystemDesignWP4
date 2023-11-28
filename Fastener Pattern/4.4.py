def n_fasteners(x):
    #until we know how to iterate
    #with open("Checks\Results_Checks.txt", 'r') as file:
        #lines = file.readlines()

    #lines[0] = f"Number of Fasteners: {x}" + '\n'

    with open("Checks\Results_Checks.txt", 'w') as file:
        #file.writelines(lines)
        file.write(f"Number of Fasteners: {x}")
    return x


n_fasteners(10)






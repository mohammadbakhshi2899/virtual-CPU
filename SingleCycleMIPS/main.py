from CentralProcessingUnit_CPU import CPU

path_Code = "Code.txt"

if __name__ == '__main__':
    cpu = CPU()
    cpu.giveProgramToExcute(path_Code)
    cpu.start()



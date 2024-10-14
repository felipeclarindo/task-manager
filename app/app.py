from os import name, system
from .modules.operations.atualizar import _atualizar
from .modules.operations.remover import _remover
from .modules.operations.adicionar import _adicionar
from .modules.operations.visualizar import _visualizar


class App:
    def __init__(self) -> None:
        pass

    def clear(self) -> None:
        if name == "nt":
            system("cls")
        else:
            system("clear")

    def menu(self):
        self.clear()
        print("-" * 40)
        print("--------- Task Manager --------")
        print("-" * 40)
        print("1 - Adicionar Tarefa.")
        print("2 - Atualizar Tarefa.")
        print("3 - Remover Tarefa.")
        print("4 - Ver Tarefas")
        print("5 - Sair")

    def adicionar_tarefa(self):
        _adicionar()

    def run(self):
        sair = False
        while not sair:
            self.menu()
            option = str(input("Informe uma opção: "))
            match option:
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    saida_valida = False
                    while not saida_valida:
                        self.menu()

                case _:
                    print("Opção ínvalida.")

from main import create_model
import matplotlib.pyplot as plt

SIM_TIME = 10000

if __name__ == "__main__":
    for is_modified in [False, True]:
        for _ in range(4):
            model = create_model(modified=is_modified)
            model_response = model.simulate(SIM_TIME, {})
            plt.plot(list(range(100, SIM_TIME, 100)), model_response)
        plt.title(f'Значення відгуку моделі в залежності від часу моделювання (модифікована = {is_modified})')
        plt.show()

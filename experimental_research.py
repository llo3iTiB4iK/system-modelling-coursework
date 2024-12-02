from main import create_model
import scipy.stats


NUM_ITER = 20

if __name__ == "__main__":
    y_means = []
    residual_influence = 0
    for is_modified in [False, True]:
        result_dict = {}
        model_response = []
        for _ in range(NUM_ITER):
            model = create_model(modified=is_modified)
            model.simulate(5000, result_dict)
            model_response.append(result_dict["Середній час перебування клієнта в банку"])
        print(f"\n------------- Результати симуляції (модифікована модель = {is_modified}): -------------")
        model_response = [r if i == 0 else r - model_response[i-1] for i, r in enumerate(model_response)]
        print(f'Список значень відгуку: {model_response}')
        response_mean = result_dict["Середній час перебування клієнта в банку"] / NUM_ITER
        print(f'Середнє значення відгуку: {response_mean}')
        y_means.append(response_mean)
        residual_influence += sum((value-response_mean) ** 2 for value in model_response)

    y_mean = sum(y_means)/len(y_means)
    print(f'\n\ny_mean = {y_mean}')
    factor_influence = NUM_ITER * sum((y_i_mean-y_mean) ** 2 for y_i_mean in y_means)
    print(f'S_факт = {factor_influence}')
    print(f'S_залиш = {residual_influence}')
    factor_dispersion = factor_influence
    print(f'd_факт = {factor_dispersion}')
    residual_dispersion = residual_influence / (2 * (NUM_ITER-1))
    print(f'd_залиш = {residual_dispersion}')
    fisher_criterion_val = factor_dispersion / residual_dispersion
    print(f'F = {fisher_criterion_val}')
    fisher_critical_val = scipy.stats.f.ppf(q=1 - .05, dfn=1, dfd=2 * (NUM_ITER-1))
    print(f'F_кр = {fisher_critical_val}')

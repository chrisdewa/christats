from typing import Any
def quad(
        dists: dict[str, dict[str, Any]]
    ):
        


with pm.Model() as globe_model: # definimos el modelo 
    p = pm.Uniform('p', 0, 1, default_transform=None)
    # Default transform None es vital o los estimadores serán
    # para el espacio no transformado y no corresponden con el libro
    lk = pm.Binomial('likelihood', observed=W, n=N, p=p)
    mp = pm.find_MAP(bounds=[(1e-9, 1-1e-9)], progressbar=0)
    # Los límites son requeridos para que el estimador converja apropiadamente
    # debajo del capote utiliza scipy minimize.
    hess = pm.find_hessian(
        mp,
        negate_output=False
        # en la versión actual de pymc (5)
        # esto es necesario para evitar errores y advertencias, 
        # aunque la consecuencia es que el resultado es negativo.
    )

sd = (1/-hess[0,0])**0.5
# como el resultado es negativo, utilizamos el menos unario para 
# hacerlo positivo "-hess"
map_point = mp['p']
# Por fin la aproximación normal
lo, hi = stats.norm.ppf([0.055, 0.945], loc=map_point, scale=sd)

print('mean', 'std', '5.5%', '94.5%')
print('p', *np.array([map_point, sd, lo, hi]).round(2))
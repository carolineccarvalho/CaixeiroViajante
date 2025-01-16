import multiprocessing

def limite_de_tempo(func, args=(), timeout=1800):
    # try:
    #     # resultado["caminho"] = tatt(g)
    #     resultado["caminho"] = chris(g)
    # except Exception as e:
    #     resultado["erro"] = str(e)
    resultado = {"caminho": None, "erro": None, "timeout": False}
    def func_wrapper(queue, *args):
        try:
            resultado = func(*args)
            queue.put(resultado)
        except Exception as e:
            queue.put(e)
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=func_wrapper, args=(queue, *args))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        resultado["timeout"] = True
        resultado["erro"] = f"Tempo limite de {timeout}s excedido"
    else:
        process.close()
        if not queue.empty():
            res = queue.get()
            if isinstance(res, Exception):
                resultado["erro"] = str(res)
            else:
                resultado["caminho"] = res
    return resultado
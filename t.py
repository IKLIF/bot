import multiprocessing

def your_func(queue):
    # Your custom logic here
    result = 4
    queue.put(result)

if __name__ == 'main':
    result_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=your_func, args=(result_queue,))
    p.start()
    p.join(30)

    if p.is_alive():
        print("Kill it.")
        p.terminate()

    result = result_queue.get()
    print(f"Result from your_func(): {result}")

    # Retrieve the result from the queue






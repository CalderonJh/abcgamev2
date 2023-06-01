import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def get_info():
    return ancho, alto


if __name__ == '__main__':
    print(get_info())

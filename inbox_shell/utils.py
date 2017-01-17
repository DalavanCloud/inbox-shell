import hashlib


def checksum_file(file, algorithm=hashlib.md5):
    """Resumo do arquivo ``file``, em hexadecimal, usando ``algorithm``.
    A invocação dessa função altera o *offset* de ``file``. Caso esse
    comportamento seja indesejável, veja ``safe_checksum_file``.
    :param file: Objeto do tipo arquivo.
    :param algorithm: (opcional) Invocável que produz o algorítmo utilizado
                    na produção do hash. Ver: ``hashlib.algorithms_available``.
    """
    _algorith = algorithm()

    while True:
        chunk = file.read(1024)
        if not chunk:
            break

        _algorith.update(chunk)

    return _algorith.hexdigest()


def safe_checksum_file(file, algorithm=hashlib.md5):
    """Resumo do arquivo ``file``, em hexadecimal, usando ``algorithm``.
    A invocação dessa função *NÃO* altera o *offset* de ``file``.
    :param file: Objeto do tipo arquivo.
    :param algorithm: (opcional) Invocável que produz o algorítmo utilizado
                      na produção do hash. Ver: ``hashlib.algorithms_available``.
    """
    if not file.seekable():
        raise TypeError('Object "file" does not support random access.')

    former_offset = file.tell()
    try:
        return checksum_file(file, algorithm=algorithm)

    finally:
        file.seek(former_offset)

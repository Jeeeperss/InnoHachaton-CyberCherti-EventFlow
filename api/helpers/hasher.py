import bcrypt

def hash_password(raw_password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    
    :param raw_password: Исходный пароль в виде строки.
    :return: Хешированный пароль в виде строки или None, если пароль не передан.
    """
    if raw_password:  # Проверка, что пароль передан
        # Генерация соли и хеширование пароля
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')  # Возвращаем строку с хешем
    return None  # Возвращаем None, если пароль не был передан

def check_password(raw_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли переданный пароль с сохраненным хешированным паролем.
    
    :param raw_password: Исходный пароль в виде строки.
    :param hashed_password: Хешированный пароль, с которым нужно сравнить.
    :return: True, если пароли совпадают, иначе False. Если переданы некорректные данные, возвращается False.
    """
    if raw_password and hashed_password:  # Проверка, что оба параметра переданы
        # Сравнение пароля с хешем
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
    return False  # Возвращаем False, если переданы некорректные данные


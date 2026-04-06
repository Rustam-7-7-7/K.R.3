from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    try:
        # Попробуем прочитать с UTF-8
        with open(filename, 'r', encoding='utf-8') as f:
            parser.read_file(f)
    except (UnicodeDecodeError, FileNotFoundError):
        # Если UTF-8 не работает, попробуем системную кодировку
        parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename}')
    return db

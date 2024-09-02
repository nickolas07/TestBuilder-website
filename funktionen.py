import ast
import inspect
import tokenize
import uuid
import random
import importlib

import django

django.setup()
from aufgaben.models import Themen


def get_uuid(length: int = 8, implement: str = '') -> str:  # < 32 und % 2 == 0
    from tests.models import Erstellt
    uuid_list = []
    for _ in range(100):
        rand_num: int = random.randint(0, 32 - length)
        temp_uuid: str = str(uuid.uuid4()).replace('-', '')[rand_num:rand_num + length].upper()
        uuid_list.append(f'{temp_uuid[:len(temp_uuid) // 2]}-{temp_uuid[len(temp_uuid) // 2:]}')

    selected = random.choice(uuid_list)

    if not Erstellt.objects.filter(uuid=selected).exists():
        if implement:
            return f'{implement} {selected}'
        else:
            return selected
    else:
        return get_uuid(length, implement)


def get_aufgaben(themenbereich: str = None) -> list | None:
    if themenbereich is None:
        return None

    stufe = Themen.objects.get(name=themenbereich).stufe

    def sonderzeichen(text: str):
        text = text.replace('Ã¶', 'ö')
        text = text.replace('Ã¼', 'ü')
        text = text.replace('Ã¤', 'ä')
        text = text.replace('Ã–', 'Ö')
        text = text.replace('Ãœ', 'Ü')
        text = text.replace('Ã„', 'Ä')
        text = text.replace('ÃŸ', 'ß')
        return text

    def in_comments(nummer: int, comments: list) -> (bool, int):
        for i, comment in enumerate(comments):
            if nummer in comment:
                return True, i
            else:
                continue
        return False, i

    def tree(filename: str) -> list:
        with open(filename, 'r') as f:
            content = f.read()

        with open(filename, 'r') as f:
            comments = [(token.start[0], sonderzeichen(token.string.replace('# ', ''))) for token in
                        tokenize.generate_tokens(f.readline) if token.type == tokenize.COMMENT]

        output = []
        root = ast.parse(content)
        funktionen = [funktion for funktion in ast.walk(root) if isinstance(funktion, ast.FunctionDef)]

        for node in funktionen:
            has_comment = in_comments(node.lineno + 1, comments)
            if has_comment[0]:
                output.append((node.lineno, sonderzeichen(node.name), comments[has_comment[1]][1]))
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.If):
                    has_comment = in_comments(child.lineno + 1, comments)
                    if has_comment[0]:
                        output.append((child.lineno, 'if', comments[has_comment[1]][1]))
        return output

    try:
        module = importlib.import_module(f'skripteTests.Aufgaben.{stufe}_{themenbereich}')
    except ModuleNotFoundError as e:
        raise e
    file_path: str = inspect.getmodule(module).__file__
    comments = {}

    i = 1
    for ln, name, comment in tree(file_path):
        if name == 'if':
            comments[ln] = ['if', comment]
        else:
            comments[ln] = [str(i), name, comment]
            i += 1

    comments = sorted(comments.items())
    comments.append((1, [1, 2, 3]))
    new_comments = []
    temp_ifs = []
    for i, comment in enumerate(comments):
        comment = comment[1]
        if comment[0] != 'if':
            if i > 0:
                new_comments[-1].append(temp_ifs)
                temp_ifs = []
            new_comments.append([str(comment[0]), comment[1], comment[2]])
        else:
            temp_ifs.append([f'{new_comments[-1][1].split('_')[-1]}.{len(temp_ifs) + 1}', comment[1]])

    new_comments.pop(-1)
    new_comments = sorted(new_comments, key=lambda x: int(x[0]))
    return new_comments

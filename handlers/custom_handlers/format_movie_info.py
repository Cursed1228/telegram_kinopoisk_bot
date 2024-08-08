from typing import Tuple, Dict, List


def _format_movie_info(movie: dict) -> str | None:
    text = ''
    info_dict = dict()
    if movie['name']:
        text += f"*{movie['name']}*\n"
        info_dict['name'] = text
    else:
        return None

    if movie['description']:
        text += f"{movie['description']}\n"
    else:
        return None

    if movie['rating']['imdb']:
        text += f"Рейтинг imdb = {movie['rating']['imdb']}\n"
    if movie['year']:
        text += f"Год производства: {movie['year']}\n"
    if movie['genres']:
        genre_names = ', '.join(genre['name'] for genre in movie['genres'])
        text += f"Жанры: {genre_names}\n"
    if movie['ageRating'] is not None:
        text += f"Возрастной рейтинг: {movie['ageRating']}+\n"
    if movie['poster']['url']:
        text += f"{movie['poster']['url']}"

    return text


def _process_movie_results(result, limit: int) -> list[str]:
    movie_info_list = list()
    for i_limit in range(limit):
        try:
            movie_info = _format_movie_info(result['docs'][i_limit])
        except:
            movie_info = None

        if movie_info:
            movie_info_list.append(movie_info)

    return movie_info_list

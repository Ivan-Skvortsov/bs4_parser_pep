import re
import logging
from urllib.parse import urljoin
from collections import defaultdict

import requests_cache
from tqdm import tqdm
from bs4 import BeautifulSoup

from constants import BASE_DIR, MAIN_DOC_URL, MAIN_PEP_URL, EXPECTED_STATUS
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, features='lxml')

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)

        response = get_response(session, version_link)
        soup = BeautifulSoup(response.text, features='lxml')

        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')

        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, features='lxml')

    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')

    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, features='lxml')

    table_tag = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )

    download_url = urljoin(downloads_url, pdf_a4_tag.get('href'))
    filename = download_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    download_path = downloads_dir / filename

    response = session.get(download_url)
    with open(download_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив загружен: {download_path}')


def pep(session):
    response = get_response(session, MAIN_PEP_URL)
    soup = BeautifulSoup(response.text, features='lxml')

    section_tag = find_tag(
        soup, 'section', attrs={'id': 'numerical-index'}
    )
    table_body_tag = find_tag(section_tag, 'tbody')
    table_row_tags = find_tag(
        table_body_tag, 'tr', attrs={'class': re.compile(r'row-.+')}, many=True
    )
    unexpected_statuses = []
    statuses_count = defaultdict(int)
    for row in tqdm(table_row_tags):
        expected_pep_status = EXPECTED_STATUS.get(
            row.td.text[1:], ['Unknown status']
        )
        link = row.a.get('href')
        pep_url = urljoin(MAIN_PEP_URL, link)

        response = get_response(session, pep_url)
        soup = BeautifulSoup(response.text, features='lxml')

        dl_tag = find_tag(
            soup, 'dl', attrs={'class': 'rfc2822 field-list simple'}
        )
        try:
            status_row = dl_tag.find(string='Status').parent
            pep_status = status_row.find_next_sibling('dd').string
        except Exception as e:
            logging.warning(
                f'Не найден статус PEP в карточке: {pep_url}. Код ошибки: {e}'
            )
            pep_status = 'Unknown status'
        # pep_status преобразовываем в str чтобы не упасть в бесконечную
        # рекурсиию при использовании prettytable
        pep_status = str(pep_status)
        statuses_count[pep_status] += 1
        if pep_status not in expected_pep_status:
            unexpected_statuses.append(
                (pep_url, pep_status, expected_pep_status)
            )

    if unexpected_statuses is not None:
        logging.warning('Несовпадающие статусы:')
        for item in unexpected_statuses:
            logging.warning(item[0])
            logging.warning(f'Статус в карточе: {item[1]}')
            logging.warning(f'Ожидаемые статусы: {item[2]}')
    result = [('Статус', 'Количество')]
    result.extend(statuses_count.items())
    result.append(('Total', sum(statuses_count.values())))
    return result


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode

    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)

    logging.info('Пасер завершил работу.')


if __name__ == '__main__':
    main()

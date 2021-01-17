# SPECIAL THANKS TO THE py3-pinterest open-source module's maintainers!
import json
import requests
from requests.structures import CaseInsensitiveDict
from urllib.parse import urlencode, quote_plus

AGENT_STRING = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) " \
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

BOARDS_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardsResource/get/'

GET_BOARD_SECTION_PINS = 'https://www.pinterest.com/resource/BoardSectionPinsResource/get/'

GET_BOARD_SECTIONS = 'https://www.pinterest.com/resource/BoardSectionsResource/get/'

HOME_PAGE = 'https://www.pinterest.com/'

USER_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserResource/get/'


class Pinterest:
    def __init__(self, username=''):
        self.username = username
        self.bookmark_manager = BookmarkManager()
        self.http = requests.session()
        self.sources = {}

    def build_get(self, url, options, source_url='/', context=None):
        data = self.url_encode({
            'source_url': source_url,
            'data': json.dumps({
                'options': options,
                "context": context
            })
        })
        url = '{}?{}'.format(url, data)
        return url

    def get_user_boards(self, username=None, page_size=50, archived=False):
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(primary='boards', secondary=username)
        options = {
            "page_size": page_size,
            "sort": "custom",
            "username": username,
            "include_archived": archived,
            "group_by": "visibility",
            "field_set_key": "profile_grid_item",
            "bookmarks": [next_bookmark],
        }
        url = self.build_get(url=BOARDS_RESOURCE, options=options, source_url='/{}/boards/'.format(username))
        result = self.get(session=self.http, url=url).json()
        bookmark = result['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='boards', secondary=username, bookmark=bookmark)

        return result['resource_response']['data']

    def get_board_sections(self, board_id='', reset_bookmark=False):
        """
        Obtains a list of all sections of a board
        """
        next_bookmark = self.bookmark_manager.get_bookmark(primary='board_sections', secondary=board_id)
        if next_bookmark == '-end-':
            if reset_bookmark:
                self.bookmark_manager.reset_bookmark(primary='board_sections', secondary=board_id)
            return []

        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark]
        }

        url = self.build_get(url=GET_BOARD_SECTIONS, options=options)
        result = self.get(session=self.http, url=url).json()
        bookmark = result['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='board_sections', secondary=board_id, bookmark=bookmark)

        return result['resource_response']['data']

    def get_section_pins(self, section_id='', page_size=250, reset_bookmark=False):
        next_bookmark = self.bookmark_manager.get_bookmark(primary='section_pins', secondary=section_id)
        if next_bookmark == '-end-':
            if reset_bookmark:
                self.bookmark_manager.reset_bookmark(primary='section_pins', secondary=section_id)
            return []

        options = {
            "isPrefetch": False,
            "field_set_key": "react_grid_pin",
            "is_own_profile_pins": True,
            "page_size": page_size,
            "redux_normalize_feed": True,
            "section_id": section_id,
            "bookmarks": [next_bookmark]
        }

        url = self.build_get(url=GET_BOARD_SECTION_PINS, options=options)
        result = self.get(session=self.http, url=url).json()
        bookmark = result['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='section_pins', secondary=section_id, bookmark=bookmark)

        pins = [d for d in result['resource_response']['data'] if 'pinner' in d]
        return pins

    def get_user_overview(self, username=None):
        """
        :param username target username, if left blank current user is assumed
        :return python dict describing the pinterest user profile response
        """
        if username is None:
            raise ValueError('No username has been founded')

        options = {
            "isPrefetch": 'false',
            "username": username,
            "field_set_key": "profile"
        }
        url = self.build_get(url=USER_RESOURCE, options=options)
        result = self.get(session=self.http, url=url).json()
        print(url)

        return result['resource_response']['data']

    @staticmethod
    def request(session, method, url):
        headers = CaseInsensitiveDict([
            ('Referer', HOME_PAGE),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Accept', 'application/json'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')])

        response = session.request(method, url, headers=headers)
        response.raise_for_status()

        return response

    @staticmethod
    def get(session, url):
        return session.request('GET', url=url)

    @staticmethod
    def url_encode(query):
        if isinstance(query, str):
            query = quote_plus(query)
        else:
            query = urlencode(query)
        query = query.replace('+', '%20')
        return query


class BookmarkManager:
    def __init__(self):
        self.bookmark_map = {}

    def add_bookmark(self, primary, bookmark, secondary=None):
        if primary not in self.bookmark_map:
            self.bookmark_map[primary] = {}
        if secondary is not None:
            self.bookmark_map[primary][secondary] = bookmark
        else:
            self.bookmark_map[primary] = bookmark

    def get_bookmark(self, primary, secondary=None):
        try:
            if secondary is not None:
                return self.bookmark_map[primary][secondary]
            else:
                return self.bookmark_map[primary]
        except KeyError:
            pass
        return None

    def reset_bookmark(self, primary, secondary=None):
        if primary in self.bookmark_map:
            del self.bookmark_map[primary][secondary]
        else:
            pass

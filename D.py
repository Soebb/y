# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from .vk import VKIE
from ..compat import compat_b64decode

from ..utils import (
    int_or_none,
    js_to_json,
    get_elements_by_class,
    parse_count,
    parse_duration,
    try_get,
    unified_timestamp,
)



class DaftsexIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?daftsex\.com/watch/(?P<id>-?\d+_\d+)'
    _TESTS = [{
        'url': 'https://daftsex.com/watch/-156601359_456242791',
        'info_dict': {
            'id': '-156601359_456242791',
            'ext': 'mp4',
            'title': 'Skye Blue - Dinner And A Show',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        globParams = self._parse_json(self._search_regex(
            r'<script id="globParams">.*window.globParams = ([^;]+);[^<]+</script>',
            embed_page, 'Global Parameters', flags=re.DOTALL), video_id, transform_source=js_to_json)

        if 'credentials' in globParams['video']:

            title = self._search_regex(
                r'<meta.*itemprop ?= ?"name".*content ?= ?"([^"]+)".*/>',
                webpage, 'Title', default='Empty Title', fatal=False)

            uploadDate = self._search_regex(
                r'<meta.*itemprop ?= ?"uploadDate".*content ?= ?"([^"]+)".*/?>',
                webpage, 'Upload Date', fatal=False)

            timestamp = unified_timestamp(uploadDate)

            description = self._search_regex(
                r'<meta.*itemprop ?= ?"description".*content ?= ?"([^"]+)".*/>',
                webpage, 'Description', fatal=False)

            globalEmbed_url = self._search_regex(
                r'<script.+?window.globEmbedUrl = \'((?:https?:)?//(?:daxab\.com|dxb\.to|[^/]+/player)/[^\']+)\'.*?></script>',
                webpage, 'global Embed url', flags=re.DOTALL)

            hash = self._search_regex(
                r'<script id="data-embed-video.+?hash: "([^"]+)"[^<]*</script>',
                webpage, 'Hash', flags=re.DOTALL)

            embed_url = globalEmbed_url + hash

            if VKIE.suitable(embed_url):
                return self.url_result(embed_url, VKIE.ie_key(), video_id)

            embed_page = self._download_webpage(
                embed_url, video_id, 'Downloading embed webpage', headers={'Referer': url})

            hostName = compat_b64decode(globParams['server'][::-1]).decode()
            server = 'https://%s/method/video.get/' % hostName

            item = self._download_json(
                f'{server}{video_id}', video_id,
                headers={'Referer': url}, query={
                    'token': globParams['video']['access_token'],
                    'videos': video_id,
                    'ckey': globParams['c_key'],
                    'credentials': globParams['video']['credentials'],
                })['response']['items'][0]

            formats = []
            for f_id, f_url in item.get('files', {}).items():
                if f_id == 'external':
                    return self.url_result(f_url)
                ext, height = f_id.split('_')
                if globParams['video']['partial']['quality']['height'] is not None:
                    formats.append({
                        'format_id': f'{height}p',
                        'url': f'https://{hostName}/{f_url[8:]}&videos={video_id}&extra_key={globParams["video"]["partial"]["quality"][height]}',
                        'height': int_or_none(height),
                        'ext': ext,
                    })
            self._sort_formats(formats)

            thumbnails = []
            for k, v in item.items():
                if k.startswith('photo_') and v:
                    width = k.replace('photo_', '')
                    thumbnails.append({
                        'id': width,
                        'url': v,
                        'width': int_or_none(width),
                    })

            return {
                'id': video_id,
                'title': title,
                'formats': formats,
                'comment_count': int_or_none(item.get('comments')),
                'description': description,
                'duration': int_or_none(item.get('duration')),
                'thumbnails': thumbnails,
                'timestamp': timestamp,
                'view_count': int_or_none(item.get('views')),
            }

# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_b64decode
from ..utils import (
    get_elements_by_class,
    int_or_none,
    js_to_json,
    parse_count,
    parse_duration,
    try_get,
)


class DaftsexIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?daftsex\.com/watch/(?P<id>-?\d+_\d+)'
    _TESTS = [{
        'url': 'https://daftsex.com/watch/-156601359_456242791',
        'info_dict': {
            'id': '-156601359_456242791',
            'ext': 'mp4',
            'title': 'Skye Blue - Dinner And A Show',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        title = get_elements_by_class('heading', webpage)[-1]
        duration = parse_duration(self._search_regex(
            r'Duration: ((?:[0-9]{2}:){0,2}[0-9]{2})',
            webpage, 'duration', fatal=False))
        views = parse_count(self._search_regex(
            r'Views: ([0-9 ]+)',
            webpage, 'views', fatal=False))

        player_hash = self._search_regex(
            r'DaxabPlayer\.Init\({[\s\S]*hash:\s*"([0-9a-zA-Z_\-]+)"[\s\S]*}',
            webpage, 'player hash')
        player_color = self._search_regex(
            r'DaxabPlayer\.Init\({[\s\S]*color:\s*"([0-9a-z]+)"[\s\S]*}',
            webpage, 'player color', fatal=False) or ''

        embed_page = self._download_webpage(
            'https://daxab.com/player/%s?color=%s' % (player_hash, player_color),
            video_id, headers={'Referer': url})
        video_params = self._parse_json(
            self._search_regex(
                r'window\.globParams\s*=\s*({[\S\s]+})\s*;\s*<\/script>',
                embed_page, 'video parameters'),
            video_id, transform_source=js_to_json)

        server_domain = 'https://%s' % compat_b64decode(video_params['server'][::-1]).decode('utf-8')
        formats = []
        for format_id, format_data in video_params['video']['cdn_files'].items():
            ext, height = format_id.split('_')
            extra_quality_data = format_data.split('.')[-1]
            url = f'{server_domain}/videos/{video_id.replace("_", "/")}/{height}.mp4?extra={extra_quality_data}'
            formats.append({
                'format_id': format_id,
                'url': url,
                'height': int_or_none(height),
                'ext': ext,
            })
        self._sort_formats(formats)

        thumbnail = try_get(video_params,
                            lambda vi: 'https:' + compat_b64decode(vi['video']['thumb']).decode('utf-8'))

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'duration': duration,
            'thumbnail': thumbnail,
            'view_count': views,
            'age_limit': 18,
        }

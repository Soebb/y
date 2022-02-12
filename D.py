# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from .vk import VKIE
from ..compat import compat_b64decode

from ..utils import (
    int_or_none,
    js_to_json,
    unified_timestamp,
)
import re


class DaftsexIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?daftsex\.com/watch/(?P<id>-?\d+_\d+)'
    _TESTS = [{
        'url': 'https://daftsex.com/watch/-2000421746_85421746',
        'md5': 'ae6ef4f04d19ac84e4658046d02c151c',
        'info_dict': {
            'id': '-2000421746_85421746',
            'ext': 'mp4',
            'title': 'Forsaken By Hope Studio Clip',
            'description': 'Forsaken By Hope Studio Clip — Смотреть онлайн',
            'upload_date': '19700101',
            'timestamp': 0,
            'thumbnail': 'https://sun9-86.userapi.com/impf/7vN3ACwSTgChP96OdOfzFjUCzFR6ZglDQgWsIw/KPaACiVJJxM.jpg?size=800x450&quality=96&keep_aspect_ratio=1&background=000000&sign=b48ea459c4d33dbcba5e26d63574b1cb&type=video_thumb',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._search_regex(
            r'<meta.*itemprop ?= ?"name".*content ?= ?"([^"]+)".*/>',
            webpage, 'Title', default='Empty Title', fatal=False)
        self.write_debug('title: %s' % title)
        uploadDate = self._search_regex(
            r'<meta.*itemprop ?= ?"uploadDate".*content ?= ?"([^"]+)".*/?>',
            webpage, 'Upload Date', fatal=False)
        self.write_debug('Upload Date: %s' % uploadDate)
        timestamp = unified_timestamp(uploadDate)
        self.write_debug('timestamp: %s' % timestamp)
        description = self._search_regex(
            r'<meta.*itemprop ?= ?"description".*content ?= ?"([^"]+)".*/>',
            webpage, 'Description', fatal=False)
        self.write_debug('description: %s' % description)

        globalEmbed_url = self._search_regex(
            r'<script.+?window.globEmbedUrl = \'((?:https?:)?//(?:daxab\.com|dxb\.to|[^/]+/player)/[^\']+)\'.*?></script>',
            webpage, 'global Embed url', flags=re.DOTALL)
        hash = self._search_regex(
            r'<script id="data-embed-video.+?hash: "([^"]+)"[^<]*</script>',
            webpage, 'Hash', flags=re.DOTALL)

        embed_url = globalEmbed_url + hash
        self.write_debug('embed_url: %s' % embed_url)

        if VKIE.suitable(embed_url):
            return self.url_result(embed_url, VKIE.ie_key(), video_id)

        embed_page = self._download_webpage(
            embed_url, video_id, 'Downloading embed webpage', headers={'Referer': url})

        globParams = self._parse_json(self._search_regex(
            r'<script id="globParams">.*window.globParams = ([^;]+);[^<]+</script>',
            embed_page, 'Global Parameters', flags=re.DOTALL), video_id, transform_source=js_to_json)
        self.write_debug('globParams: %s' % globParams)
        hostName = compat_b64decode(globParams['server'][::-1]).decode()
        server = 'https://%s/method/video.get/' % hostName
        self.write_debug('server: %s' % server)

        item = self._download_json(
            server + video_id, video_id,
            headers={'Referer': url}, query={
                'token': globParams['video']['access_token'],
                'videos': video_id,
                'ckey': globParams['c_key'],
                #'credentials': globParams['video']['credentials'],
            })['response']['items'][0]

        formats = []
        for f_id, f_url in item.get('files', {}).items():
            if f_id == 'external':
                return self.url_result(f_url)
            ext, height = f_id.split('_')
            if globParams['video']['partial']['quality'].get(height) is not None:
                formats.append({
                    'format_id': height + 'p',
                    'url': f_url.replace('https://', 'https://%s/' % hostName) + '&videos=%s' % video_id + '&extra_key=%s' % globParams['video']['partial']['quality'][height],
                    'height': int_or_none(height),
                    'ext': ext,
                })
        self._sort_formats(formats)
        self.write_debug('formats: %s' % formats)

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

import requests
import uplink
from uplink_helper import raise_for_status
import datetime


@uplink.json
@raise_for_status
class BlogClient(uplink.Consumer):
    def __init__(self):
        super().__init__(base_url='http://consumer_services_api.talkpython.fm')

    @uplink.get('/api/blog')
    def all_entries(self) -> requests.models.Response:
        """ Get all blog entries from the server. """

    @uplink.get('/api/blog/{post_id}')
    def entry_by_id(self, post_id) -> requests.models.Response:
        """ Get single blog post details. """

    @uplink.post('/api/blog')
    def __create_new_entry(self, **kwargs: uplink.Body
                           ) -> requests.models.Response:
        """ Create a new post """

    def create_new_entry(self, title: str, content: str, views: int = 0,
                         published: str = None) -> requests.models.Response:
        if published is None:
            published = datetime.datetime.now().isoformat()

        # noinspection PytypeChecker
        return self.__create_new_entry(
            title=title,
            content=content,
            view_count=views,
            published=published
        )

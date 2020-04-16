from itertools import chain, islice

from usb.logging import logger
from usb.utils import formatted_episodes, msecs
from usb.search import Appsearch


class Document:
    def __init__(self, **kwargs):
        allowed_types = [str, int, list, float]

        self.__dict__.update(
            (key, value) for key, value in kwargs.items() if type(value) in allowed_types
        )

        self.timems = msecs(kwargs["start"], kwargs["end"])

    @property
    def id(self):
        return "{}-{}-{}-{}".format(
            self.title.lower(), self.season, formatted_episodes(self.episode), self.index
        )

    @property
    def data(self):
        return {"id": self.id, **vars(self)}

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.id)


class Subtitles:
    def __init__(self, video):
        self.video = video
        self.appsearch = Appsearch()

    @property
    def list(self):
        for subtitle in self.video.extract_subs():
            yield subtitle

    @property
    def documents(self):
        for subtitle in self.list:
            yield Document(
                **vars(self.video),
                **vars(subtitle),
                seconds_start=subtitle.start.total_seconds(),
                seconds_middle=(
                    (subtitle.start.total_seconds() + subtitle.end.total_seconds()) / 2
                ),
                seconds_end=subtitle.end.total_seconds()
            )

    @property
    def documents_chunked(self, chunksize=100):
        iterator = iter(self.documents)
        for first in iterator:
            yield chain([first], islice(iterator, chunksize - 1))

    def index(self, engine=None):
        if not engine:
            engine = self.video.title.lower()

        logger.debug("engine: {}", engine)

        for n, chunk in enumerate(self.documents_chunked):
            documents = self.appsearch.index_documents(engine, [i.data for i in list(chunk)])
            logger.debug("indexed {} chunk {} containing {}", str(self.video), n, len(documents))

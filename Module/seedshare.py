import textwrap


SEED_SPLITTER = '$'


class SharedSeed:

    def __init__(self, generator_version: str, seed_name: str, spoiler_log: bool, settings_string: str):
        self.generator_version = generator_version
        self.seed_name = seed_name
        self.spoiler_log = spoiler_log
        self.settings_string = settings_string

    def to_share_string(self) -> str:
        return SEED_SPLITTER.join([
            self.generator_version,
            self.seed_name,
            '1' if self.spoiler_log else '0',
            self.settings_string
        ])

    @classmethod
    def from_share_string(cls, local_generator_version: str, share_string: str):
        parts = share_string.split(SEED_SPLITTER)

        if len(parts) != 4:
            raise InvalidShareStringFormatException(textwrap.dedent(
                '''
                Unrecognized seed format.
                Make sure you are on the same seed generator version as the person who shared the seed with you.
                '''
            ))

        seed_generator_version = parts[0]
        if seed_generator_version != local_generator_version:
            raise IncompatibleShareStringVersionException(textwrap.dedent(
                '''
                Incompatible seed versions.
                Seed was generated from {0} and your version is {1}.
                Make sure you are on the same seed generator version as the person who shared the seed with you.
                '''.format(seed_generator_version, local_generator_version)
            ))

        return SharedSeed(
            generator_version=seed_generator_version,
            seed_name=parts[1],
            spoiler_log=True if parts[2] == '1' else False,
            settings_string=parts[3]
        )


class ShareStringException(Exception):

    def __init__(self, message):
        self.message = message


class InvalidShareStringFormatException(ShareStringException):

    def __init__(self, message):
        super().__init__(message)


class IncompatibleShareStringVersionException(ShareStringException):

    def __init__(self, message):
        super().__init__(message)

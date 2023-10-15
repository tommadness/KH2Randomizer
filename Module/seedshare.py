import textwrap


SEED_SPLITTER = '$'


def loop(int_val):
    if int_val==47:
        return 122
    if int_val==58:
        return 65
    if int_val==64:
        return 57
    if int_val==91:
        return 97
    if int_val==96:
        return 90
    if int_val==123:
        return 48
    return int_val
    

def transform(in_string,tourney_gen):
    if not tourney_gen:
        return in_string
    out_string = ""
    for i in range(len(in_string)):
        out_string+=chr(loop((ord(in_string[i])+1)))
    
    return out_string


def untransform(in_string,tourney_gen):
    if not tourney_gen:
        return in_string
    out_string = ""
    for i in range(len(in_string)):
        out_string+=chr(loop((ord(in_string[i])-1)))
    
    return out_string

class SharedSeed:

    def __init__(self, generator_version: str, seed_name: str, spoiler_log: bool, settings_string: str, tourney_gen: bool = False):
        self.generator_version = generator_version
        self.seed_name = seed_name
        self.spoiler_log = spoiler_log
        self.settings_string = settings_string
        self.tourney_gen = tourney_gen

    def to_share_string(self) -> str:
        transformed_string = transform(self.seed_name,self.tourney_gen)

        return SEED_SPLITTER.join([
            self.generator_version,
            '1' if self.tourney_gen else '0',
            transformed_string,
            '1' if self.spoiler_log else '0',
            self.settings_string
        ])

    @classmethod
    def from_share_string(cls, local_generator_version: str, share_string: str):
        parts = share_string.split(SEED_SPLITTER)

        if len(parts) != 5:
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

        tourney_gen = (parts[1] == '1')
        untransformed_string = untransform(parts[2],tourney_gen)

        return SharedSeed(
            generator_version=seed_generator_version,
            seed_name=untransformed_string,
            spoiler_log=True if parts[3] == '1' else False,
            settings_string=parts[4],
            tourney_gen=tourney_gen,
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

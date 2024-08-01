import os
import re
from typing import Any, Dict, Iterable, List, Optional

from dataclasses import dataclass

import jellyfish

# import jellyfish  # type: ignore

NUMR_RE = re.compile(r"^\d{2}$")
ABBR_RE = re.compile(r"^[a-zA-Z]{2}$")

FRANCOPHONE = bool(os.environ.get('FRANCOPHONE', False))

VIVE_LE_QUEBEC_LIBRE = bool(os.environ.get('VIVE_LE_QUEBEC_LIBRE', False))


_lookup_cache: Dict[str, "Province"] = {}


@dataclass
class Province:

    # Name in English
    name_en: str
    name_metaphone_en: str
    # Name in French
    name_fr: str
    name_metaphone_fr: str
    # Two letter alphabetic abbreviation
    abbr: str
    # English abbreviation
    abbr_en: str
    # French abbreviation
    abbr_fr: str
    # Numeric code
    nu_code: int
    # ISO Country-Region code
    iso_code: str
    is_territory: bool
    capital: Optional[str]
    capital_tz: Optional[str]
    time_zones: List[str]
    confederation_year: Optional[int]

    def __repr__(self) -> str:
        return f"<Province:{self.name}>"

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self.name_en if not FRANCOPHONE else self.name_fr

    @property
    def name_metaphone(self) -> str:
        return self.name_metaphone_en if not FRANCOPHONE else self.name_metaphone_fr


def lookup(query: str | int, field: Optional[str] = None, use_cache: bool = True) -> Optional[Province]:
    """Look up a Canadian province or territory using its two letter
    abbreviation, numeric code, or full name. When searching by name, matches
    will include fuzzy matches using metaphones.
    """

    if isinstance(query, str) and NUMR_RE.match(query):
        query = int(query)

    if isinstance(query, int):
        field = field or 'nu_code'

    if isinstance(query, str) and ABBR_RE.match(query):
        field = field or 'abbr'

    if field is None:
        field = 'name'

    def match(region):
        if field == 'name':
            return region.name.lower() == query.lower() or region.name_metaphone == jellyfish.metaphone(query)
        return getattr(region, field) == query

    try:
        return next(filter(match, PROVINCES_AND_TERRITORIES))
    except StopIteration:
        raise ValueError(f"Cannot find a province or territory identified by: {field}={query}")


def mapping(from_field: str, to_field: str, regions: Optional[Iterable[Province]] = None) -> Dict[Any, Any]:
    """Generate a mapping of Canadian regions, using the specified from and to fields"""
    if regions is None:
        regions = PROVINCES_AND_TERRITORIES
    return {getattr(s, from_field): getattr(s, to_field) for s in regions}


AB = Province(
    **{
        "name_en": "Alberta",
        "name_metaphone_en": "ALBRT",
        "name_fr": "Alberta",
        "name_metaphone_fr": "ALBRT",
        "abbr": "AB",
        "abbr_en": "Alta.",
        "abbr_fr": "Alb.",
        "nu_code": 48,
        "iso_code": "CA-AB",
        "is_territory": False,
        "capital": "Edmonton",
        "capital_tz": "America/Edmonton",
        "time_zones": ["America/Edmonton"],
        "confederation_year": 1905,
    }
)

BC = Province(
    **{
        "name_en": "British Columbia",
        "name_metaphone_en": "BRTX KLMB",
        "name_fr": "Colombie-Britannique",
        "name_metaphone_fr": "KLMBBRTNK",
        "abbr": "BC",
        "abbr_en": "B.C.",
        "abbr_fr": "C.-B.",
        "nu_code": 59,
        "iso_code": "CA-BC",
        "is_territory": False,
        "capital": "Victoria",
        "confederation_year": 1871,
        "capital_tz": "America/Vancouver",
        "time_zones": ["America/Edmonton", "America/Creston", "America/Dawson_Creek", "America/Fort_Nelson", "America/Vancouver"],
    }
)

MB = Province(
    **{
        "name_en": "Manitoba",
        "name_metaphone_en": "MNTB",
        "name_fr": "Manitoba",
        "name_metaphone_fr": "MNTB",
        "abbr": "MB",
        "abbr_en": "Man.",
        "abbr_fr": "Man.",
        "nu_code": 35,
        "iso_code": "CA-MB",
        "is_territory": False,
        "capital": "Winnipeg",
        "confederation_year": 1870,
        "capital_tz": "America/Winnipeg",
        "time_zones": ["America/Winnipeg"]
    }
)

NB = Province(
    **{
        "name_en": "New Brunswick",
        "name_metaphone_en": "N BRNSWK",
        "name_fr": "Nouveau-Brunswick",
        "name_metaphone_fr": "NFBRNSWK",
        "abbr": "NB",
        "abbr_en": "N.B.",
        "abbr_fr": "N.-B.",
        "nu_code": 13,
        "iso_code": "CA-NB",
        "is_territory": False,
        "capital": "Fredericton",
        "confederation_year": 1867,
        "capital_tz": "America/Moncton",
        "time_zones": ["America/Moncton"],
    }
)

NL = Province(
    **{
        "name_en": "Newfoundland and Labrador",
        "name_metaphone_en": "NFNTLNT ANT LBRTR",
        "name_fr": "Terre-Neuve-et-Labrador",
        "name_metaphone_fr": "TRNFTLBRTR",
        "abbr": "NL",
        "abbr_en": "N.L.",
        "abbr_fr": "T.-N.-L.",
        "nu_code": 10,
        "iso_code": "CA-NL",
        "is_territory": False,
        "capital": "St. John's",
        "confederation_year": 1949,
        "capital_tz": "America/St_Johns",
        "time_zones": ["America/St_Johns", "America/Goose_Bay"],
    }
)

NS = Province(
    **{
        "name_en": "Nova Scotia",
        "name_metaphone_en": "NF SKX",
        "name_fr": "Nouvelle-Écosse",
        "name_metaphone_fr": "NFLKS",
        "abbr": "NS",
        "abbr_en": "N.S.",
        "abbr_fr": "N.-É.",
        "nu_code": 12,
        "iso_code": "CA-NS",
        "is_territory": False,
        "capital": "Halifax",
        "confederation_year": 1867,
        "capital_tz": "America/Halifax",
        "time_zones": ["America/Halifax"],
    }
)

NT = Province(
    **{
        "name_en": "Northwest Territories",
        "name_metaphone_en": "NR0WST TRTRS",
        "name_fr": "Territoires du Nord-Ouest",
        "name_metaphone_fr": "TRTRS T NRTST",
        "abbr": "NT",
        "abbr_en": "N.W.T.",
        "abbr_fr": "T.N.-O.",
        "nu_code": 61,
        "iso_code": "CA-NT",
        "is_territory": True,
        "capital": "Yellowknife",
        "confederation_year": 1870,
        "capital_tz": "America/Yellowknife",
        "time_zones": ["America/Yellowknife", "America/Inuvik"],
    }
)

NU = Province(
    **{
        "name_en": "Nunavut",
        "name_metaphone_en": "NNFT",
        "name_fr": "Nunavut",
        "name_metaphone_fr": "NNFT",
        "abbr": "NU",
        "abbr_en": "Nvt.",
        "abbr_fr": "Nt",
        "nu_code": 62,
        "iso_code": "CA-NU",
        "is_territory": True,
        "capital": "Iqaluit",
        "confederation_year": 1999,
        "capital_tz": "America/Iqaluit",
        "time_zones": ["America/Iqaluit", "America/Resolute", "America/Atikokan", "America/Rankin_Inlet", "America/Pangnirtung", "America/Cambridge_Bay"],
    }
)

ON = Province(
    **{
        "name_en": "Ontario",
        "name_metaphone_en": "ONTR",
        "name_fr": "Ontario",
        "name_metaphone_fr": "ONTR",
        "abbr": "ON",
        "abbr_en": "Ont.",
        "abbr_fr": "Ont.",
        "nu_code": 35,
        "iso_code": "CA-ON",
        "is_territory": False,
        "capital": "Toronto",
        "confederation_year": 1867,
        "capital_tz": "America/Toronto",
        "time_zones": ["America/Toronto", "America/Winnipeg", "America/Atikokan", "America/Nipigon", "America/Thunder_Bay"],
    }
)

PE = Province(
    **{
        "name_en": "Prince Edward Island",
        "name_metaphone_en": "PRNS ETWRT ISLNT",
        "name_fr": "Île-du-Prince-Édouard",
        "name_metaphone_fr": "ILTPRNSTRT",
        "abbr": "PE",
        "abbr_en": "P.E.I.",
        "abbr_fr": "Î.-P.-É.",
        "nu_code": 11,
        "iso_code": "CA-PE",
        "is_territory": False,
        "capital": "Charlottetown",
        "confederation_year": 1873,
        "capital_tz": "America/Halifax",
        "time_zones": ["America/Halifax"],
    }
)

QC = Province(
    **{
        "name_en": "Quebec",
        "name_metaphone_en": "KBK",
        "name_fr": "Québec",
        "name_metaphone_fr": "KBK",
        "abbr": "QC",
        "abbr_en": "Que.",
        "abbr_fr": "Qc",
        "nu_code": 24,
        "iso_code": "CA-QC",
        "is_territory": False,
        "capital": "Quebec City",
        "confederation_year": 1867,
        "capital_tz": "America/Montreal",
        "time_zones": ["America/Montreal", "America/Blanc-Sablon"],
    }
)

SK = Province(
    **{
        "name_en": "Saskatchewan",
        "name_metaphone_en": "SSKXWN",
        "name_fr": "Saskatchewan",
        "name_metaphone_fr": "SSKXWN",
        "abbr": "SK",
        "abbr_en": "Sask.",
        "abbr_fr": "Sask.",
        "nu_code": 47,
        "iso_code": "CA-SK",
        "is_territory": False,
        "capital": "Regina",
        "confederation_year": 1905,
        "capital_tz": "America/Regina",
        "time_zones": ["America/Regina", "America/Swift_Current", "America/Edmonton"],
    }
)

YT = Province(
    **{
        "name_en": "Yukon",
        "name_metaphone_en": "YKN",
        "name_fr": "Yukon",
        "name_metaphone_fr": "YKN",
        "abbr": "YT",
        "abbr_en": "Y.T.",
        "abbr_fr": "Yn",
        "nu_code": 60,
        "iso_code": "CA-YT",
        "is_territory": True,
        "capital": "Whitehorse",
        "confederation_year": 1898,
        "capital_tz": "America/Whitehorse",
        "time_zones": ["America/Whitehorse", "America/Dawson"],
    }
)


PROVINCES = [AB, BC, MB, NB, NL, NS, ON, PE, QC, SK]

if VIVE_LE_QUEBEC_LIBRE:
    PROVINCES.pop(PROVINCES.index(QC))

TERRITORIES = [NT, NU, YT]

PROVINCES_AND_TERRITORIES = PROVINCES + TERRITORIES

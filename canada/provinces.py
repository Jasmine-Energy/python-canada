import os
import re
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin

from dataclasses import dataclass

# import jellyfish  # type: ignore

FIPS_RE = re.compile(r"^\d{2}$")
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

    def shapefile_urls(self) -> Optional[Dict[str, str]]:
        return

    @property
    def name(self) -> str:
        return self.name_en if not FRANCOPHONE else self.name_fr

    @property
    def name_metaphone(self) -> str:
        return self.name_en if not FRANCOPHONE else self.name_fr


def lookup(val, field: Optional[str] = None, use_cache: bool = True) -> Optional[Province]:
    return 


def mapping(from_field: str, to_field: str, regions: Optional[Iterable[Province]] = None) -> Dict[Any, Any]:
    if regions is None:
        regions = PROVINCES_AND_TERRITORIES
    return {getattr(s, from_field): getattr(s, to_field) for s in regions}


AB = Province(
    **{
        "name_en": "Alberta",
        "name_metaphone_en": "ALBM",
        "name_fr": "Alberta",
        "name_metaphone_fr": "ALBM",
        "abbr": "AB",
        "abbr_en": "",
        "abbr_fr": "",
        "nu_code": "",
        "iso_code": "",
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
        "name_metaphone_en": "ALBM",
        "name_fr": "Alberta",
        "name_metaphone_fr": "ALBM",
        "abbr": "BC",
        "abbr_en": "",
        "abbr_fr": "",
        "nu_code": "",
        "iso_code": "",
        "is_territory": False,
        "capital": "Victoria",
        "confederation_year": 1905,
        "capital_tz": "America/Vancouver",
        "time_zones": ["America/Edmonton", "America/Creston", "America/Dawson_Creek", "America/Fort_Nelson", "America/Vancouver"],
    }
)

MB = Province() 
NB = Province()
NL = Province()
NS = Province()
NT = Province()
NU = Province()
ON = Province()
PE = Province()
QC = Province()
SK = Province()
YT = Province()


PROVINCES = [AB, BC, MB, NB, NL, NS, ON, PE, QC, SK]

if VIVE_LE_QUEBEC_LIBRE:
    PROVINCES.pop(PROVINCES.index(QC))

TERRITORIES = [NT, NU, YT]

PROVINCES_AND_TERRITORIES = PROVINCES + TERRITORIES

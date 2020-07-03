# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

import invenio_logging.config
import invenio_theme.config
from invenio_indexer.api import RecordIndexer
from invenio_records_rest.facets import terms_filter
from invenio_records_rest.utils import allow_all, check_elasticsearch, deny_all

from ..file_management.api import FILE_MNGT_PID_FETCHER, \
    FILE_MNGT_PID_MINTER, FILE_MNGT_PID_TYPE, RevisionSearch
from .search import RevisionedRecordsSearch


def _(x):
    """Identity function for string extraction."""
    return x


invenio_logging.config.LOGGING_FS_LOGFILE = "/var/log/fare/log_fare.txt"
invenio_logging.config.LOGGING_FS_PYWARNINGS = True
invenio_theme.config.THEME_FOOTER_TEMPLATE = "fare/footer.html"

EDUCATION_LEVEL = {
  "educationLevel": [
                      "Divulgazione",
                      "Scuola Ospedaliera",
                      "Scuola Primaria",
                      "Scuola Secondaria di primo grado",
                      "Scuola Secondaria di secondo grado",
                      "Università"
  ]
}

SUBJECTS = {
  "subject": [
              "Arte",
              "Biologia",
              "Chimica",
              "Economia",
              "Elettronica",
              "Etica",
              "Fisica",
              "Geografia",
              "Informatica",
              "Lingue e letteratura",
              "Matematica",
              "Scienze",
              "Società",
              "Sociologia",
              "Storia"
  ]
}

ARGUMENTS = {
    "Matematica": [
        "Algebra",
        "Geometria analitica",
        "Analisi",
        "Fondamenti",
        "Combinatoria",
        "Probabilità",
        "Statistica"
    ],
    "Informatica": [
        "Hardware",
        "Software",
        "Programmazione",
        "Sicurezza",
        "Reti"
    ],
    "Scienze": [
        "Scienze naturali",
        "Scienze astronomiche"
    ],
    "Lingue e letteratura": [
        "Italiano",
        "Inglese"
    ],
    "Fisica": [
        "Elettromagnetismo",
        "Ottica"
    ],
    "Arte": [
        "Storia dell'arte"
    ]
}

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=RevisionedRecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('fare.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=deny_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        list_permission_factory_imp=allow_all
    ),
    'fmgid': dict(
        pid_type=FILE_MNGT_PID_TYPE,
        pid_minter=FILE_MNGT_PID_MINTER,
        pid_fetcher=FILE_MNGT_PID_FETCHER,
        default_endpoint_prefix=True,
        search_class=RevisionSearch,
        indexer_class=RecordIndexer,
        # search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('fare.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('fare.records.loaders'
                                 ':json_v1'),
        },
        list_route='/file_management/',
        item_route='/file_management/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=deny_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for fare."""

RECORDS_UI_ENDPOINTS = {
    'recid': {
        'pid_type': 'recid',
        'route': '/records/<pid_value>',
        'template': 'records/record.html',
    },
}
"""Records UI for fare."""

SEARCH_UI_JSTEMPLATE_RESULTS = 'templates/records/results.html'
"""Result list template."""

PIDSTORE_RECID_FIELD = 'id'

FARE_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""


RECORDS_REST_FACETS = dict(
    records=dict(
        aggs=dict(
            type=dict(terms=dict(field='type')),
            keywords=dict(terms=dict(field='keywords')),
            Ordine_di_scuola=dict(terms=dict(field='educationLevel.keyword')),
            Disciplina=dict(terms=dict(field='subject.keyword'))
        ),
        post_filters=dict(
            type=terms_filter('type'),
            keywords=terms_filter('keywords'),
            Ordine_di_scuola=terms_filter('educationLevel.keyword'),
            Disciplina=terms_filter('subject.keyword'),
        )
    )
)
"""Introduce searching facets."""


RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            title=_('Best match'),
            fields=['_score'],
            default_order='desc',
            order=1,
        ),
        mostrecent=dict(
            title=_('Most recent'),
            fields=['-_created'],
            default_order='asc',
            order=2,
        ),
    )
)
"""Setup sorting options."""


RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(
        query='bestmatch',
        noquery='mostrecent',
    )
)
"""Set default sorting options."""

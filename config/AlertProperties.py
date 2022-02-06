class AlertPriority:
    templates = {
        1: [
            {
                'alert_type': 'AttackIndication',
                'alert_subtype': 'BlackMarket',
                'title_identifiers': [
                    'A bot server holding company customer credentials is offered for sale on a BlackMarket',
                ],
            },
            {
                'alert_type': 'AttackIndication',
                'alert_subtype': 'BotDataForSale',
                'title_identifiers': [
                    'A bot server with credentials for a company',
                    'employees login credentials',
                ],
            },
        ],
        2: [
            {
                'alert_type': 'DataLeakage',
                'alert_subtype': 'ConfidentialInformationExposed',
                'title_identifiers': [
                    'GitHub',
                ],
            },
        ],
        3: [
            {
                'alert_type': 'DataLeakage',
                'alert_subtype': 'CredentialsLeakage',
                'title_identifiers': [
                    'login credentials of',
                    'were leaked',
                ],
            },
            {

                'alert_type': 'DataLeakage',
                'alert_subtype': 'CredentialsLeakage',
                'title_identifiers': [
                    'Company DB is offered for',
                ],
            },
        ],
        4: [
            {
                'alert_type': 'DataLeakage',
                'alert_subtype': 'ConfidentialDocumentLeakage',
                'title_identifiers': [
                    'A company\'s confidential document was exposed publicly',
                ],
                'source_identifiers': [
                    'virustotal.com',
                ],
            },
        ],
        5: [
            {
                'alert_type': 'VIP',
                'alert_subtype': 'BlackMarket',
                'title_identifiers': [
                    'VIP - Private details of a company VIP are offered for sale on a black market',
                ],
            },
        ],
        6: [
            {
                'alert_type': 'DataLeakage',
                'alert_subtype': 'ExposedMentionsOnGithub',
                'title_identifiers': [
                    'GitHub',
                ],
            },
        ],
    }

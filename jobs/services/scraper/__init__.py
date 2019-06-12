default_providers_list = {
    
    "fuzu-it-software":"https://www.fuzu.com/categories/it-software",
    "brightermonday-ug":"https://www.brightermonday.co.ug/jobs/technology/",
    "brightermonday-ke":"https://www.brightermonday.co.ke/jobs/technology/",
    "brightermonday-tz":"https://www.brightermonday.co.tz/jobs/technology/",
    "pigiame":"https://www.pigiame.co.ke/it-telecoms-jobs",
    "ihub-jobs":"https://ihub.co.ke/jobs",
    # "careerpointkenya":"https://www.careerpointkenya.co.ke/category/ict-jobs-in-kenya/",
    # "jobwebkenya":"https://jobwebkenya.com/job-category/ittelecom-jobs-in-kenya-2013/",
}

country_mapping = {
    'CA': 'Canada', 'TM': 'Turkmenistan', 'IR': 'Iran, Islamic Republic of', 'PM': 'Saint Pierre and Miquelon',
    'ET': 'Ethiopia', 'SZ': 'Swaziland', 'CM': 'Cameroon', 'BF': 'Burkina Faso',
    'TG': 'Togo', 'UM': 'United States Minor Outlying Islands', 'CC': 'Cocos (Keeling) Islands', 'BA': 'Bosnia and Herzegovina',
    'RU': 'Russian Federation', 'BQ': 'Bonaire, Sint Eustatius and Saba', 'DM': 'Dominica', 'LR': 'Liberia',
    'MV': 'Maldives', 'CX': 'Christmas Island', 'MC': 'Monaco', 'WF': 'Wallis and Futuna',
    'JE': 'Jersey', 'CI': "C\xc3\xb4te d'Ivoire",'SJ': 'Svalbard and Jan Mayen', 'MO': 'Macao',
    'TR': 'Turkey', 'AF': 'Afghanistan', 'FR': 'France', 'SK': 'Slovakia',
    'VU': 'Vanuatu', 'NR': 'Nauru', 'SC': 'Seychelles', 'NO': 'Norway',
    'MW': 'Malawi', 'CD': 'Congo, the Democratic Republic of the', 'ME': 'Montenegro', 'FM': 'Micronesia, Federated States of',
    'TL': 'Timor-Leste', 'DO': 'Dominican Republic', 'BH': 'Bahrain', 'KY': 'Cayman Islands',
    'LY': 'Libya', 'FI': 'Finland', 'CF': 'Central African Republic', 'LI': 'Liechtenstein',
    'US': 'United States', 'PT': 'Portugal', 'FJ': 'Fiji', 'VE': 'Venezuela, Bolivarian Republic of',
    'MY': 'Malaysia', 'AX': '\xc3\x85land Islands', 'PN': 'Pitcairn', 'GN': 'Guinea',
    'PA': 'Panama', 'KR': 'Korea, Republic of', 'CR': 'Costa Rica', 'LU': 'Luxembourg',
    'AS': 'American Samoa', 'AD': 'Andorra', 'GI': 'Gibraltar', 'IE': 'Ireland',
    'IT': 'Italy', 'NG': 'Nigeria', 'EC': 'Ecuador', 'AU': 'Australia',
    'SV': 'El Salvador', 'TV': 'Tuvalu', 'RW': 'Rwanda', 'TH': 'Thailand',
    'BZ': 'Belize', 'HK': 'Hong Kong', 'SL': 'Sierra Leone', 'GE': 'Georgia',
    'LA':"Lao People's Democratic Republic",'DK': 'Denmark', 'PH': 'Philippines', 'MA': 'Morocco',
    'GG': 'Guernsey', 'EE': 'Estonia', 'CW': 'Cura\xc3\xa7ao', 'LB': 'Lebanon',
    'UZ': 'Uzbekistan', 'FK': 'Falkland Islands (Malvinas)', 'VA': 'Holy See (Vatican City State)', 'CO': 'Colombia',
    'CY': 'Cyprus', 'BB': 'Barbados', 'MG': 'Madagascar', 'PW': 'Palau',
    'SD': 'Sudan', 'BO': 'Bolivia, Plurinational State of', 'NP': 'Nepal', 'NL': 'Netherlands',
    'SR': 'Suriname', 'AI': 'Anguilla', 'IL': 'Israel', 'SN': 'Senegal',
    'PG': 'Papua New Guinea', 'ZW': 'Zimbabwe', 'JO': 'Jordan', 'MQ': 'Martinique',
    'MD': 'Moldova, Republic of', 'MR': 'Mauritania', 'TT': 'Trinidad and Tobago', 'LV': 'Latvia',
    'HU': 'Hungary', 'GP': 'Guadeloupe', 'MX': 'Mexico', 'RS': 'Serbia',
    'GB': 'United Kingdom', 'CG': 'Congo', 'KP':"Korea, Democratic People's Republic of",'PY': 'Paraguay',
    'GF': 'French Guiana', 'BW': 'Botswana', 'ST': 'Sao Tome and Principe', '(.uk)': 'ISO 3166-2:GB',
    'LT': 'Lithuania', 'KH': 'Cambodia', 'SH': 'Saint Helena, Ascension and Tristan da Cunha', 'AW': 'Aruba',
    'AR': 'Argentina', 'GH': 'Ghana', 'SA': 'Saudi Arabia', 'CV': 'Cape Verde',
    'SI': 'Slovenia', 'GT': 'Guatemala', 'KW': 'Kuwait', 'VG': 'Virgin Islands, British',
    'ES': 'Spain', 'PK': 'Pakistan', 'OM': 'Oman', 'GL': 'Greenland',
    'GA': 'Gabon', 'NU': 'Niue', 'BS': 'Bahamas', 'NZ': 'New Zealand',
    'YE': 'Yemen', 'JM': 'Jamaica', 'AL': 'Albania', 'WS': 'Samoa',
    'NF': 'Norfolk Island', 'AE': 'United Arab Emirates', 'GU': 'Guam', 'IN': 'India',
    'AZ': 'Azerbaijan', 'LS': 'Lesotho', 'VC': 'Saint Vincent and the Grenadines', 'KE': 'Kenya',
    'CZ': 'Czech Republic', 'ER': 'Eritrea', 'SB': 'Solomon Islands', 'TC': 'Turks and Caicos Islands',
    'LC': 'Saint Lucia', 'SM': 'San Marino', 'PF': 'French Polynesia', 'MK': 'Macedonia, the former Yugoslav Republic of',
    'SY': 'Syrian Arab Republic', 'BM': 'Bermuda', 'SO': 'Somalia', 'PE': 'Peru',
    'CK': 'Cook Islands', 'BJ': 'Benin', 'CU': 'Cuba', 'KN': 'Saint Kitts and Nevis',
    'IO': 'British Indian Ocean Territory', 'CN': 'China', 'AM': 'Armenia', 'UA': 'Ukraine',
    'TO': 'Tonga', 'EH': 'Western Sahara', 'ID': 'Indonesia', 'MU': 'Mauritius',
    'SE': 'Sweden', 'ML': 'Mali', 'BG': 'Bulgaria', 'PS': 'Palestine, State of',
    'RO': 'Romania', 'AO': 'Angola', 'TF': 'French Southern Territories', 'TD': 'Chad',
    'ZA': 'South Africa', 'TK': 'Tokelau', 'TJ': 'Tajikistan', 'GS': 'South Georgia and the South Sandwich Islands',
    'BN': 'Brunei Darussalam', 'QA': 'Qatar', 'AT': 'Austria', 'MZ': 'Mozambique',
    'UG': 'Uganda', 'JP': 'Japan', 'NE': 'Niger', 'BR': 'Brazil',
    'FO': 'Faroe Islands', 'VI': 'Virgin Islands, U.S.', 'Code': 'Country name', 'BD': 'Bangladesh',
    'VN': 'Viet Nam', 'BY': 'Belarus', 'DZ': 'Algeria', 'MH': 'Marshall Islands',
    'CL': 'Chile', 'PR': 'Puerto Rico', 'BE': 'Belgium', 'KI': 'Kiribati',
    'HT': 'Haiti', 'IQ': 'Iraq', 'GM': 'Gambia', 'HR': 'Croatia',
    'MN': 'Mongolia', 'GW': 'Guinea-Bissau', 'CH': 'Switzerland', 'GD': 'Grenada',
    'TW': 'Taiwan, Province of China', 'IM': 'Isle of Man', 'TZ': 'Tanzania, United Republic of', 'UY': 'Uruguay',
    'BL': 'Saint Barth\xc3\xa9lemy', 'GQ': 'Equatorial Guinea', 'TN': 'Tunisia', 'DJ': 'Djibouti',
    'HM': 'Heard Island and McDonald Islands', 'AG': 'Antigua and Barbuda', 'BI': 'Burundi', 'NI': 'Nicaragua',
    'MF': 'Saint Martin (French part)', 'BT': 'Bhutan', 'MT': 'Malta', 'MP': 'Northern Mariana Islands',
    'BV': 'Bouvet Island', 'IS': 'Iceland', 'ZM': 'Zambia', 'DE': 'Germany',
    'KZ': 'Kazakhstan', 'PL': 'Poland', 'KG': 'Kyrgyzstan', 'GR': 'Greece',
    'YT': 'Mayotte', 'MS': 'Montserrat', 'NC': 'New Caledonia', 'RE': 'R\xc3\xa9union',
    'SS': 'South Sudan', 'GY': 'Guyana', 'HN': 'Honduras', 'MM': 'Myanmar',
    'EG': 'Egypt', 'SG': 'Singapore', 'AQ': 'Antarctica', 'SX': 'Sint Maarten (Dutch part)',
    'LK': 'Sri Lanka', 'NA': 'Namibia', 'KM': 'Comoros'
}
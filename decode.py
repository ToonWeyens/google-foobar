#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64

MESSAGE = '''
D0gcG00UAAoWSVNOT0gJXBIEDUJCU1MMAAJCEgQeEAtUVFVPSUsEERwAAxYQSENOCRIDHwocBwdI T1QOUAwXBhwWEAYNAktQSVlCDxAcBgoYSxoAFxFJU05PSBtAGwoaDgsXU0NPSVwWBxsMGgBTT1VO CQQEHwBJX1RICQFBUEVDRUkEHQFOSVM=
'''

KEY = 'toon.weyens'

result = []
for i, c in enumerate(base64.b64decode(MESSAGE)):
    result.append(chr(ord(c) ^ ord(KEY[i % len(KEY)])))

print ''.join(result)

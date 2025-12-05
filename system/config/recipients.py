
from enum import Enum
from typing import List, Dict, Union
from typing import Literal
from system.utils.recipients_utlis import Recipient


recipients: Dict[str, Recipient] = {
    'some_person_01': {
        'typ': 'internal',
        'sms_active': True,
        'email_active': True,
        'mobile': 987654321,
        'email': 'some_person@some_company.com'
    },
    'some_person_02': {
        'typ': 'internal',
        'sms_active': True,
        'email_active': False,
        'mobile': 123456789,
        'email': 'some_person_02@some_company.com'
    },
    'some_person_03': {
        'typ': 'internal',
        'sms_active': False,
        'email_active': True,
        'mobile': 512369874,
        'email': 'some_person_03@some_company.com'
    },
    'some_person_04': {
        'typ': 'internal',
        'sms_active': False,
        'email_active': False,
        'mobile': None,
        'email': 'some_person_04@some_company.com'
    }
}


class Senders(Enum):

    ReportService = ('Report Service', 'report-service@some_company.com')
    OtherReportService = ('Other Report Service', 'other-report-service@some_company.com')

    def __init__(self, name: str, email: str):
        self.sender_name = name
        self.email = email

    def email_list(self) -> List[str]:
        return [self.email]


class RecipientGroup(Enum):
    a_dist_list = ['some_person_01', 'some_person_02', 'some_person_03']
    another_dist_list = ['some_person_02', 'some_person_03']
    yet_another_dist_list = ['some_person_01']

    def __init__(self, members: List[str]):
        self.members = members

    def get(
        self,
        typ: Literal['mobile', 'email'],
        return_type: Literal['str', 'list'] = 'list',
        active_only: bool = True
    ) -> Union[List[str], str]:

        flag = 'sms_active' if typ == 'mobile' else 'email_active'
        out: List[str] = []

        for m in self.members:
            r = recipients.get(m)
            if not r:
                continue
            if r.get(flag) != active_only:
                continue
            value = r.get(typ)
            if value:
                out.append(str(value))

        if return_type == 'str':
            return str(';'.join(out))
        return out


if __name__ == '__main__':
    print(RecipientGroup.a_dist_list.get(typ='mobile', return_type='str', active_only=True))
    print(RecipientGroup.a_dist_list.get(typ='mobile', return_type='list', active_only=True))
    print(RecipientGroup.a_dist_list.get(typ='email', return_type='str', active_only=True))
    print(RecipientGroup.a_dist_list.get(typ='email', return_type='list', active_only=True))
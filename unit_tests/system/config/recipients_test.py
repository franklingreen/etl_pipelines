import pytest
from system.config.email.recipients import RecipientGroup, recipients


def test_get_email_list_active_only():
    group = RecipientGroup.a_dist_list

    result = group.get("email", return_type="list", active_only=True)

    assert isinstance(result, list)
    # some_person_01: email_active=True
    assert "some_person@some_company.com" in result
    # some_person_03: email_active=True
    assert "some_person_03@some_company.com" in result
    # some_person_02: email_active=False → must not be included
    assert "some_person_02@some_company.com" not in result


def test_get_email_list_inactive_only():
    group = RecipientGroup.a_dist_list

    result = group.get("email", return_type="list", active_only=False)

    assert isinstance(result, list)
    # in this group, only some_person_02 has email_active=False
    assert "some_person_02@some_company.com" in result
    assert "some_person_03@some_company.com" not in result
    assert "some_person@some_company.com" not in result
    assert len(result) == 1


def test_get_email_str():
    group = RecipientGroup.another_dist_list

    result = group.get("email", return_type="str", active_only=True)

    assert isinstance(result, str)
    # some_person_03: email_active=True
    assert "some_person_03@some_company.com" in result
    # some_person_02: email_active=False
    assert "some_person_02@some_company.com" not in result
    # only one email → no separator
    assert ";" not in result


def test_get_mobile_active_only():
    group = RecipientGroup.a_dist_list

    result = group.get("mobile", "list", active_only=True)

    assert isinstance(result, list)
    # active mobiles: some_person_01 + some_person_02
    assert "987654321" in result
    assert "123456789" in result
    # some_person_03: sms_active=False → excluded
    assert "512369874" not in result
    assert None not in result


def test_get_mobile_inactive_only():
    group = RecipientGroup.a_dist_list

    result = group.get("mobile", "list", active_only=False)

    assert isinstance(result, list)
    # inactive mobiles in this group: some_person_03 only
    assert "512369874" in result
    assert "987654321" not in result
    assert "123456789" not in result


def test_missing_recipient_is_skipped_safely():
    # make a local enum-like object using the same logic (or just call the method directly)
    from system.config.email.recipients import RecipientGroup as RG

    # hacky group to test missing key
    class FakeGroup:
        members = ["unknown_user_999"]

        @staticmethod
        def get(typ, return_type="list", active_only=True):
            return RG.a_dist_list.get(typ, return_type, active_only)  # reuse implementation is overkill

    # Simpler: directly test the underlying function behaviour using a custom group instance
    group = RecipientGroup.a_dist_list
    group.members = ["unknown_user_999"]  # monkeypatch members

    result = group.get("email", "list", active_only=True)

    assert result == []

    # restore members to avoid side effects in other tests
    group.members = ["some_person_01", "some_person_02", "some_person_03"]


def test_none_mobile_value_skipped():
    group = RecipientGroup.yet_another_dist_list
    # temporarily point group to a member with None mobile & sms_active=False
    original_members = group.members
    group.members = ["some_person_04"]

    result = group.get("mobile", "list", active_only=False)

    # mobile is None → should not appear
    assert result == []

    # restore
    group.members = original_members


if __name__ == "__main__":
    pytest.main([__file__])
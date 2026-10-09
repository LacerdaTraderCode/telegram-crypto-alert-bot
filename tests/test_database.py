from bot.database import (
    add_alert,
    deactivate_alert,
    list_all_active_alerts,
    list_user_alerts,
    trigger_alert,
)


def test_add_alert_normalizes_symbol_and_direction():
    alert = add_alert(1, "btcusdt", "ABOVE", 70000)

    assert alert.id is not None
    assert alert.symbol == "BTCUSDT"
    assert alert.direction == "above"
    assert alert.target_price == 70000
    assert alert.is_active is True


def test_list_user_alerts_only_returns_active_alerts_of_user():
    mine = add_alert(1, "BTCUSDT", "above", 70000)
    removed = add_alert(1, "ETHUSDT", "below", 2000)
    add_alert(2, "BNBUSDT", "above", 600)
    deactivate_alert(removed.id, 1)

    alerts = list_user_alerts(1)

    assert [alert.id for alert in alerts] == [mine.id]


def test_list_all_active_alerts_spans_users():
    add_alert(1, "BTCUSDT", "above", 70000)
    add_alert(2, "ETHUSDT", "below", 2000)

    assert len(list_all_active_alerts()) == 2


def test_deactivate_alert_requires_ownership():
    alert = add_alert(1, "BTCUSDT", "above", 70000)

    assert deactivate_alert(alert.id, 2) is False
    assert len(list_user_alerts(1)) == 1
    assert deactivate_alert(alert.id, 1) is True
    assert list_user_alerts(1) == []


def test_deactivate_missing_alert_returns_false():
    assert deactivate_alert(999, 1) is False


def test_trigger_alert_deactivates_it():
    alert = add_alert(1, "BTCUSDT", "above", 70000)

    trigger_alert(alert.id)

    assert list_all_active_alerts() == []


def test_trigger_missing_alert_is_a_noop():
    trigger_alert(999)

    assert list_all_active_alerts() == []

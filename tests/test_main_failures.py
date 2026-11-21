import json

from carwatch import config, main


def test_fails_only_after_consecutive_errors(monkeypatch, tmp_path):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr(config, "STATE_FILE", str(state_file))
    monkeypatch.setattr(config, "FAIL_AFTER", 3)
    monkeypatch.setattr(main, "check_used", lambda ctx, st: None)
    monkeypatch.setattr(main, "maybe_send_summary", lambda ctx, st: None)

    def check_new_price(ctx, st):  # nazwa ma znaczenie: licznik jest po __name__
        raise RuntimeError("strona leży")

    monkeypatch.setattr(main, "check_new_price", check_new_price)
    assert [main.main() for _ in range(3)] == [0, 0, 1]
    assert json.loads(state_file.read_text())["check_failures"] == {"check_new_price": 3}

    def check_new_price(ctx, st):
        pass

    monkeypatch.setattr(main, "check_new_price", check_new_price)
    assert main.main() == 0
    assert "check_failures" not in json.loads(state_file.read_text())

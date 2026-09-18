from school_system.services.notifications import (
    StudentNotification,
)


def test_student_notification(capsys):
    observer = StudentNotification()

    observer.update(
        "REGISTERED",
        "STU001",
        "CSC301"
    )

    captured = capsys.readouterr()

    assert (
        "[NOTIFICATION] STU001: "
        "REGISTERED CSC301"
        in captured.out
    )


def test_waitlist_notification(capsys):
    observer = StudentNotification()

    observer.update(
        "WAITLISTED",
        "STU002",
        "CSC501"
    )

    captured = capsys.readouterr()

    assert (
        "[NOTIFICATION] STU002: "
        "WAITLISTED CSC501"
        in captured.out
    )


def test_promotion_notification(capsys):
    observer = StudentNotification()

    observer.update(
        "PROMOTED_FROM_WAITLIST",
        "STU002",
        "CSC501"
    )

    captured = capsys.readouterr()

    assert (
        "[NOTIFICATION] STU002: "
        "PROMOTED_FROM_WAITLIST CSC501"
        in captured.out
    )


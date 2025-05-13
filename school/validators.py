from datetime import date

from validate_docbr import CPF

from school.models import Course
from school.models import Enrollment


Level = Course.Level
Period = Enrollment.Period


def validate_allowed_period(period: str, level: str, birthday: date) -> bool:
    """No student under legal age (18 year old) can start a basic course at night. Only who are already studing can go on."""
    is_valid: bool = True
    try:
        assert not (Period[period] == Period.NIGHT and Level[level] == Level.BASIC and birthday > date(date.today().year - 18, date.today().month, date.today().day))
    except Exception as e:
        is_valid = False
        print(f"A course level {Level[level]} can'to be taught at period {Period[period]} for ones under legal age (birthday: {birthday}) - Exception was: {e}")

    return is_valid


def validate_cpf(cpf_number: str) -> bool:
    cpf: CPF = CPF()

    return cpf.validate(cpf_number)

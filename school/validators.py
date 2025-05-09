from school.models import Course
from school.models import Enrollment


Level = Course.Level
Period = Enrollment.Period


# TODO test it! Maybe pure period is validate by django choices. Use, instead: assert not Period['NIGHT'] and course.level['BASIC']
def validate_allowed_period(period: str) -> bool:
    is_valid: bool = True
    try:
        assert Period[period]
    except Exception as e:
        is_valid = False
        print(f'Error validating period: {e}')

    return is_valid

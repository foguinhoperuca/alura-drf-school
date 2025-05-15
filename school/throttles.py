from rest_framework.throttling import AnonRateThrottle


class CourseAnonRateThrottle(AnonRateThrottle):
    rate = '5/hour'

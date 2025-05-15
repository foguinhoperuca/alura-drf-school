from rest_framework.throttling import AnonRateThrottle


class CourseAnonRateThrottle(AnonRateThrottle):
    rate = '5000/hour'

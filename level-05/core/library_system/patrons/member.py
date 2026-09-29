from core.library_system.borrowing.student_loan_strategy import StudentLoanStrategy
from core.library_system.borrowing.faculty_loan_strategy import FacultyLoanStrategy
from core.library_system.borrowing.community_loan_strategy import CommunityLoanStrategy


class Member:
    def __init__(
        self,
        name,
        member_id,
        contact,
        membership_type,
    ):
        self.name = name
        self.member_id = member_id
        self.contact = contact
        self.membership_type = membership_type
        self.borrowed_resources = []

    @property
    def loan_count(self):
        return len(self.borrowed_resources)

    def add_borrowed_resource(self, resource):
        self.borrowed_resources.append(resource)

    def remove_borrowed_resource(self, resource):
        self.borrowed_resources.remove(resource)

class StudentMember(Member):
    def __init__(
        self,
        name,
        member_id,
        contact,
        membership_type,
        student_id,
        school,
    ):
        super().__init__(
            name,
            member_id,
            contact,
            membership_type,
        )

        self.student_id = student_id
        self.school = school
        self.loan_strategy = StudentLoanStrategy()

    @property
    def borrow_limit(self):
        return self.loan_strategy.get_max_loans()


class FacultyMember(Member):
    def __init__(
        self,
        name,
        member_id,
        contact,
        membership_type,
        department,
        research_area,
    ):
        super().__init__(
            name,
            member_id,
            contact,
            membership_type,
        )

        self.department = department
        self.research_area = research_area
        self.loan_strategy = FacultyLoanStrategy()


class CommunityMember(Member):
    def __init__(
        self,
        name,
        member_id,
        contact,
        membership_type,
        address,
        occupation,
    ):
        super().__init__(
            name,
            member_id,
            contact,
            membership_type,
        )

        self.address = address
        self.occupation = occupation
        self.loan_strategy = CommunityLoanStrategy()
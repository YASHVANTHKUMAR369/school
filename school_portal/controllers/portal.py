from werkzeug.exceptions import Forbidden

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route


class SchoolCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        guardian = self._get_current_guardian()
        if guardian:
            values['school_pending_homework_count'] = request.env['school.homework.submission'].search_count([
                ('student_id.guardian_ids', '=', guardian.id), ('state', '=', 'pending')])
            values['school_fee_due_count'] = request.env['school.fee.invoice'].search_count([
                ('student_id.guardian_ids', '=', guardian.id), ('state', 'in', ('posted', 'partially_paid', 'overdue'))])
        return values

    def _get_current_guardian(self):
        if request.env.user._is_public():
            return None
        return request.env['school.guardian'].search([('user_id', '=', request.env.uid)], limit=1)

    def _get_active_student(self, guardian, student_id=None):
        """Resolve which child is "active" for this portal session, verifying
        ownership explicitly (defense in depth on top of the ir.rule)."""
        students = guardian.student_ids
        if not students:
            return request.env['school.student']
        if student_id:
            student = students.filtered(lambda s: s.id == student_id)
            if not student:
                raise Forbidden()
            request.session['school_active_student_id'] = student.id
            return student
        session_id = request.session.get('school_active_student_id')
        student = students.filtered(lambda s: s.id == session_id)
        if student:
            return student
        return students[0]

    @route(['/my/school'], type='http', auth='user', website=True)
    def school_dashboard(self, student_id=None, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian, int(student_id) if student_id else None)
        values = {
            'page_name': 'school_dashboard',
            'guardian': guardian,
            'students': guardian.student_ids,
            'student': student,
        }
        return request.render('school_portal.portal_school_dashboard', values)

    @route(['/my/school/attendance'], type='http', auth='user', website=True)
    def school_attendance(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        records = request.env['school.student.attendance'].search(
            [('student_id', '=', student.id)], order='date desc', limit=60) if student else []
        values = {
            'page_name': 'school_attendance', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'records': records,
        }
        return request.render('school_portal.portal_school_attendance', values)

    @route(['/my/school/timetable'], type='http', auth='user', website=True)
    def school_timetable(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        slots = request.env['school.timetable.slot'].search(
            [('section_id', '=', student.section_id.id)], order='day_of_week, period_no') if student and student.section_id else []
        day_labels = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday', '4': 'Friday', '5': 'Saturday'}
        values = {
            'page_name': 'school_timetable', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'slots': slots, 'day_labels': day_labels,
        }
        return request.render('school_portal.portal_school_timetable', values)

    @route(['/my/school/homework'], type='http', auth='user', website=True)
    def school_homework(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        submissions = request.env['school.homework.submission'].search(
            [('student_id', '=', student.id)], order='due_date desc') if student else []
        values = {
            'page_name': 'school_homework', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'submissions': submissions,
        }
        return request.render('school_portal.portal_school_homework', values)

    @route(['/my/school/homework/<int:submission_id>/submit'], type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def school_homework_submit(self, submission_id, text_answer='', **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        submission = request.env['school.homework.submission'].search([
            ('id', '=', submission_id), ('student_id.guardian_ids', '=', guardian.id)], limit=1)
        if not submission:
            raise Forbidden()
        submission.write({'text_answer': text_answer})
        submission.action_submit()
        return request.redirect('/my/school/homework')

    @route(['/my/school/exam'], type='http', auth='user', website=True)
    def school_exam(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        cards = request.env['school.report.card'].search(
            [('student_id', '=', student.id), ('state', '=', 'published')], order='exam_id desc') if student else []
        values = {
            'page_name': 'school_exam', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'cards': cards,
        }
        return request.render('school_portal.portal_school_exam', values)

    @route(['/my/school/exam/<int:card_id>/report_card'], type='http', auth='user', website=True)
    def school_report_card_pdf(self, card_id, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        card = request.env['school.report.card'].search([
            ('id', '=', card_id), ('student_id.guardian_ids', '=', guardian.id), ('state', '=', 'published')], limit=1)
        if not card:
            raise Forbidden()
        return self._show_report(model=card, report_type='pdf', report_ref='school_exam.action_report_school_report_card', download=True)

    @route(['/my/school/fees'], type='http', auth='user', website=True)
    def school_fees(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        invoices = request.env['school.fee.invoice'].search(
            [('student_id', '=', student.id)], order='invoice_date desc') if student else []
        payments = request.env['school.fee.payment'].search(
            [('student_id', '=', student.id), ('state', '=', 'confirmed')], order='payment_date desc') if student else []
        values = {
            'page_name': 'school_fees', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'invoices': invoices, 'payments': payments,
        }
        return request.render('school_portal.portal_school_fees', values)

    @route(['/my/school/fees/receipt/<int:payment_id>'], type='http', auth='user', website=True)
    def school_fee_receipt_pdf(self, payment_id, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        payment = request.env['school.fee.payment'].search([
            ('id', '=', payment_id), ('student_id.guardian_ids', '=', guardian.id), ('state', '=', 'confirmed')], limit=1)
        if not payment:
            raise Forbidden()
        return self._show_report(model=payment, report_type='pdf', report_ref='school_fees.action_report_school_fee_receipt', download=True)

    @route(['/my/school/library'], type='http', auth='user', website=True)
    def school_library(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        member = request.env['school.library.member'].search([('student_id', '=', student.id)], limit=1) if student else None
        circulations = member.circulation_ids if member else []
        values = {
            'page_name': 'school_library', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'circulations': circulations,
        }
        return request.render('school_portal.portal_school_library', values)

    @route(['/my/school/transport'], type='http', auth='user', website=True)
    def school_transport(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        allocation = request.env['school.transport.allocation'].search(
            [('student_id', '=', student.id), ('state', '=', 'active')], limit=1) if student else None
        values = {
            'page_name': 'school_transport', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'allocation': allocation,
        }
        return request.render('school_portal.portal_school_transport', values)

    @route(['/my/school/hostel'], type='http', auth='user', website=True)
    def school_hostel(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        student = self._get_active_student(guardian)
        allocation = request.env['school.hostel.allocation'].search(
            [('student_id', '=', student.id), ('state', '=', 'active')], limit=1) if student else None
        values = {
            'page_name': 'school_hostel', 'guardian': guardian,
            'students': guardian.student_ids, 'student': student, 'allocation': allocation,
        }
        return request.render('school_portal.portal_school_hostel', values)

    @route(['/my/school/notices'], type='http', auth='user', website=True)
    def school_notices(self, **kw):
        guardian = self._get_current_guardian()
        if not guardian:
            raise Forbidden()
        notices = request.env['school.notice'].search([('state', '=', 'published')], order='notice_date desc')
        values = {
            'page_name': 'school_notices', 'guardian': guardian,
            'students': guardian.student_ids, 'notices': notices,
        }
        return request.render('school_portal.portal_school_notices', values)

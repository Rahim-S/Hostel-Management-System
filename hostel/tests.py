from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.formats import date_format

from .models import Hostel, Payment, Room, Student, Visitor, Warden


class EditStudentModalTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='tester', password='test-password')
        self.client.force_login(user)
        self.student = Student.objects.create(
            student_id='S001',
            first_name='Alex',
            last_name='Student',
            room_id='R01',
            birth_date='2000-01-01',
            gender='M',
            course='Engineering',
            contact='1234567890',
        )

    def test_edit_link_page_redirects_to_student_list(self):
        response = self.client.get(reverse('edit_student_page', args=[self.student.pk]))

        self.assertRedirects(response, reverse('student_registration_page'))

    def test_edit_post_updates_student_and_returns_to_list(self):
        response = self.client.post(
            reverse('edit_student_page', args=[self.student.pk]),
            {
                'student_id': 'S001',
                'first_name': 'Alexandra',
                'last_name': 'Student',
                'room_id': 'R01',
                'birth_date': '2000-01-01',
                'gender': 'F',
                'course': 'Engineering',
                'contact': '1234567890',
            },
        )

        self.assertRedirects(response, reverse('student_registration_page'))
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Alexandra')
        self.assertEqual(self.student.gender, 'F')

    def test_invalid_edit_renders_list_and_reopens_edit_modal(self):
        response = self.client.post(
            reverse('edit_student_page', args=[self.student.pk]),
            {'first_name': ''},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_registration.html')
        self.assertContains(response, f"editStudentModal{self.student.pk}")
        self.assertContains(response, 'Please correct the errors in the edit form.')


class HostelActionTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='hostel-tester', password='test-password')
        self.client.force_login(user)
        self.hostel = Hostel.objects.create(
            hostel_id='H001',
            hostel_name='North Hall',
            location='North Campus',
            capacity=100,
            status='O',
        )

    def test_edit_and_delete_actions_render_hostel_routes(self):
        response = self.client.get(reverse('hostel_details_page'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('edit_hostel_page', args=[self.hostel.pk]))
        self.assertContains(response, reverse('delete_hostel_page', args=[self.hostel.pk]))
        self.assertContains(response, f'editHostelModal{self.hostel.pk}')

    def test_edit_action_updates_hostel(self):
        response = self.client.post(
            reverse('edit_hostel_page', args=[self.hostel.pk]),
            {
                'hostel_id': 'H001',
                'hostel_name': 'South Hall',
                'location': 'South Campus',
                'capacity': 120,
                'status': 'F',
            },
        )

        self.assertRedirects(response, reverse('hostel_details_page'))
        self.hostel.refresh_from_db()
        self.assertEqual(self.hostel.hostel_name, 'South Hall')
        self.assertEqual(self.hostel.status, 'F')

    def test_delete_action_requires_post_and_deletes_hostel(self):
        response = self.client.get(reverse('delete_hostel_page', args=[self.hostel.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Hostel.objects.filter(pk=self.hostel.pk).exists())

        response = self.client.post(reverse('delete_hostel_page', args=[self.hostel.pk]))

        self.assertRedirects(response, reverse('hostel_details_page'))
        self.assertFalse(Hostel.objects.filter(pk=self.hostel.pk).exists())


class RecordActionTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='record-tester', password='test-password')
        self.client.force_login(user)
        self.room = Room.objects.create(
            room_id='R001',
            room_number='01',
            hostel_id='H001',
            capacity=2,
            status='O',
        )
        self.visitor = Visitor.objects.create(
            visitor_id='V001',
            first_name='Taylor',
            last_name='Visitor',
            relation_to_student='Parent',
            date_of_visit='2026-11-16',
            intime='09:00',
            outtime='10:00',
            contact='1234567890',
            address='Example Street',
        )
        self.warden = Warden.objects.create(
            warden_id='W001',
            first_name='Jordan',
            last_name='Warden',
            hostel_id='H001',
            contact='1234567890',
        )
        self.payment = Payment.objects.create(
            payment_id='P001',
            student_id='S001',
            amount='125.00',
            date_of_payment='2026-10-15',
            mode_of_payment='C',
            due_date='2026-11-15',
            status='P',
            academic_year='2026',
            semester='1',
        )

    def test_edit_and_delete_buttons_render_for_each_record(self):
        pages = [
            ('room_details_page', 'edit_room_page', 'delete_room_page', self.room.pk),
            ('visitor_registration_page', 'edit_visitor_page', 'delete_visitor_page', self.visitor.pk),
            ('warden_registration_page', 'edit_warden_page', 'delete_warden_page', self.warden.pk),
            ('payment_details_page', 'edit_payment_page', 'delete_payment_page', self.payment.pk),
        ]
        for page_name, edit_name, delete_name, record_id in pages:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, reverse(edit_name, args=[record_id]))
                self.assertContains(response, reverse(delete_name, args=[record_id]))

    def test_room_edit_and_post_delete(self):
        response = self.client.post(
            reverse('edit_room_page', args=[self.room.pk]),
            {'room_id': 'R001', 'room_number': '02', 'hostel_id': 'H001', 'capacity': 4, 'status': 'F'},
        )
        self.assertRedirects(response, reverse('room_details_page'))
        self.room.refresh_from_db()
        self.assertEqual(self.room.room_number, '02')

        response = self.client.post(reverse('delete_room_page', args=[self.room.pk]))
        self.assertRedirects(response, reverse('room_details_page'))
        self.assertFalse(Room.objects.filter(pk=self.room.pk).exists())

    def test_visitor_edit_and_post_delete(self):
        response = self.client.post(
            reverse('edit_visitor_page', args=[self.visitor.pk]),
            {
                'visitor_id': 'V001',
                'first_name': 'Taylor',
                'last_name': 'Visitor',
                'relation_to_student': 'Guardian',
                'date_of_visit': '2026-11-16',
                'intime': '09:00',
                'outtime': '10:00',
                'contact': '1234567890',
                'address': 'Example Street',
            },
        )
        self.assertRedirects(response, reverse('visitor_registration_page'))
        self.visitor.refresh_from_db()
        self.assertEqual(self.visitor.relation_to_student, 'Guardian')

        response = self.client.post(reverse('delete_visitor_page', args=[self.visitor.pk]))
        self.assertRedirects(response, reverse('visitor_registration_page'))
        self.assertFalse(Visitor.objects.filter(pk=self.visitor.pk).exists())

    def test_warden_edit_and_post_delete(self):
        response = self.client.post(
            reverse('edit_warden_page', args=[self.warden.pk]),
            {
                'warden_id': 'W001',
                'first_name': 'Jordan',
                'last_name': 'Warden',
                'hostel_id': 'H002',
                'contact': '1234567890',
            },
        )
        self.assertRedirects(response, reverse('warden_registration_page'))
        self.warden.refresh_from_db()
        self.assertEqual(self.warden.hostel_id, 'H002')

        response = self.client.post(reverse('delete_warden_page', args=[self.warden.pk]))
        self.assertRedirects(response, reverse('warden_registration_page'))
        self.assertFalse(Warden.objects.filter(pk=self.warden.pk).exists())

    def test_payment_edit_and_post_delete(self):
        response = self.client.post(
            reverse('edit_payment_page', args=[self.payment.pk]),
            {
                'payment_id': 'P001',
                'student_id': 'S001',
                'amount': '150.00',
                'date_of_payment': '2026-10-15',
                'mode_of_payment': 'C',
                'due_date': '2026-11-15',
                'status': 'P',
                'academic_year': '2026',
                'semester': '1',
            },
        )
        self.assertRedirects(response, reverse('payment_details_page'))
        self.payment.refresh_from_db()
        self.assertEqual(str(self.payment.amount), '150.00')

        response = self.client.post(reverse('delete_payment_page', args=[self.payment.pk]))
        self.assertRedirects(response, reverse('payment_details_page'))
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())


class PaymentDetailsTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='payment-tester', password='test-password')
        self.client.force_login(user)

    def test_submitted_payment_is_shown_in_the_table(self):
        response = self.client.post(
            reverse('payment_details_page'),
            {
                'payment_id': 'P001',
                'student_id': 'S001',
                'amount': '125.00',
                'date_of_payment': '2026-10-15',
                'mode_of_payment': 'C',
                'due_date': '2026-11-15',
                'status': 'P',
                'academic_year': '2026',
                'semester': '1',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Payment.objects.filter(payment_id='P001').exists())
        self.assertContains(response, 'P001')
        self.assertContains(response, 'Cash')
        self.assertContains(response, 'Paid')

    def test_invalid_payment_reopens_modal_with_validation_errors(self):
        response = self.client.post(
            reverse('payment_details_page'),
            {
                'payment_id': 'P002',
                'student_id': 'S001',
                'amount': '125.00',
                'date_of_payment': 'not-a-date',
                'mode_of_payment': 'C',
                'due_date': '2026-11-15',
                'status': 'P',
                'academic_year': '2026',
                'semester': '1',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid date.')
        self.assertContains(response, "bootstrap.Modal.getOrCreateInstance(paymentModal).show()")
        self.assertFalse(Payment.objects.filter(payment_id='P002').exists())

    def test_payment_dates_use_native_date_inputs(self):
        response = self.client.get(reverse('payment_details_page'))

        self.assertContains(response, 'type="date" name="date_of_payment"')
        self.assertContains(response, 'type="date" name="due_date"')


class VisitorDetailsTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='visitor-tester', password='test-password')
        self.client.force_login(user)

    def test_submitted_visitor_relationship_and_date_are_shown(self):
        response = self.client.post(
            reverse('visitor_registration_page'),
            {
                'visitor_id': 'V001',
                'first_name': 'Taylor',
                'last_name': 'Visitor',
                'relation_to_student': 'Parent',
                'date_of_visit': '2026-11-16',
                'intime': '09:00',
                'outtime': '10:00',
                'contact': '1234567890',
                'address': 'Example Street',
            },
        )

        visitor = Visitor.objects.get(visitor_id='V001')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Parent')
        self.assertContains(response, date_format(visitor.date_of_visit))

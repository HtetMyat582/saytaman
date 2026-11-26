from django.test import SimpleTestCase
from django.template.loader import render_to_string
from .forms import MissionFuelRefillFormSet
from .models import MissionRecord


class MissionFuelRefillFormSetTests(SimpleTestCase):
	def make_formset(self, total_forms, form_data=None):
		data = {
			'fuel_refills-TOTAL_FORMS': str(total_forms),
			'fuel_refills-INITIAL_FORMS': '0',
		}
		data.update(form_data or {})
		return MissionFuelRefillFormSet(
			data=data,
			instance=MissionRecord(mission_number='001/26'),
			prefix='fuel_refills',
		)

	def test_empty_formset_is_valid(self):
		formset = self.make_formset(0)

		self.assertTrue(formset.is_valid(), formset.errors)
		self.assertEqual(formset.total_form_count(), 0)

	def test_added_refill_requires_required_fields(self):
		formset = self.make_formset(1, {
			'fuel_refills-0-pump_name': 'Pump A',
		})

		self.assertFalse(formset.is_valid())
		self.assertIn('liters', formset.forms[0].errors)
		self.assertIn('cost', formset.forms[0].errors)

	def test_cancelled_refill_is_ignored(self):
		formset = self.make_formset(1, {
			'fuel_refills-0-pump_name': 'Pump A',
			'fuel_refills-0-DELETE': 'on',
		})

		self.assertTrue(formset.is_valid(), formset.errors)
		self.assertEqual(formset.deleted_forms, [formset.forms[0]])
		html = render_to_string(
			'mission_records/_fuel_refill_formset.html',
			{'fuel_formset': formset},
		)
		self.assertIn('fuel-refill-card" hidden', html)

	def test_empty_formset_keeps_section_copy_and_remove_control(self):
		html = render_to_string(
			'mission_records/_fuel_refill_formset.html',
			{'fuel_formset': self.make_formset(0)},
		)

		self.assertIn('On-mission fuel refills', html)
		self.assertIn('Enter one row for each refill.', html)
		self.assertIn('data-remove-refill', html)
		self.assertIn('fuel-refill-delete-button', html)
		self.assertIn('bi-x-lg', html)

	def test_refill_row_hides_delete_input_and_renders_top_right_x(self):
		html = render_to_string(
			'mission_records/_fuel_refill_formset.html',
			{'fuel_formset': self.make_formset(1)},
		)

		self.assertIn('class="fuel-delete-field" hidden', html)
		self.assertIn('class="fuel-refill-card-header"', html)
		self.assertIn('class="btn btn-danger fuel-refill-delete-button"', html)
		self.assertIn('bi-x-lg', html)

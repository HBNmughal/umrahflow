from django.utils.translation import gettext_lazy as _


city_choices = (
    ('makkah', _('Makkah')),
    ('med', _('Medina')),
)

flight_types = (
    ('arrival', _('Arrival')),
    ('departure', _('Departure')),
)


transport_cities = (
    ('JED-A', _('Jeddah Airport')),
    ('MED-A', _('Medina Airport')),
    ('MAK', _('Makkah')),
    ('MED', _('Medina')),
    ('LAND', _('Land Border'))
)

transport_types = (
    ('arrival', _('Arrival')),
    ('departure', _('Departure')),
    ('intercity', _('InterCity')),
    ('city_tour', _('City Tour')),
)

nusuk_permit_types = (
    ('rawdah_men', _('Prayer in Rawdah - Men')),
    ('rawdah_women', _('Prayer in Rawdah - Women')),
    ('umrah', _('Umrah'))
)

voucher_status = (
    ('under_review', _('Under Review')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected')),
    ('draft', _('Draft')),

)

transportation_type = (
    ('air', _('By Air')),
    ('land', _('By Land')),
    ('sea', _('By Sea'))
)

transport_routes = (
    ('3', _('3 Routes')),
    ('4', _('4 Routes')),
)

saudi_airports = (
    ('JED', _('Jeddah Airport')),
    ('MED', _('Medina Airport')),
)


from django.core.management.base import BaseCommand

from website.models import (
    Config,
    Location,
    LocationGroup,
    Master,
    Program,
    ProgramBelt,
    TimelineEvent,
)


class Command(BaseCommand):
    help = 'Seed CMS content (locations, programs, masters, timeline, config) if empty'

    def handle(self, *args, **options):
        self._seed_config()
        self._seed_locations()
        self._seed_masters()
        self._seed_timeline()
        self._seed_programs()
        self.stdout.write(self.style.SUCCESS('CMS seed complete.'))

    def _seed_config(self):
        config = Config.get_solo()
        updates = {}
        if not config.contact_phone:
            updates['contact_phone'] = '069/2153419'
        if not config.contact_phone_2:
            updates['contact_phone_2'] = '065/5911859'
        if not config.contact_phone_3:
            updates['contact_phone_3'] = '064/1236222'
        if not config.email or config.email.startswith('default'):
            updates['email'] = 'info@aikidovokic.rs'
        if not config.email_2:
            updates['email_2'] = 'nikola@aikidovokic.rs'
        if not config.address or config.address.startswith('default'):
            updates['address'] = 'Geteova 3A, Beograd 11080'
        if updates:
            for key, value in updates.items():
                setattr(config, key, value)
            config.save()
            self.stdout.write('Updated Config')

    def _seed_locations(self):
        if Location.objects.exists():
            self.stdout.write('Locations already exist — skip')
            return
        loc = Location.objects.create(
            name='Zemun',
            address='Geteova 3A, Beograd 11080',
            phone='069/2153419',
            trainer_name='Aleksandar Petrović',
            trainer_belt='Crni pojas 2. Dan',
            map_embed_url='https://www.google.com/maps?q=Geteova%203A%2C%20Beograd%2011080&output=embed',
            sort_order=1,
        )
        LocationGroup.objects.create(
            location=loc,
            group_type='younger',
            label='Mlađa grupa',
            days='Utorak i Četvrtak',
            time_range='19:30 DO 20:30',
            sort_order=1,
        )
        LocationGroup.objects.create(
            location=loc,
            group_type='older',
            label='Starija grupa',
            days='Utorak i Četvrtak',
            time_range='20:30 DO 21:30',
            sort_order=2,
        )
        self.stdout.write('Created Location: Zemun')

    def _seed_masters(self):
        if Master.objects.exists():
            self.stdout.write('Masters already exist — skip')
            return
        for i, name in enumerate([
            'Ljubomir Vračarević',
            'Aleksandar Petrović',
            'Nikola Simić',
        ], start=1):
            Master.objects.create(name=name, sort_order=i)
        self.stdout.write('Created Masters')

    def _seed_timeline(self):
        if TimelineEvent.objects.exists():
            self.stdout.write('Timeline already exists — skip')
            return
        events = [
            (1985, 'Osnivanje', 'Osnivanje kluba sa misijom širenja tradicionalnog Aikido znanja u Srbiji.'),
            (1992, 'Međunarodni seminar', 'Prvi međunarodni seminar sa gostima iz Japana i Evrope u Beogradu.'),
            (2005, 'Novi dojo', 'Novi dojo otvara svoja vrata u centru grada, sa više termina za sve uzraste.'),
            (2023, 'Novi programi', 'Uvodimo specijalizovane programe za decu, rekreativce i početnike.'),
        ]
        for i, (year, title, desc) in enumerate(events, start=1):
            TimelineEvent.objects.create(year=year, title=title, description=desc, sort_order=i)
        self.stdout.write('Created Timeline events')

    def _seed_programs(self):
        if Program.objects.exists():
            self.stdout.write('Programs already exist — skip')
            return

        kids = Program.objects.create(title='Za decu', audience='kids', sort_order=1)
        adults = Program.objects.create(title='Za odrasle', audience='adults', sort_order=2)

        kids_belts = [
            ('Žuti pojas', 'yellow', 'Kretnja, padovi, osnovni udarci i oslobađanje od hvata. Uvod u tehnike samoodbrane.', 'hHyoTwqMJts'),
            ('Narandžasti pojas', 'orange', 'Naprednija kretanja, blokade i tehnike odbrane od hvata i udaraca.', ''),
            ('Zeleni pojas', 'green', 'Kombinacije padova, udarci pesnicom i nogom, blokade i složene tehnike.', ''),
            ('Plavi pojas', 'blue', 'Proširenje tehnika, preciznost i kontrola u situacijama napada.', ''),
            ('Braon pojas', 'brown', 'Priprema za više nivoe — kompleksne odbrane i princip kontinuiteta.', ''),
        ]
        for i, (name, color, desc, yt) in enumerate(kids_belts, start=1):
            ProgramBelt.objects.create(
                program=kids, name=name, color=color, description=desc,
                youtube_id=yt, sort_order=i,
            )

        adult_belts = [
            ('5 Kyu — žuti pojas', 'yellow', 'Osnove stava, kretnje, padova i prvih tehnika samoodbrane.'),
            ('4 Kyu — narandžasti pojas', 'orange', 'Blokade, oslobađanja i uvod u naprednije tehnike.'),
            ('3 Kyu — zeleni pojas', 'green', 'Udarci, blokade i više situacionih odbrana.'),
            ('2 Kyu — plavi pojas', 'blue', 'Složene tehnike i veća preciznost u izvođenju.'),
            ('1 Kyu — braon pojas', 'brown', 'Priprema za dan — princip, kontrola i primena u realnim situacijama.'),
        ]
        for i, (name, color, desc) in enumerate(adult_belts, start=1):
            ProgramBelt.objects.create(
                program=adults, name=name, color=color, description=desc, sort_order=i,
            )

        self.stdout.write('Created Programs and belts')

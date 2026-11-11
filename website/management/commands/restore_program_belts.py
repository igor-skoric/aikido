from django.core.management.base import BaseCommand

from website.models import Program, ProgramBelt


KIDS = [
    {
        'name': 'Žuti pojas',
        'color': 'yellow',
        'youtube_id': 'hHyoTwqMJts',
        'description': (
            '<p><strong>Kretnja:</strong> levi stav, desni stav, okret na stopalima (u mestu), okret na prednjoj nozi, '
            'korak okret, korak okret mali okret, iskorak u stranu</p>'
            '<p><strong>Padovi:</strong> kolut napred, pad napred, pad nazad</p>'
            '<p><strong>Udarci:</strong> uvežbavanje udarca odozgo u glavu</p>'
            '<p><strong>Oslobađanje od hvata:</strong> za istu ruku, za suprotnu ruku</p>'
            '<p><strong>Tehnike:</strong></p><ul>'
            '<li>odbrana od hvata za kosu spreda (povlačenje u nazad i poluga na zglobu šake, radi se ispred napadača)</li>'
            '<li>odbrana od hvata za okovratnik, jednom rukom od pozadi (provlačenje ispod ruke unazad i poluga na zglobu šake, radi se ispred napadača)</li>'
            '<li>odbrana od hvata sa strane od pozadi (džeparenje, radi se iza napadača)</li>'
            '<li>odbrana od hvata za ruku (rukovanje) provlačenje i sečenje rukom na dole (radi se ispred napadača)</li>'
            '<li>odbrana od hvata desnom rukom za desnu ruku (korak okret mali okret, radi se iza napadača)</li>'
            '<li>odbrana od hvata za suprotnu ruku (hvat desnom rukom za levu ruku, iskorak u stranu i poluga na zglobu šake, radi se iza napadača)</li>'
            '<li>odbrana od hvata za grudi iskorak u stranu šamar i poluga na zglobu šake (radi se ispred napadača)</li>'
            '</ul>'
        ),
    },
    {
        'name': 'Narandžasti pojas',
        'color': 'orange',
        'youtube_id': '',
        'description': (
            '<p><strong>Kretnja:</strong> okret na stopalima (u mestu), okret na prednjoj nozi, korak okret, '
            'korak okret mali okret, iskorak u stranu</p>'
            '<p><strong>Padovi:</strong> pad napred, pad nazad</p>'
            '<p><strong>Udarci:</strong> uvežbavanje kružnog udarca rukom sa strane u glavu</p>'
            '<p><strong>Blokade:</strong> blokiranje kružnog udarca rukom sa strane u glavu</p>'
            '<ul><li>iskorak sa blokom i udarac u glavu</li>'
            '<li>iskorak u stranu, blok sa ukrštenim rukama</li></ul>'
            '<p><strong>Tehnike:</strong></p><ul>'
            '<li>odbrana od hvata sa dve ruke za dve ruke spreda (iskorak u stranu i poluga na zglobu šake, radi se iza napadača)</li>'
            '<li>odbrana od hvata dve ruke za dve ruke spreda (izvrtanje na gore sa fiksacijom na grudima i rušenje, radi se ispred napadača)</li>'
            '<li>odbrana od hvata za ruku (rukovanje desnom rukom za desnu ruku, okretanje tela, ringišpil, radi se ispred napadača)</li>'
            '<li>odbrana od obuhvata oko struka (oslobađanje hvatom za prste, džeparenje, radi se iza napadača)</li>'
            '<li>udarac odozgo u glavu (iskorak u stranu, ukršteni blok i propuštanje sa strane, radi se iza napadača)</li>'
            '<li>udarac odozgo u glavu (iskorak u stranu sa ukrštenim blokom, propuštanje i sečenje na dole i poluga na zglobu šake, radi se ispred napadača)</li>'
            '<li>kružni udarac rukom sa strane (blok presretanje sa udarcem u glavu, prebacivanje ruke ispred sebe i poluga na zglobu šake, radi se iza napadača)</li>'
            '</ul>'
        ),
    },
    {
        'name': 'Zeleni pojas',
        'color': 'green',
        'youtube_id': '',
        'description': (
            '<p><strong>Kretnja:</strong> ista kao za prethodne pojaseve, korak okret mali okret i korak okret</p>'
            '<p><strong>Padovi:</strong> Isti kao za prethodne pojaseve, tvrdi pad napred (sa udarcem ruke), '
            'pad napred i nazad (kombinacija) i džudo pad nazad</p>'
            '<p><strong>Udarci:</strong></p><ul>'
            '<li>uvežbavanje udaraca pesnicom direktno u stomak</li>'
            '<li>uvežbavanje udarca nogom u stomak (maegeri)</li></ul>'
            '<p><strong>Blokade:</strong> Blokiranje udarca pesnicom u stomak</p><ul>'
            '<li>ukršteni blok (povlačenje noge u nazad, ukršteni blok rukama)</li>'
            '<li>propuštanje udarca desnom rukom</li></ul>'
            '<p><strong>Tehnike:</strong></p><ul>'
            '<li>odbrana od hvata dve ruke za dve ruke spreda (provlačenje ispod desne ruke i korak okret mali okret i rušenje na dole, radi se iza napadača)</li>'
            '<li>kružni udarac rukom u glavu (šamar, blok na unutrašnju stranu i rušenje, radi se ispred napadača)</li>'
            '<li>udarac pesnicom odozdo u stomak (povlačenje noge u nazad, ukršteni blok, šamar i rušenje, radi se ispred napadača)</li>'
            '<li>odbrana od hvata za oba ramena od pozadi (povlačenje noge u nazad, provlačenje glave između ruku i rušenje na dole, radi se iza napadača)</li>'
            '<li>odbrana od hvata za oba ramena od napred (šamar, izvrtanje ruke sa rušenjem i poluga na laktu, radi se ispred napadača)</li>'
            '<li>odbrana od hvata (rukovanje, korak okret, provlačenje ispod ruke i sečenje na dole, uvrtanje šake, radi se ispred napadača)</li>'
            '<li>odbrana od obuhvata rukom oko vrata (davljenje, hvat za kosu od nazad i povlačenje i rušenje, radi se iza napadača)</li>'
            '<li>udarac rukom odozgo u glavu (korak okret mali okret, radi se iza napadača)</li>'
            '<li>odbrana od hvata za rever od nazad (okret na stopalima na spoljnu stranu i korak okret mali okret, rušenje i poluga na ruci, radi se iza napadača)</li>'
            '</ul>'
            '<p><strong>Izbegavanje napadača:</strong></p><ul>'
            '<li>udarac rukom odozgo u glavu (izbegavanje jedan na jedan, korak okret mali okret)</li>'
            '<li>udarac pesnicom u stomak (izbegavanje jedan na jedan, korak okret mali okret)</li></ul>'
        ),
    },
    {
        'name': 'Plavi pojas',
        'color': 'blue',
        'youtube_id': '',
        'description': (
            '<p><strong>NAPOMENA:</strong> kandidat je obavezan da zna sve raditi na obe strane</p>'
            '<p><strong>Kretnje:</strong> sva kretnja, iskorak u stranu ukršteni blok okret na prednjoj nozi, slobodna kretnja</p>'
            '<p><strong>Padovi:</strong> svi padovi, pad napred na podlaktice</p>'
            '<p><strong>Udarci:</strong> uvežbavanje kružnog udarca nogom (niski mavaši u telo)</p>'
            '<p><strong>Tehnike:</strong></p><ul>'
            '<li>udarac rukom odozgo u glavu (iskorak u stranu ukršteni blok propuštanje ruke i hvat ruke i poluga na zglobu šake, radi se iza napadača)</li>'
            '<li>odbrana od obuhvata oko struka od pozadi (izvlačenje jedne noge, hvat za nogu i rušenje, poluga na nozi)</li>'
            '<li>odbrana od hvata dve ruke za dve ruke od pozadi (prebacivanje jedne ruke poluga na malom prstu, radi se ispred napadača)</li>'
            '<li>odbrana od hvata dve ruke za dve ruke spreda (izvrtanje ruku, damski hvat i rušenje napadača hvatom za kosu unazad, radi se iza napadača)</li>'
            '<li>kružni udarac rukom sa strane u glavu (šamar i rušenje sa unutrašnje strane, radi se ispred napadača)</li>'
            '<li>kružni udarac sa strane nogom u telo (prihvatanje noge korak okret, izvlačenje noge u nazad i poluga na nozi, radi se ispred napadača)</li>'
            '<li>hvat desnom rukom za desnu ruku (šamar sa korak okret mali okret, rušenje i poluga na zglobu šake, radi se iza napadača)</li>'
            '<li>direktni udarac pesnicom u stomak (propuštanje desnom rukom, hvat za ramena i rušenje, radi se iza napadača)</li>'
            '<li>odbrana od noža, ubod nožem odozdo (ukršteni blok šamar, prebacivanje ruke i poluga na zglobu šake, radi se ispred napadača)</li>'
            '<li>ubod nožem sa strane (presretanje blok sa udarcem u glavu prebacivanje ruke i poluga na zglobu šake, radi se iza napadača)</li>'
            '</ul>'
            '<p><strong>Izbegavanje napadača:</strong></p><ul>'
            '<li>udarac rukom odozgo u glavu (izbegavanje jedan na jedan – dinamika)</li>'
            '<li>udarac direktno pesnicom u stomak (izbegavanje jedan na jedan – dinamika)</li></ul>'
        ),
    },
    {
        'name': 'Braon pojas',
        'color': 'brown',
        'youtube_id': '',
        'description': (
            '<p><strong>NAPOMENA:</strong> kandidat je obavezan da zna sve raditi na obe strane</p>'
            '<p><strong>Kretnje:</strong> sva kretnja, slobodna kretnja</p>'
            '<p><strong>Padovi:</strong> svi padovi, džudži garami (ukršteni hvat rukama), leteći pad, kata pad (sa ostajanjem na strunjači)</p>'
            '<p><strong>Udarci / Tehnike:</strong></p><ul>'
            '<li>Odbrana od hvata za okovratnik od pozadi (okretanje unutra, šamar i rušenje, radi se ispred napadača)</li>'
            '<li>Odbrana od hvata za okovratnik od pozadi (brzo provlačenje ispod ruke i poluga na laktu sa obe ruke, radi se ispred napadača)</li>'
            '<li>Odbrana od hvata desnom rukom za desnu ruku (korak okret spolja, provlačenje ispod ruke, povlačenje napadača za sobom, poluga na laktu i rušenje, radi se iza napadača)</li>'
            '<li>Odbrana od hvata desnom rukom za desnu (prethvatanje ruke, poluga na laktu, korak okret mali okret, rušenje i poluga na zglobu šake, radi se iza napadača)</li>'
            '<li>Odbrana od hvata za ruku i kragnu (prebacivanje ruke preko glave, rušenje i poluga na zglobu šake, radi se ispred napadača)</li>'
            '<li>Udarac rukom odozgo u glavu (korak okret mali okret poluga na glavi, povlačenje glave u nazad dole prema strunjači, radi se iza napadača)</li>'
            '<li>Udarac rukom odozgo u glavu (propuštanje udarca i čišćenje nogom na jednu nogu, radi se ispred napadača)</li>'
            '<li>Kružni udarac rukom sa strane (iskorak u stranu, ukršteni blok, prebacivanje ruke, prolazak ispod, poluga na malom prstu, radi se iza napadača)</li>'
            '<li>Direktni udarac pesnicom u stomak (šamar, korak okret mali okret, rušenje i poluga na zglobu šake, radi se iza napadača)</li>'
            '<li>Odbrana od udarca palicom odozgo (presretanje na unutrašnju stranu i poluga na zglobu šake, radi se ispred napadača)</li>'
            '<li>Odbrana od udarca palicom odozgo (presretanje, ukršteni blok, propuštanje i sečenje na dole, radi se iza napadača)</li>'
            '</ul>'
            '<p><strong>Odbrana od dva napadača (Džiu-vaza):</strong></p><ul>'
            '<li>Udarac rukom odozgo u glavu, izbegavanje</li>'
            '<li>Udarac pesnicom u stomak, izbegavanje</li></ul>'
        ),
    },
]

ADULTS = [
    {
        'name': '5 Kyu žuti pojas',
        'color': 'yellow',
        'description': (
            '<p><strong>PADOVI (UKEMI)</strong></p><ul>'
            '<li>Kolut napred</li><li>Pad napred (MAE UKEMI)</li><li>Pad nazad (USHIRO UKEMI)</li></ul>'
            '<p><strong>KRETANJA (TAI SABAKI)</strong></p><ul>'
            '<li>Okret unazad (USHIRO TENKAN)</li><li>Korak okret (IRIMI TENKAN)</li>'
            '<li>Okret na stopalima (TENKAI)</li><li>Korak okret mali okret (IRIMI TENKAN TENKAI)</li>'
            '<li>Iskorak u stranu (TSUGI ASHI)</li></ul>'
            '<p><strong>TEHNIKE</strong></p><ul>'
            '<li>Odbrana od hvata za istu ruku -prva forma (KATATE TORI AI HANMI IKKYO-URA)</li>'
            '<li>Odbrana od hvata za istu ruku -poluga na zglobu šake i laktu (KATATE TORI AI HANMI SHIHO NAGE-OMOTE)</li>'
            '<li>Odbrana od hvata za istu ruku -poluga na zglobu šake izvrtanjem (KATATE TORI AI HANMI KOTEGAESHI)</li>'
            '<li>Odbrana od hvata za suprotnu ruku -poluga na zglobu šake peta forma (KATATE TORI GYAKU HANMI GOKYO-URA)</li>'
            '<li>Odbrana od hvata za suprotnu ruku- poluga na zglobu šake i laktu (KATATE TORI GYAKU HANMI SHIHO NAGE-URA)</li>'
            '<li>Odbrana od hvata za rame -druga forma (ERI TORI NIKYO)</li>'
            '<li>Odbrana od hvata za okovratnik -peta forma (USHIRO ERI TORI GOKYO-OMOTE)</li>'
            '<li>Odbrana od udarca od gore u glavu -prva forma (SHOMEN UCHI IKKYO-URA)</li>'
            '<li>Odbrana od udarca od gore u glavu -poluga na zglobu šake (SHOMEN UCHI KOTEGAESHI)</li>'
            '<li>Odbrana od kružnog udarca u glavu- prva forma – ukršten blok (YOKOMEN UCHI IKKYO-URA)</li>'
            '<li>Odbrana od kružnog udarca u glavu peta forma – direktan blok (YOKOMEN UCHI GOKYO-OMOTE)</li>'
            '</ul>'
        ),
    },
    {
        'name': '4 Kyu narandžasti pojas',
        'color': 'orange',
        'description': (
            '<p><strong>PADOVI (UKEMI)</strong></p><ul>'
            '<li>Pad napred (MAE UKEMI)</li><li>Pad nazad (USHIRO UKEMI)</li>'
            '<li>Pad napred nazad (MAE UKEMI USHIRO UKEMI)</li>'
            '<li>Pad napred ublažen udarcem (KATA UKEMI)</li></ul>'
            '<p><strong>KRETANJA (TAI SABAKI)</strong></p>'
            '<p><strong>TEHNIKE</strong></p><ul>'
            '<li>Odbrana od hvata za istu ruku -poluga na zglobu šake druga forma (KATATE TORI AI HANMI NIKYO)</li>'
            '<li>Odbrana od hvata za istu ruku -poluga na laktu (KATATE TORI AI HANMI UDE OSAE-OMOTE)</li>'
            '<li>Odbrana od hvata za istu ruku -poluga na vratu (KATATE TORI AI HANMI IRIMI NAGE)</li>'
            '<li>Odbrana od hvata za suprotnu ruku -poluga na zglobu šake izvrtanjem (KATATE TORI GYAKU HANMI KOTEGAESHI)</li>'
            '<li>Odbrana od hvata za suprotnu ruku -poluga na zglobu šake i laktu- privođenje (KATATE TORI GYAKU HANMI UDE GARAMI)</li>'
            '<li>Odbrana od udarca od gore u glavu -poluga na malom prstu povlačenje na dole- treća forma (SHOMEN UCHI UCHI KAITEN SANKYO-OMOTE)</li>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke -poluga na zglobu šake i laktu (RYOTE TORI SHIHONAGE-URA)</li>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke-provlačenjem ispod ruke (RYOTE TORI UCHI KAITEN NIKYO-OMOTE)</li>'
            '<li>Odbrana od hvata za suprotnu ruku-poluga na zglobu šake –druga forma (KATATE TORI GYAKU HANMI NIKYO)</li>'
            '<li>Odbrana od kružnog udarca u glavu- poluga na zglobu šake i laktu (YOKOMEN UCHI SHIHO NAGE -OMOTE)</li>'
            '<li>Odbrana od udarca od dole u stomak -poluga na zglobu šake – peta forma (GEDAN TSUKI GOKYO)</li>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke od pozadi- poluga na zglobu šake -peta forma (USHIRO RYOTE TORI GOKYO)</li>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke od pozadi -poluga na malom prstu-treća forma (USHIRO RYOTE TORI SANKYO)</li>'
            '</ul>'
        ),
    },
    {
        'name': '3 Kyu zeleni pojas',
        'color': 'green',
        'description': (
            '<p><strong>PADOVI (UKEMI):</strong> kandidat radi obe strane –leva i desna</p><ul>'
            '<li>Pad napred (MAE UKEMI)</li><li>Pad nazad (USHIRO UKEMI)</li>'
            '<li>Pad napred nazad (MAE UKEMI USHIRO UKEMI)</li>'
            '<li>Pad napred ublažen udarcem (KATA UKEMI)</li>'
            '<li>Tvrdi pad napred (KATA MAE UKEMI)</li>'
            '<li>Tvrdi pad nazad (KATA USHIRO UKEMI)</li></ul>'
            '<p><strong>KRETANJA (TAI SABAKI):</strong> izbegavanje napadača 1 na 1 (irimi tenkan tenkai irimi tenkan)</p>'
            '<p><strong>TEHNIKE:</strong> kandidat radi obe strane –leva i desna</p><ul>'
            '<li>Odbrana od hvata za istu ruku -poluga na malom prstu – treća forma (KATATE TORI AI HANMI SANKYO)</li>'
            '<li>Odbrana od hvata za istu ruku- bacanje gušenjem (KATATE TORI AI HANMI HIJI KIME OSAE)</li>'
            '<li>Odbrana od hvata za rame- provlačenje glave poluga na laktu (ERI TORI UDE OSAE)</li>'
            '<li>Odbrana od udarca od gore u glavu -poluga na vratu (SHOMEN UCHI IRIMI NAGE)</li>'
            '<li>Odbrana od udarca od gore u glavu- bacanje polugom na laktu i zglobu šake (SHOMEN UCHI UDE GARAMI)</li>'
            '<li>Odbrana od udarca u stomak- bacanje šamarom (CHUDAN TSUKI KIRI GAESHI)</li>'
            '<li>Odbrana od kružnog udarca u glavu -bacanje gušenjem (YOKOMEN UCHI HIJI KIME OSAE)</li>'
            '<li>Odbrana od hvata za okovratnik od pozadi -poluga na laktu (USHIRO ERI TORI UDE OSAE)</li>'
            '<li>Odbrana od direktnog udarca u glavu- prva forma (JODAN TSUKI IKKYO-URA)</li>'
            '<li>Odbrana od direktnog udarca u glavu- poluga na zglobu šake izvrtanjem (JODAN TSUKI KOTEGAESHI)</li>'
            '<li>Odbrana od direktnog udarca nogom u stomak -ulazak unutra čišćenje (MAE GERI OSETO GARI)</li></ul>'
            '<p><strong>Odbrana od oružja (BUKI WAZA)</strong></p>'
            '<p><em>Odbrana od noža</em></p><ul>'
            '<li>Odbrana od boda u stomak od dole- druga forma (GEDAN TSUKI TANTO TORI NIKYO-OMOTE)</li>'
            '<li>Direktan bod u stomak poluga na zglobu šake izvrtanjem (CHUDAN TSUKI TANTO TORI KOTEGAESHI)</li></ul>'
            '<p><em>Odbrana od palice</em></p><ul>'
            '<li>Odbrana od udarca palicom od gore -prva forma (SHOMEN UCHI IKKYO-URA)</li>'
            '<li>Odbrana od udarca palicom kružno iznutra prema spolja (URAKEN-IKKYO -URA)</li></ul>'
        ),
    },
    {
        'name': '2 Kyu plavi pojas',
        'color': 'blue',
        'description': (
            '<p><strong>PADOVI (UKEMI)</strong></p><ul>'
            '<li>Svi padovi</li><li>Pad u stranu</li><li>Pad na podlaktice</li></ul>'
            '<p><strong>KRETANJA (TAI SABAKI)</strong></p><ul>'
            '<li>Sva kretanja</li>'
            '<li>Izbegavanje 1 na 1 – od udarca od gore u glavu (SHOMEN UCHI)</li>'
            '<li>od udarca u stomak (CHUDAN TSUKI)</li></ul>'
            '<p><strong>TEHNIKE</strong></p><ul>'
            '<li>Odbrana od hvata za istu ruku- bacanje polugom na laktu i zglobu šake (KATATE TORI AI HANMI UDE GARAMI)</li>'
            '<li>Odbrana od hvatova za rame od pozadi -bacanje šamarom (USHIRO ERI TORI TENCHI NAGE)</li>'
            '<li>Odbrana od hvatova za rame od pozadi- poluga na vratu (USHIRO ERI TORI IRIMI NAGE)</li>'
            '<li>Odbrana od hvata za istu ruku- bacanje preko kuka (KATATE TORI AI HANMI KOSHI NAGE)</li>'
            '<li>Odbrana od hvata za rame savijanje lakta</li>'
            '<li>Odbrana od kružnog udarca u glavu-poluga na malom prstu –treća forma (YOKOMEN UCHI UCHI KAITEN SANKYO)</li>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke od pozadi-poluga na zglobu šake i laktu (USHIRO RYOTE TORI SHIHO NAGE)</li>'
            '<li>Odbrana od udarca u stomak poluga na laktu (CHUDAN TSUKI UDE OSAE)</li>'
            '<li>Odbrana od kružnog udarca u glavu- poluga na zglobu šake izvrtanjem (YOKOMEN UCHI KOTEGAESHI)</li>'
            '<li>Odbrana od udarca pesnicom u stomak- poluga na vratu (CHUDAN TSUKI IRIMI NAGE)</li>'
            '<li>Odbrana od kružnog udarca nogom – niski (MAVASHI GERI)</li>'
            '<li>Odbrana od davljenja od pozadi (UDE OSAE)</li></ul>'
            '<p><strong>Odbrana od oružja (buki waza)</strong></p>'
            '<p><em>Odbrana od noža</em></p><ul>'
            '<li>Odbrana od uboda nožem od dole poluga na zglobu šake i laktu-privođenje (GEDAN TSUKI TANTO TORI UDE GARAMI)</li>'
            '<li>Odbrana od boda od gore – treća forma (SHOMEN UCHI TANTO TORI SANKYO)</li></ul>'
            '<p><em>Odbrana od palice</em></p><ul>'
            '<li>Odbrana od kružnog udarca palicom -bacanje šamarom (YOKOME UCHI TENCHI NAGE)</li>'
            '<li>Odbrana od kružnog udarca palicom iznutra spolja -bacanje polugom na laktu i zglobu šake (URAKEN UDE GARAMI)</li></ul>'
            '<p><em>Odbrana od pištolja</em></p><ul>'
            '<li>Odbrana od pretnje pištoljem sa leve strane (UDE OSAE OSETO GARI)</li>'
            '<li>Odbrana od pretnje pištoljem sa desne strane (KOTEGAESHI)</li></ul>'
        ),
    },
    {
        'name': '1 Kyu braon pojas',
        'color': 'brown',
        'description': (
            '<p><strong>PADOVI (UKEMI)</strong></p><ul><li>Svi padovi</li></ul>'
            '<p><strong>KRETANJA (TAI SABAKI)</strong></p><ul><li>Sva kretanja</li></ul>'
            '<p><strong>JIYU WAZA (ODBRANA OD 2 NAPADAČA)</strong></p><ul>'
            '<li>Odbrana od udarca u glavu od gore (SHOMEN UCHI)</li>'
            '<li>Odbrana od udarca u stomak (TSUKI)</li></ul>'
            '<p><strong>TEHNIKE</strong></p><ul>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke od pozadi bacanje preko kuka (USHIRO RYOTE TORI KOSHI NAGE)</li>'
            '<li>Odbrana od hvata sa dve ruke za dve ruke -bacanje preko kuka (RYOTE TORI KOSHI NAGE)</li>'
            '<li>Odbrana od udarca pesnicom u glavu-poluga na vratu (JODAN TSUKI IRIMI NAGE)</li>'
            '<li>Odbrana od udarca od gore u glavu-poluga na vratu –direktna (SHOMEN UCHI IRIMI NAGE)</li>'
            '<li>Odbrana od udarca od gore u glavu- bacanje povlačenjem glave na dole (SHOMEN UCHI KUBI SHIME NAGE)</li>'
            '<li>Odbrana od hvata za kragnu od pozadi-provlačenje iznutra čišćenje (USHIRO ERI TORI UDE OSAE OSETO GARI)</li>'
            '<li>Odbrana od kružnog udarca u glavu poluga na zglobu šake i laktu – nadhvat (YOKOMEN UCHI UDE GARAMI)</li>'
            '<li>Odbrana od direktnog udarca u glavu bacanje polugom na zglobu šake i laktu (JODAN TSUKI UDE GARAMI)</li>'
            '<li>Odbrana od kružnog udarca nogom u glavu – provlačenjem ispod noge (MAVASHI GERI)</li></ul>'
            '<p><strong>Odbrana od oružja (buki waza)</strong></p>'
            '<p><em>Odbrana od noža</em></p><ul>'
            '<li>Odbrana od kružnog boda nožem presretanje i podhvat (YOKOMEN UCHI TANTOTORI UDE GARAMI)</li>'
            '<li>Odbrana od kružnog boda nožem poluga na laktu (YOKOMEN UCHI TANTO TORI UDE OSAE)</li>'
            '<li>Odbrana od kružnog boda iznutra spolja –poluga na zglobu šake izvrtanjem (URAKEN TANTO TORI KOTEGAESHI)</li></ul>'
            '<p><em>Odbrana od palice</em></p><ul>'
            '<li>Odbrana od udarca palicom od gore u glavu – bacanje preko kuka (SHOMEN UCHI KOSHINAGE)</li>'
            '<li>Odbrana od udarca palicom od gore u glavu – presretanje – gušenje</li>'
            '<li>Odbrana od udarca palicom od gore ubacivanje ramena pod pazuh</li>'
            '<li>Odbrana od kružnog udarca palicom – presretanje – čišćenje (YOKOMEN UCHI OSETO GARI)</li></ul>'
            '<p><em>Odbrana od pištolja</em></p><ul>'
            '<li>Pretnja pištoljem s leđa okret unutra i poluga na laktu</li>'
            '<li>Pretnja pištoljem s leđa okret spolja i poluga na zglobu šake</li></ul>'
        ),
    },
]


class Command(BaseCommand):
    help = 'Restore full belt curriculum content and colors from original programs page'

    def handle(self, *args, **options):
        kids, _ = Program.objects.get_or_create(
            audience='kids',
            defaults={'title': 'Za decu', 'sort_order': 1, 'is_active': True},
        )
        adults, _ = Program.objects.get_or_create(
            audience='adults',
            defaults={'title': 'Za odrasle', 'sort_order': 2, 'is_active': True},
        )
        kids.belts.all().delete()
        adults.belts.all().delete()

        for i, belt in enumerate(KIDS, start=1):
            ProgramBelt.objects.create(program=kids, sort_order=i, **belt)
        for i, belt in enumerate(ADULTS, start=1):
            ProgramBelt.objects.create(program=adults, sort_order=i, youtube_id='', **belt)

        self.stdout.write(self.style.SUCCESS(
            f'Restored {kids.belts.count()} kids belts and {adults.belts.count()} adult belts with full curriculum.'
        ))

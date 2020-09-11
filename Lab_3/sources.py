from ugradio import coord
class source:
    def __init__(self, name, ra, dec, SA):
        self.name = name
        self.ra = self.convert_ra(ra)
        self.dec = self.convert_dec(dec)
        self.SA = SA
    def get_alt(self, JD):
        alt =coord.get_altaz(self.ra, self.dec, JD)[0]
        return alt
    def convert_ra(self, ra):
        h, m, s = ra.split(':')
        return (int(h)+float(m)/60+float(s)/3600)*15
    def convert_dec(self, dec):
        try:
            _, _ = dec.split('-')
            d, m,s = dec.split(':')
            return -1*(float(d)+float(m)/60+float(s)/3600)
        except ValueError:
            d, m, s = dec.split(':')
            return float(d)+float(m)/60+float(s)/3600

crab   = source('crab',   '5:34:31.95',  '22:0:52.1',   496)
orion  = source('orion',  '5:35:17.3',   '-5:23:28',    340)
M17    = source('M17',    '18:20:26',    '-16:10.6:0',  500)
cygnus = source('cygnus', '19:59:28.357', '40:44:2.1',  120)
cas    = source('cas',    '23:23:24',     '58:48.9:0',  320)

sources = [crab, orion, M17, cygnus, cas]

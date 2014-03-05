.separator ";"
.import adreslijst.csv huishouden
insert into nrgweb_huishouden (straat,huisnummer,huisnummer_toevoeging,woonplaats,postcode,aantal_personen,email,telefoonnummer,password) select * from huishouden;
drop table huishouden;

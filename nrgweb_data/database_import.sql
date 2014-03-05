.separator ";"
.import adreslijst.csv huishouden
insert into nrgweb_huishouden (straat,huisnummer,huisnummer_toevoeging,woonplaats,postcode,aantal_personen,email,telefoonnummer,password) select * from huishouden;
drop table huishouden;
.import apparaat_cat.txt nrgweb_apparaatcategorie
.import tijden.txt nrgweb_metingtijden
insert into nrgweb_apparaat values (null,'Zonnepaneel','Philips','Suncatcher 4140');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Philips','Suncatcher 4180');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Philips','Suncatcher 6140');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Philips','Suncatcher 6180');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Siemens','SolarSense 60W12');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Siemens','SolarSense 80W12');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Siemens','SolarSense 60W24');
insert into nrgweb_apparaat values (null,'Zonnepaneel','Siemens','SolarSense 80W24');
insert into nrgweb_apparaat values (null,'Hamsterwheel','Pets & Co','Small brown hamster');
insert into nrgweb_huishoudenapparaat values(null,'500','2');
insert into nrgweb_huishoudenapparaat values(null,'500','8');
insert into nrgweb_huishoudenapparaat values(null,'500','9');


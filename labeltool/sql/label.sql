drop table if exists tasks;
create table tasks (
  tasks_id integer primary key not null,
  dataset_name varchar not null,
  name varchar not null,
  status varchar not null
);
drop table if exists image;
create table image (
  image_id integer primary key not null,
  tasks_id integer not null,
  image_path varchar not null,
  status varchar not null,
  FOREIGN KEY(tasks_id) REFERENCES tasks(tasks_id)

);

-- insert into tasks values(1,"Chinese","start");
-- insert into tasks values(2,"Abacus_Seeds","start");
-- insert into tasks values(3,"Herbal_Chicken","start");
-- insert into tasks values(4,"Ah_boling","start");
-- insert into tasks values(5,"Bak_Chang","start");
-- insert into tasks values(6,"Bak_Chor_Mee","start");
-- insert into image values(1,4,'../static/image/Chinese/Ah_boling/boiling.jpg','unlabelled','none');
-- insert into image values(2,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174251.jpg','unlabelled','none');
-- insert into image values(3,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174256.jpg','unlabelled','none');
-- insert into image values(4,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174331.jpg','unlabelled','none');
-- insert into image values(5,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174405.jpg','unlabelled','none');
-- insert into image values(6,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174415.jpg','unlabelled','none');
-- insert into image values(7,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174444.jpg','unlabelled','none');
-- insert into image values(8,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174547.jpg','unlabelled','none');
-- insert into image values(9,4,'../static/image/Chinese/Ah_boling/IMG_20150831_174643.jpg','unlabelled','none');
-- insert into image values(10,4,'../static/image/Chinese/Ah_boling/IMG_20150831_182857.jpg','unlabelled','none');
-- insert into image values(11,4,'../static/image/Chinese/Ah_boling/IMG_20150831_182908.jpg','unlabelled','none');
-- insert into image values(12,4,'../static/image/Chinese/Ah_boling/IMG_20150831_182928.jpg','unlabelled','none');
-- insert into image values(13,4,'../static/image/Chinese/Ah_boling/IMG_20150831_182949.jpg','unlabelled','none');
-- insert into image values(14,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183014.jpg','unlabelled','none');
-- insert into image values(15,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183030.jpg','unlabelled','none');
-- insert into image values(16,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183058.jpg','unlabelled','none');
-- insert into image values(17,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183105.jpg','unlabelled','none');
-- insert into image values(18,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183110.jpg','unlabelled','none');
-- insert into image values(19,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183118.jpg','unlabelled','none');
-- insert into image values(20,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183149.jpg','unlabelled','none');
-- insert into image values(21,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183210.jpg','unlabelled','none');
-- insert into image values(22,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183238.jpg','unlabelled','none');
-- insert into image values(23,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183254.jpg','unlabelled','none');
-- insert into image values(24,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183324.jpg','unlabelled','none');
-- insert into image values(25,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183339.jpg','unlabelled','none');
-- insert into image values(26,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183355.jpg','unlabelled','none');
-- insert into image values(27,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183408.jpg','unlabelled','none');
-- insert into image values(28,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183430.jpg','unlabelled','none');
-- insert into image values(29,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183445.jpg','unlabelled','none');
-- insert into image values(30,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183447.jpg','unlabelled','none');
-- insert into image values(31,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183506.jpg','unlabelled','none');
-- insert into image values(32,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183603.jpg','unlabelled','none');
-- insert into image values(33,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183626.jpg','unlabelled','none');
-- insert into image values(34,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183638.jpg','unlabelled','none');
-- insert into image values(35,4,'../static/image/Chinese/Ah_boling/IMG_20150831_183710.jpg','unlabelled','none');

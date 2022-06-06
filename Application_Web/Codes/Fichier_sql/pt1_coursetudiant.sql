create table coursetudiant
(
    id                 int auto_increment
        primary key,
    id_cours           varchar(20) not null,
    no_immatriculation varchar(20) not null,
    constraint fk_coursEtudiant_Cours
        foreign key (id_cours) references cours (id_cours),
    constraint fk_coursEtudiant_Etudiant
        foreign key (no_immatriculation) references etudiant (no_immatriculation)
);

INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (1, '11X008', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (2, 'D200008', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (3, 'D200009', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (4, 'D200013', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (5, 'D200014', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (6, 'D200017', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (7, 'D200025', '20-315-365');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (8, 'D200008', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (9, 'D200009', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (10, 'D200013', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (11, 'D200014', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (12, 'D200017', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (13, 'D200020', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (14, 'D200025', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (15, '11M010', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (16, '12B801', '20-315-65');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (17, '1_22H001', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (18, '10A001', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (19, '11B001', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (20, '11B001', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (21, '11B002', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (22, '11B003', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (23, '11C001', '10-300-30');
INSERT INTO pt1.coursetudiant (id, id_cours, no_immatriculation) VALUES (24, '11C002', '10-300-30');

create table etudiant
(
    no_immatriculation varchar(20) not null
        primary key,
    nom                varchar(20) null,
    prenom             varchar(20) null,
    semestre_etude     int         null,
    centres_interets   longtext    null
);

INSERT INTO pt1.etudiant (no_immatriculation, nom, prenom, semestre_etude, centres_interets) VALUES ('10-300-30', 'doe', 'john', 6, 'religion, histoire, peinture, mathématiques');
INSERT INTO pt1.etudiant (no_immatriculation, nom, prenom, semestre_etude, centres_interets) VALUES ('20-315-365', 'missiri', 'nikita', 4, 'programmation, informatique, économie, science');
INSERT INTO pt1.etudiant (no_immatriculation, nom, prenom, semestre_etude, centres_interets) VALUES ('20-315-65', 'cissé', 'kerfalla', 4, 'programmation, machine learning, algorithmique');

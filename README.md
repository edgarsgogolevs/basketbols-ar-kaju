# basketbols-ar-kaju

NBA game outcome prediction.

## Saturs

- [Tehniskais risinājums](#Tehniskais-risinājums)
- [Concept](#Konceptu-modelis)
- [Algoritms](#Algoritms)
- [Lietotāju stāsti](#Lietotāju-stāsti)


## Tehniskais risinājums

### Frontend

| Satvars | Vue.js |
| ---- | ---- |
| Programmēšanas valoda | Javascript |
| Tīmekļa serveris | Nginx |

Tika pielietota client-side rendering pieeja. Piekļuve datu bāzei notiek caur HTTP pieprasījumiem uz API.

### Backend

| Satvars               | Flask  |
| --------------------- | ------ |
| Programmēšanas valoda | Python |
| Tīmekļa serveris      |Waitress|

Pieprasījumu un atbilžu validācijai tiek pielietota Marshmallow bibliotēka.

### Datubāze

Izmantotā datubāze ir Azure SQL server. Tās pamatā ir Microsoft SQL Server, kas izmanto Transact SQL dielektu.

### Izmantotā infrastruktūra

Visi resursi tika izvietoti Azure platformā.
Datu bāze - Azure SQL server
Frontent un Backend - Azure Container App
Failu krātuve - Azure BLOB Storage

## Algoritms

Lai pareģotu basketbola spēles tika izmantota mašīnmācīšanās pieeja.
### XGBoostClassifier 
Bāzē izmanto daudzus lēmumu kokus kopā. Mēs sniedzam tam datus un norādām, ko vēlamies prognozēt (vai komanda uzvarēs vai nē). Modelis mācās no šiem datiem, veido daudzus kokus, un katrs jauns koks cenšas labot iepriekšējo koku kļūdas. Galu galā mums ir ansamblis (daudzi kopā) koku, kas darbojas kopā, lai sniegtu precīzu prognozi par jaunajiem datiem. 
### Loģistiskā regresija 
Tiek zmantota binārajai klasifikācijai. Tā izveido vienādojumu, apvienojot svērtos lielumus, pārvērš to varbūtībā, izmantojot loģistisko funkciju, un pieņem lēmumu, pamatojoties uz šo varbūtību. Modelis tiek apmācīts, optimizējot svarus, lai tā prognozes būtu tuvākas reālajiem datiem. 
### Support Vector Machine 
Meklē optimālo hiperplānu klašu nodalīšanai datos. Pamatideja ir maksimizēt atšķirību starp klasēm, izmantojot atbalsta vektorus. Modelis tiek apmācīts, lai atrastu optimālo hiperplakni ar maksimālo atstarpi, un to var izmantot, lai prognozētu, vai jauni objekti pieder klasēm.
### RandomForestClassifier 
Izveido lēmumu koku grupu. Katrs koks tiek apmācīts, izmantojot nejaušu datu apakšparaugu un nejaušus raksturlielumus. Koku balsošanas rezultātā modelis veido prognozi par jaunajiem datiem. RandomForestClassifier ir efektīvs, izturīgs pret pārmācīšanu un spēj novērtēt pazīmju nozīmīgumu.


## Konceptu modelis
![Concept model](./basketball_konceptu_modelis.excalidraw.png)

## Lietotāju stāsti

| Apraksts                                                                                                                                                              | Prioritāte (1..10) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------:|
| Lietotājam ir iespēja izvēlēties pareģošanas modeli un apskatīt pareģojumu noteiktai spēlei                                                                           |         10         |
| Lietotājam ir iespēja apskatīties tuvākās NBA spēles                                                                                                                  |         8          |
| Gadījumā, ja kāda no spēlēm nav sarakstā, lietotājam ir iespēja piedāvāt trūkstošo spēli. Tiek pārbaudīts, vai tā tiešām ir reāla spēle un tiek pievienota sarakstam. |         6          |
| Lietotājam ir iespēja apskatīt datus par modeli (nosaukums, nominālā precizitāte, pareģošanas vēsture)                                                                |         5          |
| Ar ChatGPT izveidotā reportāža par spēli                                                                                                                              |         3          |
| Pareģošanas modelim ir savs profils ar bildi, vārdu, uzvārdu un statistiku                                                                                            |         4          |


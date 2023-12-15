# basketbols-ar-kaju

NBA game outcome prediction.

### Saturs

- [Technology stack](#Technology-stack)
- [Concept](#Concept)
- [Lietotāju stāsti](#Lietotāju-stāsti)

### Technology stack

Frontend: 
 - Framework – Vue.js
 - Programming language – Javascript
 - Virtualization – Docker
 
Backend: 
 - Framework – Flask
 - Programming language – Python
 - Server – Waitress
 - Virtualization – Docker
 
Machine learning:
 - Framework – Scikit learn
 - Programming language – Python
 
Database: Azure SQL

Infrastructure:
 - Azure SQL servers
 - Azure BLOB storage
 - Azure Container App

### Concept
![Concept model](./basketball_konceptu_modelis.excalidraw.png)

### Lietotāju stāsti

| Apraksts                                                                                                                                                              | Prioritāte (1..10) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------:|
| Lietotājam ir iespēja izvēlēties pareģošanas modeli un apskatīt pareģojumu noteiktai spēlei                                                                           |         10         |
| Lietotājam ir iespēja apskatīties tuvākās NBA spēles                                                                                                                  |         8          |
| Gadījumā, ja kāda no spēlēm nav sarakstā, lietotājam ir iespēja piedāvāt trūkstošo spēli. Tiek pārbaudīts, vai tā tiešām ir reāla spēle un tiek pievienota sarakstam. |         6          |
| Lietotājam ir iespēja apskatīt datus par modeli (nosaukums, nominālā precizitāte, pareģošanas vēsture)                                                                |         5          |
| Ar ChatGPT izveidotā reportāža par spēli                                                                                                                              |         3          |
| Pareģošanas modelim ir savs profils ar bildi, vārdu, uzvārdu un statistiku                                                                                            |         4          |


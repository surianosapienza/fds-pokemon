# fds-pokemon
Cartella del progetto di fds
link kaggle: https://www.kaggle.com/competitions/fds-pokemon-battles-prediction-2025


IN GENERALE
xgboost è il miglior modello. serve solo sistemare le feature adesso

ho notato che in pokemon effectiveness manca il noteffective e chat mi da piccoli problemi
c'è da implementare il colpo critico con la velocità

forse ha piu senso considerare la differenza tra max e min per le singole stats invece della media? (es. pkmn con maggior valore di speed meno pkmn con minor valore di speed all'interno della squadra)

ho provato a rimuovere delle feature ma lo score e' peggiorato, la versione non aggiornata si trova in preprocessing_backup

TASK

EDO
count mosse superefficaci FATTO
count mosse potenziate FATTO
numero di pokemon morti di p2 FATTO
numero di pokemon morti di p1 FATTO
numero di volte che è stato cambiato pokemon FATTO
guarda ogni stato singolarmente FATTO
inserisci category e il count dei diversi tipi FATTO
stessa cosa con gli stati come scritto appena su FATTO
media delle medie delle stat del team FATTO 
bisogna guardare meglio le feature del singolo pokemon per tunare meglio -> sentiamoci FATTO
media base_power delle mosse FATTO
accuracy per le mosse di tipo STATUS (count di mosse non mandate a segno) 
numero di miss 

max tra atk e sp atk 
rivedere feature hp FATTO
fare un'unica feature per gli stati, assegnando un peso ad ogni stato e poi sommarli FATTO
fare un'unica feature sul moltiplicatore mettendo insieme stab e super efficace FATTO


FRA
sistemare iperparametri 
modificare il modelling mettendo mean+-stdev nei kfold          FATTO
aggiungere gli altri modelli
guardare bene il kfold e dirgli di fare accuracy solo sulla vali!!!!    FATTO
bisogna guardare meglio le feature del singolo pokemon per tunare meglio -> sentiamoci


ANGELO 
commentare le celle dei notebook: 01_preprocessing.ipynb e 03_modeling.ipynb
provare a pensare a nuove feature da inserire (regola rasoio di occam) e aggiungerle alle task di EDO




COSE DA FARE PRIMA DI RUNNARE
nella logistic se cambi il dataset ricordati di trovare il migliore c possibile